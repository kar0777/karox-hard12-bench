You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

robots.txt enforcement fails OPEN for 2nd+ concurrent same-host request (RobotsTxtMiddleware + Twisted Deferred.asFuture())

## What happened

With `ROBOTSTXT_OBEY=True`, a path disallowed by robots.txt was fetched (HTTP 200) instead of being blocked — but only when it was the **2nd or later concurrent request to the same host**. Reproduced 4/4 runs, deterministically.

**Versions:** Scrapy 2.19, Python 3.12 (Twisted as bundled with the Scrapy 2.19 install — exact version available on request).

## Reproduction

1. Serve a local test site (`python -m http.server`) with robots.txt containing:
```
User-agent: *
Disallow: /private/
```
2. Run a spider with `ROBOTSTXT_OBEY=True`, `DOWNLOAD_DELAY=1.0`, `CONCURRENT_REQUESTS_PER_DOMAIN=1`, AutoThrottle enabled, honest User-Agent, requesting three URLs on that host: a live page, a 404, and `/private/x.html`.
3. Observe: `/private/x.html` returns 200 and reaches the parse callback instead of being filtered by the robots middleware.

## Root cause (instrumented)

Concurrent same-host requests share a single Twisted `Deferred` for the robots.txt fetch/parse inside `RobotsTxtMiddleware`. The middleware converts that Deferred per-waiter via `Deferred.asFuture()` — and Twisted's `asFuture()` delivers the real result to the **first** future and **`None`** to the second. The second waiter therefore gets `parser=None`, and `process_request_2` treats `None` as "no parser available → allow the request."

So robots.txt enforcement **silently fails open** for every concurrent same-host request after the first, on the very first robots.txt fetch for a host.

## Expected behavior

All waiters on the shared robots.txt Deferred should receive the parsed result (or all should fail closed — block the request — if the parse result is unavailable).

## Suggested fix directions

- Share the *parsed* result (not the raw Deferred) across waiters; or
- Fail closed: treat `parser=None` as "deny" rather than "allow" in `process_request_2`.

## Workaround

Serialize same-host requests so two requests never race the first robots.txt fetch of a host (e.g. `CONCURRENT_REQUESTS_PER_DOMAIN=1` plus a per-host delay), or pre-fetch robots.txt before crawling.

## Why this matters

Fail-open robots.txt enforcement is a compliance footgun: users who set `ROBOTSTXT_OBEY=True` believe disallowed paths are never fetched. Under concurrency, that guarantee silently breaks.

---
*Found while building a polite liveness-checker that deliberately serializes per-host requests; the serialization accidentally immunized us, which is how the race was isolated. Happy to provide the minimal spider + test server scripts.*
