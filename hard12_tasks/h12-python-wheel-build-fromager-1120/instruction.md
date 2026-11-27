You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Fail fast on GitHub API rate limit instead of hanging for 25+ minutes

## Problem

When the GitHub API rate limit is hit, `RetryHTTPAdapter._handle_github_rate_limit()` in `src/fromager/http_retry.py` caps wait time at 300s per retry. With the default config (`FROMAGER_HTTP_RETRIES=8`), this means up to 8 retries × 300s = **~40 minute hang** before failing.

In CI, multiple parallel jobs share one IP, quickly exhausting the 60 req/hr unauthenticated limit. The actual reset is ~3600s away, but the 300s cap means the code sleeps, retries, hits the same 403, and repeats.

## Proposed Solution

- Add `GitHubRateLimitError(RequestException)` exception
- In `_handle_github_rate_limit()`: when wait time exceeds a threshold (e.g. 120s), **raise immediately** with an actionable message suggesting `GITHUB_TOKEN`
- Keep existing sleep-and-retry for short waits
- Exclude `GitHubRateLimitError` from `RETRYABLE_EXCEPTIONS` so `@retry_on_exception` on `_find_tags` won't swallow it

## Context

PR #1117 passes `GITHUB_TOKEN` to CI but tokens aren't available for fork PRs. This ensures fork PR CI fails fast with a clear message instead of hanging.

Ref: https://github.com/python-wheel-build/fromager/actions/runs/25432530885/job/74602126392?pr=1115

## Files

- `src/fromager/http_retry.py`
- `tests/test_http_retry.py`
