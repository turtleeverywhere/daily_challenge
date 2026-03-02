// 🧩 Daily Challenge: 2026-03-02
// Language: Rust | Difficulty: Beginner
//
// ## Markdown Link Extractor
//
// Write a function that extracts all markdown-style links from a string
// and returns them as a vector of (text, url) tuples.
//
// Markdown links look like: [link text](https://example.com)
//
// Rules:
// - Extract ALL links found in the input string
// - Preserve the link text and URL exactly as written
// - Ignore malformed links (mismatched brackets/parens)
// - Nested brackets are NOT expected (keep it simple)
//
// ## Examples
//
// Input:  "Check out [Rust](https://rust-lang.org) and [Cargo](https://doc.rust-lang.org/cargo/)!"
// Output: [("Rust", "https://rust-lang.org"), ("Cargo", "https://doc.rust-lang.org/cargo/")]
//
// Input:  "No links here, just [broken( stuff"
// Output: []
//
// Input:  "[A](url1) text [B](url2)"
// Output: [("A", "url1"), ("B", "url2")]
//
// ## Hints (ROT13 — decode if stuck)
//
// Hint 1: Hfr `punef()` naq `crrxnoyr()` be whfg vgrengr guebhtu punenpgref
//         jvgu n fgngr znpuvar nccebnpu (ybpx sbe '[', gura ']', gura '(', gura ')').
//
// Hint 2: `Fgevat::svaq` naq fyvprf jbex, ohg n fvzcyr fgngr-onfrq cnefre
//         vf pyrnarfg. Genpx lbhe cbfvgvba nf lbh fpna.
//
// Hint 3: Pbafvqre ohvyqvat hc `grkg` naq `hey` jvgu `Fgevat::arj()`
//         naq chfuvat gb erfhygf jura lbh svaq gur pybfvat ')'.

fn extract_links(input: &str) -> Vec<(&str, &str)> {
    // TODO: Implement this!
    // Return a Vec of (link_text, url) borrowed from the input string.
    todo!()
}

fn main() {
    let text = "Check out [Rust](https://rust-lang.org) and [Cargo](https://doc.rust-lang.org/cargo/)!";
    let links = extract_links(text);
    for (text, url) in &links {
        println!("{} -> {}", text, url);
    }
    assert_eq!(links.len(), 2);
    assert_eq!(links[0], ("Rust", "https://rust-lang.org"));
    assert_eq!(links[1], ("Cargo", "https://doc.rust-lang.org/cargo/"));

    // Edge cases
    assert_eq!(extract_links("no links here"), Vec::<(&str, &str)>::new());
    assert_eq!(extract_links("[broken( stuff"), Vec::<(&str, &str)>::new());
    assert_eq!(
        extract_links("[A](url1) middle [B](url2)"),
        vec![("A", "url1"), ("B", "url2")]
    );
    assert_eq!(extract_links("[no-url]"), Vec::<(&str, &str)>::new());
    assert_eq!(extract_links("](url)"), Vec::<(&str, &str)>::new());

    println!("All tests passed! 🎉");
}
