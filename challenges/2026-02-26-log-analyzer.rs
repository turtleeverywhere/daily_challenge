// 🧩 Daily Challenge: 2026-02-26
// Language: Rust | Difficulty: Intermediate
//
// === Log Analyzer ===
//
// You're given a vector of log entries, each as a string in the format:
//   "YYYY-MM-DD HH:MM:SS [LEVEL] message"
//
// Example:
//   "2026-02-26 07:00:00 [ERROR] disk full"
//   "2026-02-26 07:01:23 [WARN] high memory usage"
//   "2026-02-26 07:02:00 [ERROR] connection timeout"
//   "2026-02-26 07:03:45 [INFO] request handled"
//   "2026-02-26 07:04:00 [WARN] slow query detected"
//   "2026-02-26 07:05:12 [ERROR] disk full"
//
// Implement a function that returns a LogReport containing:
//   1. counts: a HashMap<String, usize> mapping each log level to its count
//   2. most_common_error: the most frequently occurring ERROR message (or None if no errors)
//   3. timeline: a Vec<(String, usize)> of (hour, count) pairs sorted by hour,
//      showing how many log entries occurred in each hour
//
// Example output for the above input:
//   counts: {"ERROR": 3, "WARN": 2, "INFO": 1}
//   most_common_error: Some("disk full")
//   timeline: [("07", 6)]
//
// ─── Starter Template ───────────────────────────────────────────────

use std::collections::HashMap;

#[derive(Debug, PartialEq)]
struct LogReport {
    counts: HashMap<String, usize>,
    most_common_error: Option<String>,
    timeline: Vec<(String, usize)>,
}

fn analyze_logs(entries: &[&str]) -> LogReport {
    // TODO: Implement this function
    //
    // Hint 1: Use str::find() or split() to extract the level between [ and ]
    // Hint 2: entry[11..13] gives you the hour from the timestamp
    // Hint 3: HashMap::entry() with .or_insert(0) is your friend for counting
    // Hint 4: For most_common_error, keep a separate HashMap of error messages
    //         and use .iter().max_by_key() to find the winner
    // Hint 5: Collect timeline into a Vec and sort by the hour string

    todo!()
}

fn main() {
    let logs = vec![
        "2026-02-26 07:00:00 [ERROR] disk full",
        "2026-02-26 07:01:23 [WARN] high memory usage",
        "2026-02-26 07:02:00 [ERROR] connection timeout",
        "2026-02-26 08:03:45 [INFO] request handled",
        "2026-02-26 08:04:00 [WARN] slow query detected",
        "2026-02-26 09:05:12 [ERROR] disk full",
        "2026-02-26 09:10:00 [INFO] cache cleared",
        "2026-02-26 09:15:30 [ERROR] disk full",
    ];

    let report = analyze_logs(&logs);

    println!("Level counts:");
    for (level, count) in &report.counts {
        println!("  {}: {}", level, count);
    }
    println!("Most common error: {:?}", report.most_common_error);
    println!("Timeline:");
    for (hour, count) in &report.timeline {
        println!("  {}:xx → {} entries", hour, count);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic() {
        let logs = vec![
            "2026-02-26 07:00:00 [ERROR] disk full",
            "2026-02-26 07:01:23 [WARN] high memory usage",
            "2026-02-26 08:02:00 [ERROR] connection timeout",
            "2026-02-26 08:03:45 [INFO] request handled",
        ];
        let report = analyze_logs(&logs);
        assert_eq!(report.counts.get("ERROR"), Some(&2));
        assert_eq!(report.counts.get("WARN"), Some(&1));
        assert_eq!(report.counts.get("INFO"), Some(&1));
        assert_eq!(report.most_common_error, Some("disk full".to_string()));
        assert_eq!(report.timeline, vec![("07".to_string(), 2), ("08".to_string(), 2)]);
    }

    #[test]
    fn test_no_errors() {
        let logs = vec![
            "2026-02-26 10:00:00 [INFO] started",
            "2026-02-26 10:05:00 [WARN] slow",
        ];
        let report = analyze_logs(&logs);
        assert_eq!(report.most_common_error, None);
    }

    #[test]
    fn test_empty() {
        let report = analyze_logs(&[]);
        assert!(report.counts.is_empty());
        assert_eq!(report.most_common_error, None);
        assert!(report.timeline.is_empty());
    }

    #[test]
    fn test_tie_breaking() {
        // When error messages tie, either is acceptable
        let logs = vec![
            "2026-02-26 07:00:00 [ERROR] alpha",
            "2026-02-26 07:01:00 [ERROR] beta",
        ];
        let report = analyze_logs(&logs);
        assert!(
            report.most_common_error == Some("alpha".to_string())
                || report.most_common_error == Some("beta".to_string())
        );
    }
}
