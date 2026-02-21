"""
Daily Challenge: 2026-02-21
Language: Python | Difficulty: Advanced

# Parallel Data Pipeline with Backpressure

## Problem

Build a concurrent data processing pipeline using `asyncio` that:

1. **Producer** — generates items at variable speed (simulated)
2. **Transformer** (N workers) — applies an async transformation to each item
3. **Consumer** — collects results in order (not arrival order — *original* order)

The twist: implement **backpressure**. If the transformer queue exceeds a
configurable high-water mark, the producer must pause until the queue drains
below a low-water mark.

## Requirements

- Use only the standard library (`asyncio`, `collections`, `dataclasses`, etc.)
- The pipeline must preserve original ordering in the final output.
- Backpressure must actually pause the producer (not just drop items).
- Graceful shutdown: producer signals completion, all stages drain, pipeline
  returns the collected results.

## Example

    items_in  = list(range(20))
    results   = await run_pipeline(
        items=items_in,
        num_workers=4,
        high_water=6,
        low_water=2,
        transform=some_async_fn,
    )
    assert results == [some_async_fn(i) for i in items_in]  # order preserved

## Starter Template

Fill in the functions below. The `main()` at the bottom runs a demo.
"""

import asyncio
import random
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, List


@dataclass
class PipelineStats:
    """Track pipeline health metrics."""
    produced: int = 0
    transformed: int = 0
    consumed: int = 0
    backpressure_pauses: int = 0


# Hint: use an asyncio.Event for backpressure signaling.
#   - Set the event when queue size < low_water  (producer may continue)
#   - Clear the event when queue size >= high_water (producer must wait)

# Hint: to preserve ordering, tag each item with a sequence number.
#   A dict or list indexed by sequence number in the consumer works well.

# Hint: use asyncio.Queue for the stages. Sentinel values (None) signal shutdown.


async def producer(
    items: List[Any],
    out_queue: asyncio.Queue,
    flow_control: asyncio.Event,
    stats: PipelineStats,
) -> None:
    """Feed items into the pipeline, respecting backpressure."""
    # TODO: iterate items, put (seq, item) onto out_queue
    # Before each put, await flow_control if it's cleared
    pass


async def transformer(
    in_queue: asyncio.Queue,
    out_queue: asyncio.Queue,
    transform: Callable[[Any], Awaitable[Any]],
    stats: PipelineStats,
) -> None:
    """Pull (seq, item), apply transform, push (seq, result)."""
    # TODO: loop until sentinel, apply transform, forward result
    pass


async def consumer(
    in_queue: asyncio.Queue,
    total: int,
    stats: PipelineStats,
) -> List[Any]:
    """Collect results and reorder by original sequence number."""
    # TODO: gather results, return them in original order
    pass


def _update_backpressure(
    queue: asyncio.Queue,
    flow_control: asyncio.Event,
    high_water: int,
    low_water: int,
    stats: PipelineStats,
) -> None:
    """Check queue size and set/clear the flow control event."""
    # TODO: implement high/low water mark logic
    pass


async def run_pipeline(
    items: List[Any],
    num_workers: int,
    high_water: int,
    low_water: int,
    transform: Callable[[Any], Awaitable[Any]],
) -> List[Any]:
    """
    Orchestrate the full pipeline: producer → transformers → consumer.
    Returns results in original item order.
    """
    stats = PipelineStats()
    # TODO: wire up queues, events, tasks — return ordered results
    pass


# --------------- demo ---------------

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
