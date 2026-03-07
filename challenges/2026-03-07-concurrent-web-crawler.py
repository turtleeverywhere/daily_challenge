"""
🧩 Daily Challenge: 2026-03-07
Language: Python
Difficulty: Advanced

# Concurrent Web Crawler Simulator

Build a concurrent web crawler that traverses a simulated web graph using
asyncio, respecting a maximum concurrency limit and detecting cycles.

## Problem

You are given a "web graph" as a dictionary mapping URLs to their linked pages.
Implement an async crawler that:

1. Starts from a given root URL
2. "Fetches" each page (simulated with an async function that has a small delay)
3. Discovers and crawls all linked pages (BFS order)
4. Respects a maximum concurrency limit (at most N pages fetched simultaneously)
5. Never visits the same URL twice
6. Returns a CrawlResult with:
   - `visited`: list of URLs in the order they were fully processed
   - `edges`: list of (source, target) tuples for all discovered links
   - `unreachable`: set of URLs in the graph that were never reached

## Example

    graph = {
        "https://a.com": ["https://b.com", "https://c.com"],
        "https://b.com": ["https://d.com", "https://a.com"],  # cycle back to a
        "https://c.com": ["https://d.com"],
        "https://d.com": [],
        "https://orphan.com": ["https://a.com"],  # not reachable from a.com
    }

    result = await crawl("https://a.com", graph, max_concurrency=2, fetch_delay=0.01)

    # result.visited contains a.com, b.com, c.com, d.com (BFS order, but
    #   exact order of b/c may vary due to concurrency)
    assert "https://a.com" in result.visited
    assert "https://orphan.com" not in result.visited
    assert "https://orphan.com" in result.unreachable
    assert ("https://b.com", "https://a.com") in result.edges  # even cyclic edges recorded
    assert len(result.visited) == 4

## Constraints

- Use asyncio.Semaphore for concurrency limiting
- Use asyncio.Queue for the BFS frontier
- The fetch simulation must use `await asyncio.sleep(fetch_delay)`
- Thread-safe tracking of visited URLs (use a set guarded by the event loop)
- Handle the case where a URL in a link list doesn't exist in the graph
  (treat it as a page with no outgoing links)

## Starter Template
"""

import asyncio
from dataclasses import dataclass, field


@dataclass
class CrawlResult:
    visited: list[str] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)
    unreachable: set[str] = field(default_factory=set)


async def fetch_page(url: str, graph: dict[str, list[str]], delay: float) -> list[str]:
    """Simulate fetching a page. Returns list of linked URLs."""
    await asyncio.sleep(delay)
    return graph.get(url, [])


async def crawl(
    root: str,
    graph: dict[str, list[str]],
    max_concurrency: int = 3,
    fetch_delay: float = 0.05,
) -> CrawlResult:
    """
    Crawl the web graph starting from root using BFS with bounded concurrency.

    TODO: Implement this function.

    Hints:
    - Create an asyncio.Semaphore(max_concurrency)
    - Create an asyncio.Queue and seed it with the root URL
    - Track visited URLs in a set
    - Spawn worker coroutines that pull from the queue
    - Each worker: acquire semaphore, fetch page, record edges, enqueue new URLs
    - Use queue.task_done() and queue.join() to know when crawling is complete
    """
    raise NotImplementedError("Implement the crawler!")


# ---------------------------------------------------------------------------
# Hints (scroll down)
#
#
#
#
#
#
#
#
#
#
# Hint 1: Structure your worker loop like this:
#   while True:
#       url = await queue.get()
#       try:
#           async with semaphore:
#               links = await fetch_page(url, graph, fetch_delay)
#               ...process links...
#       finally:
#           queue.task_done()
#
# Hint 2: To avoid race conditions when checking/adding to visited,
#   do the check-and-add BEFORE putting into the queue (since we're
#   single-threaded in asyncio, the check-then-add is atomic between awaits).
#
# Hint 3: Use asyncio.create_task to spawn multiple workers, then
#   await queue.join() to wait for completion, then cancel workers.
#
# Hint 4: For unreachable, it's simply: all_urls - visited
#   where all_urls = set(graph.keys())
# ---------------------------------------------------------------------------


# === Test Suite ===
async def test_crawler():
    graph = {
        "https://a.com": ["https://b.com", "https://c.com"],
        "https://b.com": ["https://d.com", "https://a.com"],
        "https://c.com": ["https://d.com"],
        "https://d.com": [],
        "https://orphan.com": ["https://a.com"],
    }

    result = await crawl("https://a.com", graph, max_concurrency=2, fetch_delay=0.01)

    assert len(result.visited) == 4, f"Expected 4 visited, got {len(result.visited)}"
    assert "https://a.com" in result.visited
    assert "https://orphan.com" not in result.visited
    assert "https://orphan.com" in result.unreachable
    assert ("https://b.com", "https://a.com") in result.edges

    # Test with unknown links
    graph2 = {
        "https://start.com": ["https://missing.com"],
    }
    result2 = await crawl("https://start.com", graph2, max_concurrency=1, fetch_delay=0.01)
    assert "https://start.com" in result2.visited
    assert "https://missing.com" in result2.visited  # visited even though not in graph

    # Test single node
    result3 = await crawl("https://solo.com", {"https://solo.com": []}, max_concurrency=5, fetch_delay=0.01)
    assert result3.visited == ["https://solo.com"]
    assert result3.edges == []

    # Test concurrency is actually limited (timing-based)
    large_graph = {"https://root.com": [f"https://p{i}.com" for i in range(10)]}
    for i in range(10):
        large_graph[f"https://p{i}.com"] = []

    import time
    start = time.monotonic()
    result4 = await crawl("https://root.com", large_graph, max_concurrency=2, fetch_delay=0.1)
    elapsed = time.monotonic() - start
    # 11 pages, 2 at a time, 0.1s each → at least 0.5s (ceil(11/2)*0.1 = 0.6)
    # If unlimited concurrency, would be ~0.1s
    assert elapsed > 0.4, f"Concurrency not limited? Took only {elapsed:.2f}s"
    assert len(result4.visited) == 11

    print("✅ All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_crawler())
