# Analysis scripts (read-only over downloaded runs)

Each script takes one or more run directories (`karox6-bench-data/runs/<tag>`) and prints a
table. They read the gateway audit (`audit-*.jsonl`, the same counter for every arm), KaroX
session logs (`sessions/*/session.jsonl`, `karox6.jsonl`) and OpenCode's `opencode.txt`.
No model calls, nothing is written.

| script | question |
|---|---|
| `percall.py` | tokens, reasoning and latency per successful call, by arm |
| `pertask.py` | calls and reasoning per call for every task and arm |
| `stepcmp.py` | reasoning by kind of step (look / shell / edit / no tool call), KaroX vs OpenCode |
| `buckets.py` | reasoning per step by size of the tool arguments (same step, same thinking?) |
| `ctx.py` | what a step adds to the context: reasoning, text, arguments, tool results by tool |
| `replay.py` | does a CLI send reasoning back? (input growth regressed on reasoning tokens) |
| `traj.py` | context size along a run: peak, mean, drops (where a CLI compacts) |
| `peaks.py` | share of input tokens spent above 100k / 150k / 200k of context |
| `simcompact.py` | what a lower compaction threshold would have cost on recorded KaroX runs |
| `rbyctx.py` | reasoning and latency per call by context size |
| `cuts.py` | replies cut at the output limit: thinking-only cuts, streaks, cut-again rate |
| `ends.py` | how each KaroX run ended (status, steps, cuts, notices, reason) |
| `errs.py` | tool errors and tool time in KaroX runs |
| `lat.py` | latency percentiles and failed calls per arm |

`stepcmp.py`, `buckets.py`: run from this directory (buckets imports stepcmp's parsers).
