"""
Reference Solution: 2026-02-21 — Parallel Pipeline
Language: Python | Difficulty: Advanced

## Approach

The pipeline has three stages connected by asyncio.Queues:

    Producer → [work_queue] → Transformer(s) → [result_queue] → Consumer

Key design decisions:

1. **Sequence numbers for ordering.**
   The producer tags every item as (seq, item). Transformers forward (seq, result).
   The consumer slots results into a pre-allocated list by index — O(1) reorder,
   no sorting needed.

2. **Backpressure via asyncio.Event + hysteresis.**
   A single Event acts as a gate for the producer:
     - When work_queue size >= high_water → clear the event (producer blocks).
     - When work_queue size <= low_water  → set the event (producer resumes).
   The gap between high and low water prevents rapid toggling (classic
   hysteresis pattern, same idea as TCP flow control).

3. **Sentinel-based shutdown.**
   After the producer finishes, it pushes one None per transformer worker.
   Each transformer exits on None and pushes its own None to the result queue.
   The consumer counts sentinel Nones; when it's seen num_workers of them,
   it knows all results are in.

4. **No unbounded queues.**
   Both queues are bounded (maxsize = high_water * 2 as a safety net),
   but the real throttle is the Event-based backpressure — it kicks in
   well before the queue fills up.
"""

import asyncio
import random
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, List


@dataclass
class PipelineStats:
    """Track pipeline health metrics."""
    produced: int = 0
    transformed: int = 0
    consumed: int = 0
    backpressure_pauses: int = 0


# ──────────────────────────────────────────────
# Backpressure helper
# ──────────────────────────────────────────────

def _update_backpressure(
    queue: asyncio.Queue,
    flow_control: asyncio.Event,
    high_water: int,
    low_water: int,
    stats: PipelineStats,
) -> None:
    """
    Hysteresis-based flow control.

    Why hysteresis? Without the gap between high and low marks, the producer
    would alternate between "paused" and "running" on every single item when
    the queue hovers near one threshold. The two-threshold approach means:
      - Once we pause, we stay paused until the queue drains significantly.
      - Once we resume, we stay running until the queue fills up again.
    """
    size = queue.qsize()
    if size >= high_water and flow_control.is_set():
        # Queue is getting full — tell the producer to pause.
        flow_control.clear()
        stats.backpressure_pauses += 1
    elif size <= low_water and not flow_control.is_set():
        # Queue has drained enough — let the producer continue.
        flow_control.set()


# ──────────────────────────────────────────────
# Pipeline stages
# ──────────────────────────────────────────────

async def producer(
    items: List[Any],
    out_queue: asyncio.Queue,
    flow_control: asyncio.Event,
    stats: PipelineStats,
    num_workers: int,
) -> None:
    """
    Feed items into the pipeline, respecting backpressure.

    Each item is tagged with a sequence number so the consumer can
    reconstruct the original order regardless of which worker finishes first.
    """
    for seq, item in enumerate(items):
        # Block here if backpressure is active (event is cleared).
        # This is the core mechanism: the producer *actually stops producing*
        # rather than flooding the queue.
        await flow_control.wait()

        await out_queue.put((seq, item))
        stats.produced += 1

    # Send one sentinel per worker so each transformer gets exactly one
    # shutdown signal. (If we sent just one, only one worker would exit
    # and the others would hang forever.)
    for _ in range(num_workers):
        await out_queue.put(None)


async def transformer(
    in_queue: asyncio.Queue,
    out_queue: asyncio.Queue,
    transform: Callable[[Any], Awaitable[Any]],
    flow_control: asyncio.Event,
    high_water: int,
    low_water: int,
    stats: PipelineStats,
) -> None:
    """
    Pull (seq, item), apply the async transform, push (seq, result).

    After each get, we update backpressure — this is the "drain" side.
    When enough items have been consumed from the work queue, the producer
    gets unblocked.
    """
    while True:
        msg = await in_queue.get()

        if msg is None:
            # Sentinel: this worker is done. Forward a sentinel to the
            # consumer so it can track how many workers have finished.
            await out_queue.put(None)
            return

        seq, item = msg

        # After pulling an item, the work queue got smaller — check if
        # we should release backpressure.
        _update_backpressure(in_queue, flow_control, high_water, low_water, stats)

        # The actual work. This runs concurrently across all transformer
        # workers — that's where the parallelism comes from.
        result = await transform(item)
        stats.transformed += 1

        await out_queue.put((seq, result))


async def consumer(
    in_queue: asyncio.Queue,
    total: int,
    num_workers: int,
    stats: PipelineStats,
) -> List[Any]:
    """
    Collect results and reorder by original sequence number.

    We pre-allocate a results list of the right size and slot each result
    into its position by seq number. This avoids sorting and is O(n).

    We know we're done when we've received `num_workers` sentinels (one
    from each transformer) — that guarantees every real item has already
    been forwarded.
    """
    results: list[Any] = [None] * total
    sentinels_seen = 0

    while sentinels_seen < num_workers:
        msg = await in_queue.get()

        if msg is None:
            sentinels_seen += 1
            continue

        seq, result = msg
        results[seq] = result  # Direct index placement — preserves order.
        stats.consumed += 1

    return results


# ──────────────────────────────────────────────
# Orchestrator
# ──────────────────────────────────────────────

async def run_pipeline(
    items: List[Any],
    num_workers: int,
    high_water: int,
    low_water: int,
    transform: Callable[[Any], Awaitable[Any]],
) -> List[Any]:
    """
    Wire everything together and run until completion.

    Layout:
        producer --→ work_queue --→ transformer ×N --→ result_queue --→ consumer

    The flow_control Event gates the producer. Transformers update it after
    each get from work_queue. The consumer just collects and reorders.
    """
    stats = PipelineStats()

    # Bounded queues as a safety net. The real throttle is the Event,
    # but bounded queues prevent memory blowup if something goes wrong.
    work_queue: asyncio.Queue = asyncio.Queue(maxsize=high_water * 2)
    result_queue: asyncio.Queue = asyncio.Queue(maxsize=high_water * 2)

    # Start with the gate open — the producer can run freely until
    # the queue hits high_water for the first time.
    flow_control = asyncio.Event()
    flow_control.set()

    # Launch all stages as concurrent tasks.
    producer_task = asyncio.create_task(
        producer(items, work_queue, flow_control, stats, num_workers)
    )

    transformer_tasks = [
        asyncio.create_task(
            transformer(
                work_queue, result_queue, transform,
                flow_control, high_water, low_water, stats,
            )
        )
        for _ in range(num_workers)
    ]

    # The consumer is the "driver" — we await its result directly.
    results = await consumer(result_queue, len(items), num_workers, stats)

    # By the time the consumer returns, all sentinels have been received,
    # which means all transformers have exited, which means the producer
    # has exited. But we await them anyway for clean error propagation.
    await producer_task
    await asyncio.gather(*transformer_tasks)

    print(
        f"Pipeline stats: produced={stats.produced} "
        f"transformed={stats.transformed} consumed={stats.consumed} "
        f"backpressure_pauses={stats.backpressure_pauses}"
    )

    return results


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

async def _demo_transform(x: int) -> int:
    """Simulate variable-cost async work."""
    await asyncio.sleep(random.uniform(0.01, 0.05))
    return x * x


async def main():
    items = list(range(30))
    results = await run_pipeline(
        items=items,
        num_workers=4,
        high_water=6,
        low_water=2,
        transform=_demo_transform,
    )
    expected = [i * i for i in items]
    assert results == expected, f"Order mismatch!\n{results}\n{expected}"
    print(f"✅ All {len(results)} results correct and in order.")


if __name__ == "__main__":
    asyncio.run(main())
