// ============================================================
// 🧩 Daily Challenge: 2026-02-27
// 📝 Inventory Tracker
// 🟢 Difficulty: Beginner
// 🔧 Language: TypeScript
// ============================================================
//
// PROBLEM:
// Build a simple inventory tracker with these operations:
//
//   1. addItem(name, quantity, price) — add a new item or increase
//      quantity if it already exists (price updates to new value)
//   2. removeItem(name, quantity) — decrease quantity; remove entirely
//      if it drops to 0 or below. Return false if item doesn't exist.
//   3. getTotal() — return the total value of all inventory
//      (sum of quantity * price for each item)
//   4. getMostExpensive() — return the name of the item with the
//      highest per-unit price, or null if inventory is empty
//   5. lowStock(threshold) — return an array of item names where
//      quantity is at or below the threshold, sorted alphabetically
//
// EXAMPLES:
//
//   const inv = new InventoryTracker();
//   inv.addItem("apple", 50, 0.75);
//   inv.addItem("banana", 30, 1.25);
//   inv.addItem("apple", 10, 0.80);  // now 60 apples at $0.80
//
//   inv.getTotal();          // 60 * 0.80 + 30 * 1.25 = 85.50
//   inv.getMostExpensive();  // "banana"
//
//   inv.removeItem("banana", 25);
//   inv.lowStock(10);        // ["banana"]  (5 left)
//
//   inv.removeItem("banana", 10); // removes entirely (drops to -5 → removed)
//   inv.lowStock(10);        // []
//
// ============================================================

interface Item {
  quantity: number;
  price: number;
}

class InventoryTracker {
  private items: Map<string, Item>;

  constructor() {
    this.items = new Map();
  }

  addItem(name: string, quantity: number, price: number): void {
    // TODO: implement
  }

  removeItem(name: string, quantity: number): boolean {
    // TODO: implement
    return false;
  }

  getTotal(): number {
    // TODO: implement
    return 0;
  }

  getMostExpensive(): string | null {
    // TODO: implement
    return null;
  }

  lowStock(threshold: number): string[] {
    // TODO: implement
    return [];
  }
}

// ============================================================
// TESTS — run with: npx ts-node challenges/2026-02-27-inventory-tracker.ts
// or: npx tsx challenges/2026-02-27-inventory-tracker.ts
// ============================================================

function test() {
  const inv = new InventoryTracker();

  // Test addItem
  inv.addItem("apple", 50, 0.75);
  inv.addItem("banana", 30, 1.25);
  inv.addItem("cherry", 5, 3.00);
  inv.addItem("apple", 10, 0.80); // update: 60 apples at $0.80

  // Test getTotal
  const total = inv.getTotal();
  console.assert(
    Math.abs(total - (60 * 0.8 + 30 * 1.25 + 5 * 3.0)) < 0.001,
    `getTotal: expected 100.50, got ${total}`
  );

  // Test getMostExpensive
  console.assert(
    inv.getMostExpensive() === "cherry",
    `getMostExpensive: expected "cherry", got "${inv.getMostExpensive()}"`
  );

  // Test removeItem
  console.assert(inv.removeItem("banana", 25) === true, "removeItem should return true");
  console.assert(inv.removeItem("mango", 1) === false, "removeItem nonexistent should return false");

  // Test lowStock
  const low = inv.lowStock(10);
  console.assert(
    JSON.stringify(low) === JSON.stringify(["banana", "cherry"]),
    `lowStock: expected ["banana","cherry"], got ${JSON.stringify(low)}`
  );

  // Remove entirely
  inv.removeItem("banana", 100);
  const low2 = inv.lowStock(10);
  console.assert(
    JSON.stringify(low2) === JSON.stringify(["cherry"]),
    `lowStock after removal: expected ["cherry"], got ${JSON.stringify(low2)}`
  );

  // Empty inventory
  inv.removeItem("apple", 100);
  inv.removeItem("cherry", 100);
  console.assert(inv.getMostExpensive() === null, "getMostExpensive on empty should be null");
  console.assert(inv.getTotal() === 0, "getTotal on empty should be 0");

  console.log("✅ All tests passed!");
}

test();

// ============================================================
// 💡 HINTS (scroll down)
//
//
//
//
//
//
//
//
//
//
// Hint 1: Use Map.has() and Map.get() to check/retrieve items.
//
// Hint 2: For getTotal(), iterate with a for...of loop over
//         this.items.values() and accumulate quantity * price.
//
// Hint 3: For getMostExpensive(), iterate over this.items.entries()
//         and track the entry with the highest price.
//
// Hint 4: Array.from(this.items.entries()) lets you filter and
//         map over Map contents easily. Don't forget .sort()!
// ============================================================
