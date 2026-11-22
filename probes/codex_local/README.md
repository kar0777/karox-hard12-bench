# Codex CLI through the bench gateway, without a model or a key

`run.sh <bench repo> <work dir> [strict]` starts a mock chat-completions upstream
(`mock_chat.py`, logs every request body), the bench gateway (litellm with
`gateway/race_audit.py` and the ReformBoss config, upstream swapped for the mock) and
Codex CLI 0.171.0 with the arm's config, for one prompt that needs one shell call.
It shows what the gateway sends upstream for the `codex` arm and what the audit
records. With `strict` the mock refuses unknown fields, roles and tool types, as a
plain chat upstream does. Needs `litellm` as a uv tool, node and npx; nothing leaves
the machine except the download of the Codex package. Used on 2026-11-22 to find
why ReformBoss refused the bridged request (KaroX `PROGRESS.md`, devc2 and devc3).
