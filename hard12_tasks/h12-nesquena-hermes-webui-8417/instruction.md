You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Insights: Cache % is capped at 50% for WebUI sessions (cache reads counted twice)

## Summary

The **Insights → Models** card's Cache column can never exceed 50% for WebUI sessions, so a ~98% prompt-cache hit rate shows as 49%. Rows that mix WebUI and CLI sessions land somewhere between 50% and the true rate.

## Cause

`_handle_insights` (`api/routes.py`) merges two sources whose `input_tokens` mean different things:

| Source | `input_tokens` |
|---|---|
| WebUI session JSON | full prompt = uncached + cache read + cache write |
| `state.db` CLI rows (`source != 'webui'`) | uncached input only |

Example, one session: WebUI JSON `input_tokens` = 21,143,626 = 36,522 uncached + 20,703,305 read + 403,799 write; the same session's `state.db` row has `input_tokens` = 36,522.

The rates are then computed as

```python
prompt_cache_hit_percent(row_cache_read, stats["input_tokens"] + row_cache_read)   # per model
prompt_cache_hit_percent(total_cache_read_tokens, total_input_tokens + total_cache_read_tokens)  # total
```

For WebUI rows that's `read / (uncached + write + 2·read)`, which is ≤ 50%. `prompt_cache_hit_percent`'s own docstring says `prompt_tokens` must already include cache reads and writes. The daily-chart tooltip in `static/panels.js` has the same `input + cacheRead` denominator.

## Observed (30-day window)

| model | panel | actual |
|---|---|---|
| model A (468 sessions, mixed) | 76% | 95% |
| model B (39 sessions) | 49% | 96% |
| Claude Opus (6 sessions) | 49% | 98% |
| llama.cpp model (2 sessions) | 50% | 98% |

## Suggested fix

Normalise CLI rows to the full-prompt convention, then divide once:

1. CLI query: also select `COALESCE(cache_write_tokens, 0)`; use `input_tokens + cache_read_tokens + cache_write_tokens` as the row's input.
2. Per-model / total: `prompt_cache_hit_percent(read, input)`.
3. `static/panels.js` daily tooltip: `cacheDenom = input`.

As a side effect, the Tokens column for CLI rows then includes cache tokens, matching WebUI rows. We're carrying this as a build-time patch downstream and will drop it once this is fixed here.

