"""Solution for 2026-03-04 — Trie Autocomplete"""

from __future__ import annotations


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False
        self.prefix_count: int = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        node.prefix_count += 1
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.prefix_count += 1
        node.is_end = True

    def _find_node(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> list[str]:
        node = self._find_node(prefix)
        if node is None:
            return []
        results: list[str] = []
        self._collect(node, prefix, results)
        return results  # already sorted via sorted traversal

    def _collect(self, node: TrieNode, current: str, results: list[str]) -> None:
        if node.is_end:
            results.append(current)
        for ch in sorted(node.children):
            self._collect(node.children[ch], current + ch, results)

    def count_prefix(self, prefix: str) -> int:
        node = self._find_node(prefix)
        return node.prefix_count if node else 0

    def delete(self, word: str) -> bool:
        """Bonus: delete a word and adjust prefix counts."""
        if not self.search(word):
            return False
        node = self.root
        node.prefix_count -= 1
        for ch in word:
            node = node.children[ch]
            node.prefix_count -= 1
        node.is_end = False
        return True


def run_tests():
    t = Trie()
    words = ["apple", "app", "application", "apt", "banana", "band", "bandana"]
    for w in words:
        t.insert(w)

    assert t.search("app") is True
    assert t.search("apple") is True
    assert t.search("ap") is False
    assert t.search("banz") is False

    assert t.starts_with("app") == ["app", "apple", "application"]
    assert t.starts_with("ban") == ["banana", "band", "bandana"]
    assert t.starts_with("z") == []
    assert t.starts_with("") == sorted(words)

    assert t.count_prefix("app") == 3
    assert t.count_prefix("a") == 4
    assert t.count_prefix("ban") == 3
    assert t.count_prefix("banana") == 1
    assert t.count_prefix("z") == 0

    # Bonus: delete
    assert t.delete("app") is True
    assert t.search("app") is False
    assert t.count_prefix("app") == 2  # apple, application
    assert t.delete("nonexistent") is False

    print("✅ All tests passed!")


if __name__ == "__main__":
    run_tests()
