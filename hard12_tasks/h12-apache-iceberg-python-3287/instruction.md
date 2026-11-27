You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

add_files(check_duplicate_files=True) is O(N²) across incremental backfill — predicate-pushdown into manifest scan

## Summary

`Table.add_files(file_paths, check_duplicate_files=True)` currently materializes every DataFile in the current snapshot via `inspect.data_files()` (full pyarrow Table including `readable_metrics`, per-column lower/upper bounds, partition records) and filters on `file_path` in memory. Per-call cost is O(snapshot data-file count); across an incremental backfill where each call adds K files, cumulative cost is O(N²).

Related but not the same:
- #2132 — same problem shape, closed as a docs-only fix (#2249) recommending `check_duplicate_files=False`. The algorithm was not changed.
- #2133 — parallelized the per-manifest fan-out and switched `inspect.files()` → `inspect.data_files()` (skips delete manifests). Constant-factor improvement only; per-call complexity unchanged.

This issue tracks the underlying algorithmic gap.

## Repro

Backfill a fresh table day-by-day, one `add_files` call per day, on the order of tens of thousands of parquet paths per call. Per-call wall-clock for the dup-check phase grows linearly with the cumulative file count of prior commits. After ~15 commits (~600k existing files), dup-check dominates — each new call takes ~10–15 minutes versus seconds during early commits.

Setting `check_duplicate_files=False` eliminates the cost but also loses the idempotency guarantee that re-running a partial-failure resume is safe.

## Suggested fix

Push the `file_paths` set into the manifest scan instead of materializing all DataFiles up front:

1. Get `ManifestFile` references from the current snapshot's manifest list.
2. Stream `ManifestEntry`s and short-circuit on `entry.data_file.file_path in candidate_set` (Python `set` containment is O(1)).
3. Skip decoding partition records / per-column stats — they're not needed for path-equality.

This makes dup-check streaming and roughly O(file_paths × pages_to_skim_until_match), independent of total snapshot size for negative cases and bounded by matching manifest size for positive cases.

Optional follow-up: store `file_path` lower/upper bounds in `ManifestFile` so most manifests can be pruned without opening — requires an Iceberg spec extension.

## Java reference

Spark's `add_files` action / `SnapshotProducer` does not pre-scan all data files for duplicate detection. Duplicate prevention there is predicate-based against the new paths only. The proposed pyiceberg fix would bring parity.

## Environment

- pyiceberg 0.11.x (and HEAD as of this writing — `pyiceberg/table/__init__.py:add_files`)
- `file_paths` is dispatched to `pyarrow.compute.field("file_path").isin(file_paths)` after a full materialization

## Willing to contribute

Happy to send a PR if maintainers agree on the manifest-scan approach. Wanted to align on direction first since #2132 was closed as docs.

