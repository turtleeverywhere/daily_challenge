// 🌡️ Daily Challenge: 2026-02-24
// Language: Rust | Difficulty: Beginner
//
// === Temperature Converter ===
//
// Build a temperature converter that can convert between Celsius, Fahrenheit,
// and Kelvin using Rust's type system.
//
// Requirements:
//   1. Define an enum `Temperature` with variants: Celsius(f64), Fahrenheit(f64), Kelvin(f64)
//   2. Implement a method `to_celsius(&self) -> f64`
//   3. Implement a method `to_fahrenheit(&self) -> f64`
//   4. Implement a method `to_kelvin(&self) -> f64`
//   5. Implement `std::fmt::Display` so it prints like "72.0°F" / "22.2°C" / "295.4K"
//   6. Implement a function `convert(temp: &Temperature, target: &str) -> Temperature`
//      that converts to the named scale ("C", "F", or "K").
//
// Formulas:
//   C = (F - 32) × 5/9
//   F = C × 9/5 + 32
//   K = C + 273.15
//
// Example:
//   let t = Temperature::Fahrenheit(212.0);
//   println!("{}", t);                        // "212.0°F"
//   println!("{:.1}", t.to_celsius());        // "100.0"
//   println!("{:.1}", t.to_kelvin());         // "373.1"
//
//   let t2 = convert(&t, "K");
//   println!("{}", t2);                       // "373.1K"
//
//   let freezing = Temperature::Celsius(0.0);
//   println!("{:.1}", freezing.to_fahrenheit()); // "32.0"
//
// Bonus:
//   - Implement FromStr so you can parse "100C" or "212F" or "373.15K"
//   - Handle invalid input gracefully with a custom error type

use std::fmt;

#[derive(Debug, Clone, Copy)]
enum Temperature {
    Celsius(f64),
    Fahrenheit(f64),
    Kelvin(f64),
}

impl Temperature {
    fn to_celsius(&self) -> f64 {
        todo!()
    }

    fn to_fahrenheit(&self) -> f64 {
        todo!()
    }

    fn to_kelvin(&self) -> f64 {
        todo!()
    }
}

impl fmt::Display for Temperature {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        todo!()
    }
}

fn convert(temp: &Temperature, target: &str) -> Temperature {
    todo!()
}

// Hint 1: Start with to_celsius — every conversion can go through Celsius as
//         an intermediate step, so to_fahrenheit can call self.to_celsius() first.

// Hint 2: For Display, match on the variant and use write!(f, "{:.1}°F", v) etc.
//         Note: Kelvin doesn't use a degree symbol — just "K".

// Hint 3: For the bonus FromStr, split the string at the last character to get
//         the numeric part and the unit. Use `f64::from_str` for parsing.

fn main() {
    // Test your implementation:
    let boiling = Temperature::Fahrenheit(212.0);
    println!("{} = {:.1}°C = {:.1}K", boiling, boiling.to_celsius(), boiling.to_kelvin());

    let freezing = Temperature::Celsius(0.0);
    println!("{} = {:.1}°F = {:.1}K", freezing, freezing.to_fahrenheit(), freezing.to_kelvin());

    let absolute_zero = Temperature::Kelvin(0.0);
    println!("{} = {:.1}°C = {:.1}°F", absolute_zero, absolute_zero.to_celsius(), absolute_zero.to_fahrenheit());

    let converted = convert(&boiling, "K");
    println!("Converted: {}", converted);
}
