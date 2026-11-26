You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

PFlash default silently deletes the middle of every 2.3k-11.5k token prompt on Qwen3.5/3.6

Found by dogfooding a clean `pip install` of the 0.12.4 wheel:
`rapid-mlx serve qwen3.5-35b-8bit`, the documented command for the flagship
family.

## What

For prompts between roughly **2.3k and 11.5k tokens**, PFlash degenerates to
keeping only the endpoints and **silently discards the entire middle of the
prompt**. The client gets a normal `200`. The engine knows and says so — in
its own log, to nobody:

```
WARNING:rapid_mlx.pflash:PFlash endpoints-only: sink(256)+tail(2048) meet or
exceed the keep budget (2048) for a 4067-token prompt, so all 1763 middle
tokens are dropped and mid-document recall falls to ~0.
INFO:rapid_mlx.scheduler:[pflash] compressed 4067 -> 2304 tokens ratio=0.567
```

This is on by default: `pflash_tier=verified` for the Qwen3.5 / Qwen3.6
family resolves `--pflash` to `always`, so the naive serve command enables it.

## Measured

Needle-in-the-middle: a passphrase placed halfway through the conversation,
asked for at the end. Same model, same prompt, same machine — only `--pflash`
differs.

| prompt tokens | PFlash | compression | needle recalled |
|---|---|---|---|
| 4067 | default (`always`) | endpoints-only, ratio 0.567 | **NO** |
| 4067 | `--pflash off` | none | **YES** |
| 13419 | default (`always`) | real middle selection, ratio 0.200 | **YES** |

```
default : "I do not have access to a deployment passphrase from our conversation"
off     : "CORAL-WALRUS-7719"
```

## Why the range

`keep_budget = max(keep_ratio × n, min_keep_tokens)` = `max(0.20n, 2048)`, and
the endpoints are `sink + tail` = `256 + 2048` = **2304**.

The budget only exceeds the endpoints when `0.20n > 2304`, i.e. **n > 11520**.
Below that the budget can never fund a single middle block, so the middle is
dropped in full — which is exactly what the warning reports. Above it, real
block selection begins: at n=13419 the log shows `ratio=0.200` and no
endpoints-only warning, and recall returns.

So the defaults are self-consistent only for prompts over ~11.5k tokens. PR
#649 validated `keep_ratio=0.20` with "needle recall 5/5" — presumably in that
regime, where the mechanism works. The `always` default then applies it to a
regime where its own arithmetic degenerates.

`--pflash-threshold` (32768) does not protect here: its help text says
"Minimum prompt tokens before `--pflash auto` compresses", and this alias
defaults to `always`, not `auto`.

## Why it matters

2.3k–11.5k tokens is precisely where ordinary agent conversations live. A
Claude Code or Codex session crosses 2.3k within a few turns and stays under
11.5k for a long time — the whole window in which the middle of the
conversation is being silently deleted. The symptom is a model that
"forgets" what it was told a few turns ago, on our best-supported models, out
of the box, with nothing in the response to indicate anything was dropped.

## Suggested fix

Do not compress when compression cannot do its job. Concretely, skip PFlash
(or fall back to no-compression) whenever

```
max(keep_ratio × n, min_keep_tokens) <= sink_tokens + tail_tokens
```

i.e. require an effective minimum prompt of `(sink + tail) / keep_ratio`
(11 520 with today's defaults) before `always` engages. That is a strictly
better default than dropping the body: below the threshold the prompt is small
enough that prefill was never the bottleneck the compression exists to solve.

Secondary, and worth doing regardless:

* the endpoints-only condition should be an error or a refusal, not a
  `WARNING` in a log the caller never sees. Silently returning a truncated
  context as a normal `200` is the part that makes this hard to notice;
* `resolve_pflash_mode_default` should not promote an alias to `always`
  without checking that the configured budget can actually exceed the
  endpoints for the prompts that alias will realistically see.

