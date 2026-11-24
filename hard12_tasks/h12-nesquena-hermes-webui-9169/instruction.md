You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Disk full (ENOSPC) surfaces as a generic "Internal server error" when sending a message

> AI usage: investigated and written with Anthropic Claude (`claude-opus-5-5`) through Claude Code, on the account holder's instructions; the account holder reviewed it before posting.

**What happens.** When the filesystem that holds the WebUI state is full, sending a message fails with HTTP 500 `{"error": "Internal server error"}`, and the chat shows "Error: Internal server error". The log has the real cause (`OSError: [Errno 28] No space left on device`), but the user has no way to know that storage is full, or that freeing space fixes it (it does, without a restart).

**Repro** (stock `ghcr.io/nesquena/hermes-webui:latest`, 0.52.697 `382da96b5c`):
1. Run the WebUI with `HERMES_WEBUI_STATE_DIR` on a small tmpfs (`--tmpfs /home/hermeswebui/.hermes/webui:size=20m`), log in and create a session.
2. Fill it: `dd if=/dev/zero of=/home/hermeswebui/.hermes/webui/fill.bin bs=1M`.
3. Then:
   - `POST /api/chat/start` → 500 `{"error": "Internal server error"}`
   - `POST /api/session/draft` → 500 `{"error": "Internal server error"}`
   - log: `[webui] ERROR POST /api/chat/start … OSError: [Errno 28] No space left on device`

**Where.** The request handlers in `server.py` (the `except Exception` branch in both the GET and the write paths) map every unhandled exception to the same generic 500.

**Proposal.** Catch `OSError` with `errno.ENOSPC` (and `errno.EDQUOT`) before the generic branch and return a specific, actionable error, for example HTTP 507 `{"error": "Storage is full. Free up space and try again."}`, so the chat shows it. Happy to send a small PR with a test.

**Context.** We hit this in per-user containers with a disk quota: once the quota fills, the assistant only shows "Internal server error", and deleting a file restores it.

