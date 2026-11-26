You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Feature]: make application log rotation limits configurable

## Problem

The application log handler always rotates `qwenpaw.log` at 5 MiB and keeps three backups. Those defaults are reasonable for desktop use, but they cannot be adjusted for long-running servers, containers with strict disk budgets, or short-lived debug sessions.

Operators currently have to patch `qwenpaw.utils.logging` to change either limit.

## Proposal

Add two environment variables while keeping the current defaults:

- `QWENPAW_LOG_MAX_SIZE`: maximum active log size, accepting byte counts and common suffixes such as `512K`, `10MB`, and `1GiB`
- `QWENPAW_LOG_MAX_BACKUPS`: number of rotated backups to retain; `0` disables backups

Invalid or negative values should fall back to the existing defaults with a warning rather than preventing startup. The resolved values should be passed to the existing safe rotating file handler.

Document both variables in the English and Chinese configuration reference and add focused parser/handler tests.
