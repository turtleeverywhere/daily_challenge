"""
🧩 Daily Challenge: 2026-02-25 — LRU Cache
Language: Python
Difficulty: Intermediate (Wednesday)
Time: 15–25 minutes

## Problem

Implement a Least Recently Used (LRU) Cache from scratch.

Your LRUCache class should support:
- `LRUCache(capacity)` — initialize with a positive capacity
- `get(key)` — return the value if key exists, otherwise -1
- `put(key, value)` — insert or update the key-value pair;
  if the cache exceeds capacity, evict the LEAST recently used key

Both `get` and `put` must run in O(1) average time.

## Examples

    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    cache.get(1)        # → 10  (key 1 is now most recently used)
    cache.put(3, 30)    # evicts key 2 (least recently used)
    cache.get(2)        # → -1  (evicted)
    cache.get(3)        # → 30
    cache.put(4, 40)    # evicts key 1
    cache.get(1)        # → -1
    cache.get(3)        # → 30
    cache.get(4)        # → 40

## Constraints

- 1 <= capacity <= 1000
- Keys and values are integers
- You may NOT use `functools.lru_cache` or `collections.OrderedDict`
  (the whole point is to build the mechanism yourself)

## Starter Template
"""

from __future__ import annotations


class Node:
    """Doubly-linked list node."""
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # TODO: set up your data structures
        #   - a dict for O(1) key lookup
        #   - a doubly-linked list for O(1) insertion/removal
        pass

    def get(self, key: int) -> int:
        # TODO: return value if present (and mark as recently used), else -1
        pass

    def put(self, key: int, value: int) -> None:
        # TODO: insert/update key; evict LRU entry if over capacity
        pass


# ─── Hints (try solving first!) ──────────────────────────────────────────────
#
# Hint 1: Use two sentinel (dummy) nodes — head and tail — so you never
#          deal with None checks when linking/unlinking nodes.
#
# Hint 2: "Most recently used" goes right after head;
#          "Least recently used" sits right before tail.
#
# Hint 3: Every get() and put() that touches an existing node should
#          (a) unlink the node from its current position, then
#          (b) re-insert it right after head.
#
# Hint 4: When evicting, remove tail.prev, and also delete its key
#          from the dict.
# ─────────────────────────────────────────────────────────────────────────────


# ─── Tests ───────────────────────────────────────────────────────────────────
def run_tests():
    print("Running tests...")

    # Basic usage
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    assert cache.get(1) == 10, "Test 1 failed"
    cache.put(3, 30)  # evicts key 2
    assert cache.get(2) == -1, "Test 2 failed: key 2 should be evicted"
    assert cache.get(3) == 30, "Test 3 failed"
    cache.put(4, 40)  # evicts key 1
    assert cache.get(1) == -1, "Test 4 failed: key 1 should be evicted"
    assert cache.get(3) == 30, "Test 5 failed"
    assert cache.get(4) == 40, "Test 6 failed"

    # Update existing key doesn't increase size
    cache2 = LRUCache(1)
    cache2.put(1, 100)
    cache2.put(1, 200)
    assert cache2.get(1) == 200, "Test 7 failed: update should change value"

    # Capacity of 1
    cache3 = LRUCache(1)
    cache3.put(1, 1)
    cache3.put(2, 2)
    assert cache3.get(1) == -1, "Test 8 failed"
    assert cache3.get(2) == 2, "Test 9 failed"

    print("All tests passed! ✅")


if __name__ == "__main__":
    run_tests()
