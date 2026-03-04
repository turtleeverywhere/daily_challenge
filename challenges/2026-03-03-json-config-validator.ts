/**
 * 🧩 Daily Challenge: 2026-03-03
 * Title: JSON Config Validator
 * Language: TypeScript
 * Difficulty: Beginner
 *
 * ## Problem
 *
 * You're building a tool that reads JSON configuration files. Before using the
 * config, you need to validate that it has the required fields with the correct
 * types.
 *
 * Write a function `validateConfig` that takes an unknown parsed JSON value and
 * checks whether it matches a given schema. The schema is a simple object
 * describing required keys and their expected types.
 *
 * Supported type strings: "string", "number", "boolean", "object", "array"
 *
 * The function should return an object with:
 *   - `valid`: boolean — whether the config passes all checks
 *   - `errors`: string[] — a list of human-readable error messages for each violation
 *
 * ## Examples
 *
 * ```ts
 * const schema: Schema = {
 *   host: "string",
 *   port: "number",
 *   debug: "boolean",
 * };
 *
 * validateConfig({ host: "localhost", port: 8080, debug: false }, schema);
 * // => { valid: true, errors: [] }
 *
 * validateConfig({ host: "localhost", port: "8080" }, schema);
 * // => {
 * //   valid: false,
 * //   errors: [
 * //     'Field "port" expected type "number" but got "string"',
 * //     'Missing required field "debug"',
 * //   ]
 * // }
 *
 * validateConfig("not an object", schema);
 * // => { valid: false, errors: ["Config must be a non-null object"] }
 *
 * const nestedSchema: Schema = { tags: "array", metadata: "object" };
 * validateConfig({ tags: ["a", "b"], metadata: { version: 1 } }, nestedSchema);
 * // => { valid: true, errors: [] }
 * ```
 *
 * ## Starter Template
 */

type TypeName = "string" | "number" | "boolean" | "object" | "array";
type Schema = Record<string, TypeName>;

interface ValidationResult {
  valid: boolean;
  errors: string[];
}

function validateConfig(config: unknown, schema: Schema): ValidationResult {
  // TODO: Implement this function
  // Step 1: Check that config is a non-null object (and not an array)
  // Step 2: For each key in the schema, check:
  //   - Does the key exist in config?
  //   - Does the value match the expected type?
  //   - Special case: "array" should use Array.isArray(), "object" should
  //     exclude arrays and null
  // Step 3: Collect all errors and return the result
  throw new Error("Not implemented");
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
//
// Hint 1: Use `typeof` for basic type checks. But remember:
//   typeof null === "object" and typeof [] === "object"
//   So you need special handling for "array" and "object".
//
// Hint 2: To check if a key exists on an unknown object, first
//   narrow the type to Record<string, unknown> then use `in` or
//   hasOwnProperty.
//
// Hint 3: A helper function like getTypeName(value: unknown): TypeName
//   can keep your code clean. It returns "array" for arrays,
//   "object" for plain objects, and typeof for the rest.
// ============================================================

// --- Tests (run with: npx ts-node 2026-03-03-json-config-validator.ts) ---

function runTests() {
  const schema: Schema = { host: "string", port: "number", debug: "boolean" };

  // Test 1: valid config
  const r1 = validateConfig({ host: "localhost", port: 8080, debug: false }, schema);
  console.assert(r1.valid === true, "Test 1 failed: should be valid");
  console.assert(r1.errors.length === 0, "Test 1 failed: should have no errors");

  // Test 2: wrong type + missing field
  const r2 = validateConfig({ host: "localhost", port: "8080" }, schema);
  console.assert(r2.valid === false, "Test 2 failed: should be invalid");
  console.assert(r2.errors.length === 2, `Test 2 failed: expected 2 errors, got ${r2.errors.length}`);

  // Test 3: not an object
  const r3 = validateConfig("not an object", schema);
  console.assert(r3.valid === false, "Test 3 failed: should be invalid");
  console.assert(r3.errors.length === 1, "Test 3 failed: should have 1 error");

  // Test 4: null input
  const r4 = validateConfig(null, schema);
  console.assert(r4.valid === false, "Test 4 failed: null should be invalid");

  // Test 5: array and object types
  const r5 = validateConfig(
    { tags: ["a", "b"], metadata: { v: 1 } },
    { tags: "array", metadata: "object" }
  );
  console.assert(r5.valid === true, "Test 5 failed: should be valid");

  // Test 6: array should not match "object" and vice versa
  const r6 = validateConfig(
    { tags: { a: 1 }, metadata: [1, 2] },
    { tags: "array", metadata: "object" }
  );
  console.assert(r6.valid === false, "Test 6 failed: swapped types should fail");

  // Test 7: extra fields are fine (we only check required ones)
  const r7 = validateConfig({ host: "x", port: 1, debug: true, extra: "ok" }, schema);
  console.assert(r7.valid === true, "Test 7 failed: extra fields should be allowed");

  console.log("All tests passed (or check assertions above)!");
}

runTests();
