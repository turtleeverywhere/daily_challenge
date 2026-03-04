"""
🧩 Daily Challenge: 2026-03-04 — Trie Autocomplete

Language:   Python
Difficulty: Intermediate
Time:       15–25 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Problem

Implement a **Trie** (prefix tree) that supports:

1. `insert(word)` — Add a word to the trie.
2. `search(word) -> bool` — Return True if the exact word exists.
3. `starts_with(prefix) -> list[str]` — Return ALL words that start with
   the given prefix, sorted alphabetically.
4. `count_prefix(prefix) -> int` — Return how many words share the prefix
   (O(1) per node, not by collecting all words).

## Constraints

- Words contain only lowercase English letters (a–z).
- The trie should handle at least 10,000 words efficiently.
- `starts_with` returns results sorted alphabetically.
- `count_prefix` must NOT collect all words — store counts in the trie nodes.

## Examples

    t = Trie()
    t.insert("apple")
    t.insert("app")
    t.insert("application")
    t.insert("apt")
    t.insert("banana")

    t.search("app")           # True
    t.search("ap")            # False
    t.starts_with("app")      # ["app", "apple", "application"]
    t.starts_with("b")        # ["banana"]
    t.starts_with("z")        # []
    t.count_prefix("app")     # 3  (app, apple, application)
    t.count_prefix("a")       # 4  (app, apple, application, apt)
    t.count_prefix("banana")  # 1

## Bonus (optional)

- Add `delete(word) -> bool` that removes a word and decrements prefix
  counts. Return True if the word existed.
- Add `top_k(prefix, k) -> list[str]` that returns the k most recently
  inserted words with the given prefix.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from __future__ import annotations


class TrieNode:
    """A single node in the trie."""

    def __init__(self):
        # TODO: What does each node need to store?
        #   - children (dict mapping char -> TrieNode)
        #   - is this the end of a word?
        #   - how many words pass through this node?
        pass


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        # TODO: Walk the trie character by character, creating nodes as needed.
        # Don't forget to update prefix counts along the way!
        pass

    def search(self, word: str) -> bool:
        """Return True if the exact word exists in the trie."""
        # TODO: Walk the trie — the word exists only if you reach the end
        # AND the final node is marked as a word-end.
        pass

    def starts_with(self, prefix: str) -> list[str]:
        """Return all words starting with the given prefix, sorted."""
        # TODO: Navigate to the prefix node, then collect all words below it.
        # Hint: Use DFS (recursion or a stack) to gather complete words.
        pass

    def count_prefix(self, prefix: str) -> int:
        """Return the number of words that share the given prefix."""
        # TODO: Navigate to the prefix node and return its count.
        # If the prefix doesn't exist in the trie, return 0.
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HINTS (try solving first!)
#
# Hint 1: TrieNode needs three fields:
#   self.children: dict[str, TrieNode] = {}
#   self.is_end: bool = False
#   self.prefix_count: int = 0
#
# Hint 2: For insert, increment prefix_count on every node you visit
#   (including root), then mark the last node as is_end = True.
#
# Hint 3: For starts_with, first navigate to the prefix node, then use
#   a helper like _collect(node, current_prefix, results) that recurses
#   into children and appends to results when is_end is True.
#
# Hint 4: For delete (bonus), walk the path and decrement prefix_count.
#   Only unset is_end if the word actually existed.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def run_tests():
    """Basic test suite — run this to verify your solution."""
    t = Trie()

    # Insert words
    words = ["apple", "app", "application", "apt", "banana", "band", "bandana"]
    for w in words:
        t.insert(w)

    # search
    assert t.search("app") is True, "search('app') should be True"
    assert t.search("apple") is True, "search('apple') should be True"
    assert t.search("ap") is False, "search('ap') should be False"
    assert t.search("banz") is False, "search('banz') should be False"

    # starts_with
    assert t.starts_with("app") == ["app", "apple", "application"]
    assert t.starts_with("ban") == ["banana", "band", "bandana"]
    assert t.starts_with("z") == []
    assert t.starts_with("") == sorted(words)  # empty prefix = all words

    # count_prefix
    assert t.count_prefix("app") == 3  # app, apple, application
    assert t.count_prefix("a") == 4    # app, apple, application, apt
    assert t.count_prefix("ban") == 3  # band, bandana, banana
    assert t.count_prefix("banana") == 1
    assert t.count_prefix("z") == 0

    print("✅ All tests passed!")


if __name__ == "__main__":
    run_tests()
