You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Large-session fuzzy duplicate matching remains quadratic by row count

## Problem

`api.models._matching_visible_duplicate()` first checks exact visible-key identity, then falls back to scanning every existing key of the same role for substring / normalized fuzzy matches.

Current `master` already skips fuzzy work when either individual payload exceeds 200 KB, but the fallback remains quadratic when a transcript has thousands of ordinary-sized rows:

```text
for each candidate row:
    for each existing row of the same role:
        substring and normalized-content comparisons
```

A production-shaped compression sidecar that exposed this class contains 5,287 messages. Even with modest per-message content, the fallback can perform millions of comparisons while holding the Python GIL and delaying unrelated WebUI health/session endpoints.

This is independent of resident-cache byte budgeting (#6651), concurrent sidecar parsing (#7123), and compression-lineage pagination (#5776).

## Reproduction

Current `master` builds the fuzzy lookup for a non-exact candidate against 1,001 visible keys. A deterministic regression replaces the lookup builder with a sentinel and observes that the sentinel is reached.

## Expected behavior

- Exact visible-key equality remains authoritative at every transcript size.
- For normal/small transcripts, substring and normalized fuzzy recovery remain unchanged.
- Above a conservative visible-key threshold, non-exact candidates skip the O(n) fallback so end-to-end reconciliation cannot become O(n²).
- The threshold boundary is covered explicitly.

## Trade-off

A large transcript may retain an occasional near-duplicate whose visible key is not exactly equal. This is preferable to making the whole WebUI unresponsive. Exact duplicates continue to collapse, and the existing 200 KB per-message guard already establishes the same exact-only policy for a different large-input axis.

## Acceptance evidence

The regression must fail on current `master`, then pass with:

```text
1,001 keys + exact candidate: exact match returned
1,001 keys + fuzzy-only candidate: None, fuzzy lookup not built
1,000 keys + fuzzy-only candidate: existing fuzzy behavior preserved
small set + fuzzy-only candidate: existing fuzzy behavior preserved
```

## Non-goals

- No change to visible-key construction.
- No change to exact deduplication.
- No storage, API, or UI contract change.
- A future indexed fuzzy matcher could safely raise/remove the threshold without changing this issue's bounded-work requirement.

