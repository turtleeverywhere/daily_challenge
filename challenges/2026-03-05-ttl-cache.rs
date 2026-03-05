// 🧩 Daily Challenge: 2026-03-05
// Language: Rust | Difficulty: Intermediate
//
// TTL Cache — A Key-Value Store with Expiring Entries
// ===================================================
//
// Build a generic in-memory cache where each entry expires after a
// configurable time-to-live (TTL). This is the backbone of rate limiters,
// DNS caches, and session stores.
//
// Requirements:
//   1. `TtlCache::new(default_ttl: Duration)` — create a cache with a default TTL.
//   2. `insert(key, value)` — store a value that expires after default_ttl.
//   3. `insert_with_ttl(key, value, ttl)` — store a value with a custom TTL.
//   4. `get(&key) -> Option<&V>` — retrieve a value if it hasn't expired.
//   5. `remove(&key) -> Option<V>` — explicitly remove an entry.
//   6. `cleanup()` — remove all expired entries (lazy eviction).
//   7. `len()` — return the count of non-expired entries.
//
// Example:
//   let mut cache = TtlCache::new(Duration::from_secs(5));
//   cache.insert("session_a", "user_42");
//   assert_eq!(cache.get(&"session_a"), Some(&"user_42"));
//   // ... 6 seconds later ...
//   assert_eq!(cache.get(&"session_a"), None);
//
// Stretch goals (optional):
//   - Make it thread-safe with Arc<Mutex<...>> or RwLock
//   - Add a `get_or_insert_with(key, f)` method
//   - Track hit/miss stats
//
// Run:  rustc 2026-03-05-ttl-cache.rs && ./2026-03-05-ttl-cache
// Test: the main() function includes assertions to verify your implementation.

use std::collections::HashMap;
use std::hash::Hash;
use std::time::{Duration, Instant};

// ── Your implementation ─────────────────────────────────────────────

struct CacheEntry<V> {
    value: V,
    expires_at: Instant,
}

struct TtlCache<K, V> {
    entries: HashMap<K, CacheEntry<V>>,
    default_ttl: Duration,
}

impl<K: Eq + Hash, V> TtlCache<K, V> {
    fn new(default_ttl: Duration) -> Self {
        // TODO: initialize the cache
        todo!()
    }

    fn insert(&mut self, key: K, value: V) {
        // TODO: insert with default TTL
        todo!()
    }

    fn insert_with_ttl(&mut self, key: K, value: V, ttl: Duration) {
        // TODO: insert with custom TTL
        todo!()
    }

    fn get(&self, key: &K) -> Option<&V> {
        // TODO: return Some(&value) only if the entry exists AND hasn't expired
        todo!()
    }

    fn remove(&mut self, key: &K) -> Option<V> {
        // TODO: remove and return the value (even if expired)
        todo!()
    }

    fn cleanup(&mut self) {
        // TODO: remove all entries whose expires_at is in the past
        // Hint: HashMap::retain is your friend
        todo!()
    }

    fn len(&self) -> usize {
        // TODO: count only non-expired entries
        todo!()
    }
}

// ── Hints (try solving first!) ──────────────────────────────────────
//
// Hint 1: `Instant::now() + duration` gives you the expiration time.
//
// Hint 2: For `get`, compare `entry.expires_at` against `Instant::now()`.
//         Return None if now >= expires_at.
//
// Hint 3: `cleanup` can use `self.entries.retain(|_, entry| entry.expires_at > Instant::now())`
//
// Hint 4: `len` should NOT count expired entries. You can either call
//         cleanup first, or filter with `.values().filter(...)`.count().

// ── Tests ───────────────────────────────────────────────────────────

fn main() {
    // Basic insert + get
    let mut cache = TtlCache::new(Duration::from_secs(60));
    cache.insert("key1", "value1");
    cache.insert("key2", "value2");
    assert_eq!(cache.get(&"key1"), Some(&"value1"));
    assert_eq!(cache.get(&"key2"), Some(&"value2"));
    assert_eq!(cache.len(), 2);
    println!("✅ Basic insert + get works");

    // Custom TTL (very short — already expired by the time we check)
    cache.insert_with_ttl("ephemeral", "gone", Duration::from_nanos(1));
    std::thread::sleep(Duration::from_millis(1));
    assert_eq!(cache.get(&"ephemeral"), None);
    println!("✅ Custom short TTL correctly expires");

    // len should not count expired entries
    assert_eq!(cache.len(), 2); // "ephemeral" is expired
    println!("✅ len() excludes expired entries");

    // cleanup removes expired entries from the map
    cache.cleanup();
    assert_eq!(cache.entries.len(), 2); // only non-expired remain in storage
    println!("✅ cleanup() evicts expired entries");

    // remove
    let removed = cache.remove(&"key1");
    assert_eq!(removed, Some("value1"));
    assert_eq!(cache.get(&"key1"), None);
    assert_eq!(cache.len(), 1);
    println!("✅ remove() works");

    // Overwrite
    cache.insert("key2", "updated");
    assert_eq!(cache.get(&"key2"), Some(&"updated"));
    println!("✅ Overwrite works");

    // Missing key
    assert_eq!(cache.get(&"nonexistent"), None);
    println!("✅ Missing key returns None");

    println!("\n🎉 All tests passed!");
}
