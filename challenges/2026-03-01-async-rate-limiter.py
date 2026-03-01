"""
🧩 Daily Challenge: 2026-03-01 — Async Rate Limiter
Language: Python
Difficulty: Advanced

## Problem

Implement an async rate limiter using the **token bucket** algorithm.

Your `RateLimiter` class should:
1. Allow a configurable `rate` (tokens added per second) and `capacity` (max burst size).
2. Provide an async `acquire(tokens=1)` method that:
   - Returns immediately if enough tokens are available.
   - Otherwise, **awaits** until enough tokens have been replenished.
3. Provide a `try_acquire(tokens=1) -> bool` method that returns True/False
   without blocking.
4. Be safe to use from multiple concurrent coroutines.

## Token Bucket Rules
- The bucket starts full (tokens = capacity).
- Tokens are added continuously at `rate` tokens/sec (fractional accumulation).
- The bucket never exceeds `capacity`.
- `acquire(n)` consumes `n` tokens atomically — partial consumption is not allowed.

## Example

    limiter = RateLimiter(rate=5, capacity=10)

    # Burst: 10 requests go through instantly
    for _ in range(10):
        await limiter.acquire()

    # 11th request must wait ~0.2s (1 token / 5 per sec)
    await limiter.acquire()

    # try_acquire returns False when bucket is empty
    assert limiter.try_acquire() is False

## Requirements
- Use only the Python standard library (asyncio).
- All time-tracking must use `asyncio.get_event_loop().time()` (monotonic).
- Must handle concurrent acquire() calls correctly (no double-spending tokens).

## Test Harness

Run this file directly to execute the tests:

    python 2026-03-01-async-rate-limiter.py

"""

import asyncio
import time as _time


class RateLimiter:
    """Token-bucket rate limiter for async code.

    Args:
        rate: Tokens added per second.
        capacity: Maximum tokens (burst size).
    """

    def __init__(self, rate: float, capacity: float):
        # TODO: Implement initialization
        #   - Store rate, capacity
        #   - Initialize token count to capacity
        #   - Record the current loop time
        #   - Create an asyncio.Lock for thread-safety
        pass

    def _refill(self) -> None:
        """Update token count based on elapsed time."""
        # TODO: Calculate elapsed time since last refill
        #   - Add (elapsed * rate) tokens
        #   - Clamp to capacity
        #   - Update the last-refill timestamp
        pass

    def try_acquire(self, tokens: float = 1) -> bool:
        """Try to consume tokens without waiting. Returns True on success."""
        # TODO: Refill, then check if enough tokens are available
        #   - If yes: subtract and return True
        #   - If no: return False
        pass

    async def acquire(self, tokens: float = 1) -> None:
        """Consume tokens, waiting if necessary until they're available."""
        # TODO: Use the lock to ensure atomicity
        #   - Refill tokens
        #   - If enough tokens: consume and return
        #   - Otherwise: calculate wait time = (tokens - self._tokens) / self.rate
        #   - Release lock, sleep, then retry
        #
        # HINT: A while-loop with asyncio.sleep works well here.
        # HINT: Be careful to re-acquire the lock and re-refill after sleeping.
        pass


# ─── Test Harness ────────────────────────────────────────────────────

async def test_burst():
    """Full capacity should be available immediately."""
    limiter = RateLimiter(rate=100, capacity=10)
    start = asyncio.get_event_loop().time()
    for _ in range(10):
        await limiter.acquire()
    elapsed = asyncio.get_event_loop().time() - start
    assert elapsed < 0.05, f"Burst took too long: {elapsed:.3f}s"
    print("✅ test_burst passed")


async def test_throttle():
    """Requests beyond capacity should be throttled."""
    limiter = RateLimiter(rate=10, capacity=5)
    start = asyncio.get_event_loop().time()
    for _ in range(10):  # 5 burst + 5 throttled (0.5s total wait)
        await limiter.acquire()
    elapsed = asyncio.get_event_loop().time() - start
    assert 0.4 < elapsed < 0.8, f"Expected ~0.5s, got {elapsed:.3f}s"
    print("✅ test_throttle passed")


async def test_try_acquire():
    """try_acquire should not block."""
    limiter = RateLimiter(rate=1, capacity=2)
    assert limiter.try_acquire() is True
    assert limiter.try_acquire() is True
    assert limiter.try_acquire() is False  # bucket empty
    print("✅ test_try_acquire passed")


async def test_concurrent():
    """Multiple coroutines should share the limiter safely."""
    limiter = RateLimiter(rate=20, capacity=5)
    results = []

    async def worker(wid: int):
        for _ in range(5):
            await limiter.acquire()
            results.append(wid)

    start = asyncio.get_event_loop().time()
    await asyncio.gather(*(worker(i) for i in range(4)))  # 20 total
    elapsed = asyncio.get_event_loop().time() - start

    assert len(results) == 20
    # 5 burst + 15 throttled at 20/s = 0.75s
    assert 0.5 < elapsed < 1.2, f"Expected ~0.75s, got {elapsed:.3f}s"
    print("✅ test_concurrent passed")


async def test_multi_token():
    """acquire() with tokens > 1 should work."""
    limiter = RateLimiter(rate=10, capacity=10)
    await limiter.acquire(5)  # instant
    assert limiter.try_acquire(6) is False  # only 5 left
    assert limiter.try_acquire(5) is True
    print("✅ test_multi_token passed")


async def main():
    await test_burst()
    await test_throttle()
    await test_try_acquire()
    await test_concurrent()
    await test_multi_token()
    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
