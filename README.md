# KaroX HARD12 bench (GitHub Actions)

12 fresh tasks (upstream PRs/issues created after 2026-10-18, after the
DeepSeek-V4.1-Flash-1017 checkpoint), three coding CLIs on the same model, the
same W&B gateway profile and the same Harbor sandbox (agent network = docker
bridge only):

| arm | what runs |
|---|---|
| `karox5` | KaroX 5 runtime wheel in `wheels/` |
| `opencode_v2` | `@opencode/cli@2.2.7` |
| `deepseek_harness` | `@deepseek-ai/dsh@0.2.2-rc.1` |

Run: Actions -> **hard12** -> Run workflow (arms, tasks, attempts, tag). One
job per task x arm, attempts run in parallel inside the job; the `report` job
re-grades every trial uniformly and writes `HARD12_RESULTS.md` to the run
summary.

Needs one repository secret: `WANDB_API_KEY` (passed only to the litellm
gateway process). Grading: `scripts/hard12_report.py` (F2P must pass, P2P must
not regress; P2P failing in every trial of a task is excluded as environment).
