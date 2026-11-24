You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

find-updates: resolve via source_resolver when present

Part of #1294 (Phase 8 of epic #1254). Branch: `new-resolver-config`.

## What needs to happen

Update `_find_newer_versions()` in `src/fromager/commands/find_updates.py`: it currently calls `overrides.find_and_invoke("get_resolver_provider", ...)` directly, so packages with `source:` config silently resolve through the legacy resolver. Use `sources.get_source_provider()` when `pbi.source_resolver` is present; fall back to the legacy path otherwise.

This is the one piece of #1294 with a live behavioral gap today.

## Tests

- `find-updates` for a new-config package resolves via the configured provider
- Legacy-config packages behave as before

## Notes

Independent of the other #1294 sub-issues; can be worked on in any order.
