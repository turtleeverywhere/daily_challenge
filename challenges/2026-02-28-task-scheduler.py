"""
🧩 Daily Challenge: 2026-02-28
   Task Scheduler with Dependency Resolution

Language:   Python
Difficulty: Advanced
Time:       20–30 minutes

─── Problem ───────────────────────────────────────────────────────────

You're building a task scheduler for a build system. Each task has a name,
a duration (in seconds), and a list of dependencies (other task names that
must complete before it can start).

Implement a scheduler that:

1. Detects circular dependencies and raises an error.
2. Determines a valid execution order (topological sort).
3. Calculates the **minimum total build time** assuming unlimited
   parallelism — i.e., any tasks whose dependencies are all satisfied
   can run simultaneously.
4. Returns a "schedule": a list of (start_time, task_name) tuples,
   sorted by start_time then task_name.

─── Examples ──────────────────────────────────────────────────────────

tasks = {
    "compile":  {"duration": 5, "deps": ["parse"]},
    "parse":    {"duration": 3, "deps": ["lex"]},
    "lex":      {"duration": 2, "deps": []},
    "link":     {"duration": 4, "deps": ["compile", "resources"]},
    "resources":{"duration": 1, "deps": []},
    "test":     {"duration": 6, "deps": ["link"]},
}

schedule, total_time = solve(tasks)

# Expected total_time: 20
#   lex starts at 0, finishes at 2
#   parse starts at 2, finishes at 5
#   resources starts at 0, finishes at 1
#   compile starts at 5, finishes at 10
#   link starts at 10, finishes at 14
#   test starts at 14, finishes at 20

# Expected schedule:
# [(0, "lex"), (0, "resources"), (2, "parse"), (5, "compile"), (10, "link"), (14, "test")]

─── Circular dependency example ───────────────────────────────────────

tasks_circular = {
    "a": {"duration": 1, "deps": ["b"]},
    "b": {"duration": 1, "deps": ["c"]},
    "c": {"duration": 1, "deps": ["a"]},
}
# Should raise ValueError("Circular dependency detected")

─── Starter Template ──────────────────────────────────────────────────
"""

from __future__ import annotations
from typing import Any


def solve(tasks: dict[str, dict[str, Any]]) -> tuple[list[tuple[int, str]], int]:
    """
    Resolve task dependencies and compute a parallel schedule.

    Args:
        tasks: mapping of task_name -> {"duration": int, "deps": [str, ...]}

    Returns:
        (schedule, total_time) where schedule is a sorted list of
        (start_time, task_name) tuples and total_time is the minimum
        wall-clock time to complete all tasks with unlimited parallelism.

    Raises:
        ValueError: if a circular dependency is detected.
    """
    # TODO: Implement me!
    #
    # Hint 1 (approach):
    #   Use Kahn's algorithm (BFS-based topological sort) to detect cycles
    #   and determine execution order. Track in-degree counts for each node.
    #
    # Hint 2 (parallelism / critical path):
    #   For each task, its earliest start time is:
    #     max(dep_start + dep_duration for dep in dependencies)
    #   Tasks with no deps start at time 0. The total build time is
    #   max(start + duration) across all tasks. This is the "critical path."
    #
    # Hint 3 (data structures):
    #   - collections.deque for BFS queue
    #   - dict for in-degrees, adjacency list, and earliest-start times
    pass


# ─── Tests ───────────────────────────────────────────────────────────

def test_basic():
    tasks = {
        "compile":   {"duration": 5, "deps": ["parse"]},
        "parse":     {"duration": 3, "deps": ["lex"]},
        "lex":       {"duration": 2, "deps": []},
        "link":      {"duration": 4, "deps": ["compile", "resources"]},
        "resources": {"duration": 1, "deps": []},
        "test":      {"duration": 6, "deps": ["link"]},
    }
    schedule, total_time = solve(tasks)
    assert total_time == 20, f"Expected 20, got {total_time}"
    assert schedule == [
        (0, "lex"), (0, "resources"), (2, "parse"),
        (5, "compile"), (10, "link"), (14, "test"),
    ], f"Unexpected schedule: {schedule}"
    print("✅ test_basic passed")


def test_circular():
    tasks = {
        "a": {"duration": 1, "deps": ["b"]},
        "b": {"duration": 1, "deps": ["c"]},
        "c": {"duration": 1, "deps": ["a"]},
    }
    try:
        solve(tasks)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "ircular" in str(e)
    print("✅ test_circular passed")


def test_independent():
    """All tasks independent — everything starts at 0."""
    tasks = {
        "a": {"duration": 3, "deps": []},
        "b": {"duration": 5, "deps": []},
        "c": {"duration": 2, "deps": []},
    }
    schedule, total_time = solve(tasks)
    assert total_time == 5
    assert all(t == 0 for t, _ in schedule)
    print("✅ test_independent passed")


def test_diamond():
    """Diamond dependency: A -> B,C -> D."""
    tasks = {
        "d": {"duration": 1, "deps": ["b", "c"]},
        "b": {"duration": 3, "deps": ["a"]},
        "c": {"duration": 2, "deps": ["a"]},
        "a": {"duration": 1, "deps": []},
    }
    schedule, total_time = solve(tasks)
    # a:0-1, b:1-4, c:1-3, d:4-5
    assert total_time == 5
    print("✅ test_diamond passed")


if __name__ == "__main__":
    test_basic()
    test_circular()
    test_independent()
    test_diamond()
    print("\n🎉 All tests passed!")
