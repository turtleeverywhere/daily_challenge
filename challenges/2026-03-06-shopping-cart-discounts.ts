// ============================================================
// 🧩 Daily Challenge: 2026-03-06
// Shopping Cart Discount Calculator (TypeScript - Beginner)
// ============================================================
//
// PROBLEM:
// Build a function that calculates the final price of a shopping cart
// after applying discount rules. The cart contains items, and discounts
// can be percentage-based or fixed-amount, applied per-item or cart-wide.
//
// Each item has: { name: string, price: number, quantity: number, category: string }
//
// Discount rules (applied in order):
//   1. "buy2get1" — for items with quantity >= 3, every 3rd item is free
//   2. "category"  — a percentage off all items in a specific category
//   3. "cart"      — a fixed amount off the total (but total can't go below 0)
//
// EXAMPLES:
//
//   const cart: CartItem[] = [
//     { name: "T-Shirt", price: 25, quantity: 3, category: "clothing" },
//     { name: "Jeans",   price: 60, quantity: 1, category: "clothing" },
//     { name: "Book",    price: 15, quantity: 2, category: "books" },
//   ];
//
//   const discounts: Discount[] = [
//     { type: "buy2get1" },
//     { type: "category", category: "books", percent: 10 },
//     { type: "cart", amount: 5 },
//   ];
//
//   calculateTotal(cart, discounts)
//   // Step 1: T-Shirt 3 qty → pay for 2 = 50. Jeans = 60. Book = 30. Subtotal = 140
//   // Step 2: Books 10% off → 30 * 0.10 = 3 off → Subtotal = 137
//   // Step 3: Cart $5 off → 132
//   // → 132
//
//   Another example:
//   calculateTotal(
//     [{ name: "Sticker", price: 2, quantity: 1, category: "misc" }],
//     [{ type: "cart", amount: 10 }]
//   )
//   // Sticker = 2, cart discount 10 → clamped to 0
//   // → 0
//
// ============================================================

interface CartItem {
  name: string;
  price: number;
  quantity: number;
  category: string;
}

interface Buy2Get1Discount {
  type: "buy2get1";
}

interface CategoryDiscount {
  type: "category";
  category: string;
  percent: number;
}

interface CartDiscount {
  type: "cart";
  amount: number;
}

type Discount = Buy2Get1Discount | CategoryDiscount | CartDiscount;

function calculateTotal(cart: CartItem[], discounts: Discount[]): number {
  // TODO: Implement this!
  // Process each discount type in the order they appear.
  // Return the final total rounded to 2 decimal places.
  return 0;
}

// ============================================================
// HINTS (scroll down)
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
//
// Hint 1: Start by computing a "line total" for each item (price * quantity).
//         Store these in a Map<string, { category: string; lineTotal: number }>
//         so discounts can modify them.
//
// Hint 2: For buy2get1, the number of free items = Math.floor(quantity / 3).
//         Subtract (freeItems * price) from that item's line total.
//
// Hint 3: For category discounts, loop through your map and reduce
//         line totals for matching categories by the percentage.
//
// Hint 4: Use Math.max(0, total - amount) for the cart discount.
//
// Hint 5: Round at the end: Math.round(total * 100) / 100
// ============================================================

// --- Tests ---
function test() {
  const cart1: CartItem[] = [
    { name: "T-Shirt", price: 25, quantity: 3, category: "clothing" },
    { name: "Jeans", price: 60, quantity: 1, category: "clothing" },
    { name: "Book", price: 15, quantity: 2, category: "books" },
  ];
  const discounts1: Discount[] = [
    { type: "buy2get1" },
    { type: "category", category: "books", percent: 10 },
    { type: "cart", amount: 5 },
  ];
  console.assert(calculateTotal(cart1, discounts1) === 132, "Test 1 failed");

  const cart2: CartItem[] = [
    { name: "Sticker", price: 2, quantity: 1, category: "misc" },
  ];
  console.assert(
    calculateTotal(cart2, [{ type: "cart", amount: 10 }]) === 0,
    "Test 2 failed"
  );

  const cart3: CartItem[] = [
    { name: "Pen", price: 3, quantity: 7, category: "office" },
  ];
  console.assert(
    calculateTotal(cart3, [{ type: "buy2get1" }]) === 15,
    "Test 3 failed"
  );

  const cart4: CartItem[] = [
    { name: "Hat", price: 20, quantity: 2, category: "clothing" },
  ];
  console.assert(calculateTotal(cart4, []) === 40, "Test 4 failed");

  const cart5: CartItem[] = [
    { name: "Novel", price: 10, quantity: 4, category: "books" },
    { name: "Coat", price: 100, quantity: 1, category: "clothing" },
  ];
  const discounts5: Discount[] = [
    { type: "buy2get1" },
    { type: "category", category: "books", percent: 20 },
    { type: "category", category: "clothing", percent: 50 },
  ];
  console.assert(calculateTotal(cart5, discounts5) === 74, "Test 5 failed");

  console.log("All tests passed! ✅");
}

test();
