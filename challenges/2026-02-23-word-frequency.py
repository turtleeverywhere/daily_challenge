"""
Daily Challenge: 2026-02-23
Language: Python | Difficulty: Beginner

# Word Frequency Counter

Write a function that takes a string of text and returns a dictionary mapping
each word to its frequency count. Words should be compared case-insensitively,
and punctuation should be stripped from word boundaries.

## Rules
- Words are separated by whitespace
- Strip leading/trailing punctuation from each word (.,!?;:'"-())
- Comparisons are case-insensitive; return lowercase keys
- Empty strings return an empty dict

## Examples

>>> word_frequency("Hello world hello")
{'hello': 2, 'world': 1}

>>> word_frequency("It's a test. A simple test!")
{"it's": 1, 'a': 2, 'test': 2, 'simple': 1}

>>> word_frequency("  Wow!  Wow...  WOW  ")
{'wow': 3}

>>> word_frequency("")
{}

## Bonus
Return results sorted by frequency (descending), breaking ties alphabetically.
"""

import string


def word_frequency(text: str) -> dict[str, int]:
    """Return a dict mapping each lowercase word to its frequency."""
    # YOUR CODE HERE
    pass


def word_frequency_sorted(text: str) -> list[tuple[str, int]]:
    """Bonus: Return list of (word, count) sorted by count desc, then word asc."""
    # YOUR CODE HERE
    pass


# --- Hints (read only if stuck!) ---
# Hint 1: str.split() with no args splits on any whitespace and ignores empties
# Hint 2: str.strip(chars) removes leading/trailing chars from a string
# Hint 3: For sorting, look at sorted() with a key function returning a tuple


# --- Test harness ---
if __name__ == "__main__":
    tests = [
        ("Hello world hello", {"hello": 2, "world": 1}),
        ("It's a test. A simple test!", {"it's": 1, "a": 2, "test": 2, "simple": 1}),
        ("  Wow!  Wow...  WOW  ", {"wow": 3}),
        ("", {}),
        ("one", {"one": 1}),
    ]

    print("Running tests...")
    for i, (inp, expected) in enumerate(tests, 1):
        result = word_frequency(inp)
        status = "✅" if result == expected else "❌"
        print(f"  Test {i}: {status}")
        if result != expected:
            print(f"    Input:    {inp!r}")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")

    print("\nDone! All tests should show ✅")
