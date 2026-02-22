// ============================================================================
// Daily Challenge: 2026-02-22 [Rust] — Arena Allocator
// Difficulty: Advanced (Sunday)
// Estimated time: 20–30 minutes
// ============================================================================
//
// PROBLEM
// -------
// Implement a simple typed arena allocator. An arena allocates objects in bulk
// (in "chunks") and hands out references with the arena's lifetime. All memory
// is freed at once when the arena is dropped — no per-object deallocation.
//
// Your arena should support:
//   1. `new()`          — create an empty arena (first chunk allocated on first alloc)
//   2. `alloc(value)`   — move a value into the arena, return `&T`
//   3. `alloc_with(f)`  — allocate using a closure `FnOnce() -> T`, return `&T`
//   4. `len()`          — number of objects allocated so far
//
// The arena must:
//   - Return references that live as long as the arena (`&self -> &T`).
//   - Grow by allocating new chunks (don't reallocate/move old data).
//   - Work for any `Sized` type `T`.
//
// CONSTRAINTS
// -----------
// - Do NOT use `unsafe` in your solution — use `Vec<Box<[MaybeUninit<T>]>>`
//   or a similar safe approach. (Bonus: try an unsafe version after!)
// - Chunk size: start at 8 and double each time (8, 16, 32, …).
//
// EXAMPLES
// --------
//   let arena = Arena::<String>::new();
//   let a = arena.alloc("hello".to_string());   // &String
//   let b = arena.alloc("world".to_string());
//   assert_eq!(a, "hello");
//   assert_eq!(b, "world");
//   assert_eq!(arena.len(), 2);
//
//   // References remain valid even after more allocations:
//   for i in 0..100 {
//       arena.alloc(format!("item-{i}"));
//   }
//   assert_eq!(a, "hello");  // still valid!
//   assert_eq!(arena.len(), 102);
//
// HINTS (read if stuck)
// ---------------------
// Hint 1: You can't return `&T` from `&self` if T is inside a `Vec` that may
//         reallocate. Solution: store chunks as `Vec<Vec<T>>` and only push to
//         the current chunk. When full, push a *new* Vec — old references stay
//         valid because each inner Vec is a separate heap allocation.
//
// Hint 2: To return `&T` with the arena's lifetime from `&self`, you'll need
//         interior mutability. Use `RefCell<ArenaInner<T>>` or `Cell`-based
//         indexing. Alternatively, take `&self` and use `Cell<usize>` for the
//         cursor and pre-allocate each chunk to capacity with a safe pattern.
//
// Hint 3: A clean safe approach:
//         - Store `chunks: RefCell<Vec<Vec<T>>>` and `len: Cell<usize>`.
//         - In `alloc`, borrow_mut the chunks, push to last vec; if full,
//           create a new vec with doubled capacity.
//         - To return `&T` from `&self`: after pushing, get a raw pointer to
//           the last element, then... you DO need one tiny unsafe for the
//           lifetime cast. Or use a `typed_arena`-like Cell trick.
//
//         Actually, the simplest fully-safe version: store `Vec<Box<T>>`.
//         Each Box is a stable pointer. Then `alloc` pushes a Box and returns
//         `&**box`. This works with RefCell but costs per-object allocation.
//         For the real chunked version, one `unsafe` is hard to avoid — and
//         that's the learning point! Try both approaches.
//
// ============================================================================

use std::cell::{Cell, RefCell};

const INITIAL_CHUNK_SIZE: usize = 8;

/// A typed arena allocator.
pub struct Arena<T> {
    // TODO: choose your internal representation
    _marker: std::marker::PhantomData<T>,
}

impl<T> Arena<T> {
    /// Create a new, empty arena.
    pub fn new() -> Self {
        todo!()
    }

    /// Allocate a value in the arena, returning a reference that lives as
    /// long as the arena itself.
    pub fn alloc(&self, value: T) -> &T {
        todo!()
    }

    /// Allocate a value produced by the closure.
    pub fn alloc_with<F: FnOnce() -> T>(&self, f: F) -> &T {
        self.alloc(f())
    }

    /// Number of objects currently in the arena.
    pub fn len(&self) -> usize {
        todo!()
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
}

// ============================================================================
// Tests — all should pass when your implementation is correct.
// Run with: cargo test --bin arena_allocator (or rustc + run)
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_alloc() {
        let arena = Arena::<i32>::new();
        let a = arena.alloc(42);
        assert_eq!(*a, 42);
        assert_eq!(arena.len(), 1);
    }

    #[test]
    fn test_references_stable_across_growth() {
        let arena = Arena::<String>::new();
        let first = arena.alloc("first".into());

        // Force multiple chunk growths
        for i in 0..200 {
            arena.alloc(format!("item-{i}"));
        }

        // Original reference must still be valid
        assert_eq!(first, "first");
        assert_eq!(arena.len(), 201);
    }

    #[test]
    fn test_alloc_with() {
        let arena = Arena::<Vec<u8>>::new();
        let v = arena.alloc_with(|| vec![1, 2, 3]);
        assert_eq!(v, &[1, 2, 3]);
    }

    #[test]
    fn test_empty() {
        let arena = Arena::<()>::new();
        assert!(arena.is_empty());
        arena.alloc(());
        assert!(!arena.is_empty());
    }

    #[test]
    fn test_drop_runs() {
        use std::sync::atomic::{AtomicUsize, Ordering};
        static COUNT: AtomicUsize = AtomicUsize::new(0);

        struct Loud;
        impl Drop for Loud {
            fn drop(&mut self) {
                COUNT.fetch_add(1, Ordering::SeqCst);
            }
        }

        COUNT.store(0, Ordering::SeqCst);
        {
            let arena = Arena::<Loud>::new();
            for _ in 0..50 {
                arena.alloc(Loud);
            }
        }
        assert_eq!(COUNT.load(Ordering::SeqCst), 50);
    }
}

fn main() {
    let arena = Arena::<String>::new();
    let greeting = arena.alloc("Hello, Arena!".to_string());
    println!("{greeting}");
    println!("Arena has {} items", arena.len());
}
