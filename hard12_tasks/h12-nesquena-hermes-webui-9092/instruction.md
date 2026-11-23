You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`/goal` stores contract lines as plain goal text, and `/goal gate add` replaces the goal

## Problem

WebUI's `/goal` handler sets any non-control text as the goal verbatim. It doesn't parse Hermes Agent's inline completion-contract fields and has no `gate` subcommand. Two consequences, both reproduced on unmodified `master` [`7ea9607`](https://github.com/nesquena/hermes-webui/commit/7ea9607aab6e3b45fa421b33d5e336292c9087fd):

1. **Contract lines are not parsed.** In the CLI, TUI and messaging gateways, `outcome:`, `verification:`, `constraints:`, `boundaries:` and `stop when:` lines become the goal's completion contract. The judge then uses its contract prompt, which requires concrete evidence for the verification criterion and treats a violated constraint as not done. In WebUI the same text is stored as one plain goal with an empty contract, so the judge uses the free-form prompt and reads the contract as ordinary text. The judge truncates the goal to 2,000 characters, so on longer prompts it never sees the later contract lines.
2. **`/goal gate add <command>` replaces the goal.** WebUI treats it as new goal text: the active goal becomes the literal string `gate add <command>`, no gate is added, and a turn is kicked off with that string as the prompt.

## Where

- [`api/goals.py:619`](https://github.com/nesquena/hermes-webui/blob/7ea9607aab6e3b45fa421b33d5e336292c9087fd/api/goals.py#L619): `goal_command_payload` calls `mgr.set(text)` with the raw text. Only `status|pause|resume|clear|stop|done` are recognized before that.
- Hermes Agent's shared handler does both: [`hermes_cli/goals.py:312`](https://github.com/NousResearch/hermes-agent/blob/4c11aea4511123159785d5422e2dbba3867a4756/hermes_cli/goals.py#L312) `parse_contract` splits the headline from the contract fields, and [`hermes_cli/goal_command.py:118`](https://github.com/NousResearch/hermes-agent/blob/4c11aea4511123159785d5422e2dbba3867a4756/hermes_cli/goal_command.py#L118) handles `gate`.

## Reproduction

Against unmodified `master` `7ea9607`, with Hermes Agent `fbf6c6c` and a throwaway `HERMES_HOME`, calling `api.goals.goal_command_payload` directly:

```text
1. /goal with contract lines via WebUI
   stored goal: 'Ship the export endpoint\noutcome: GET /export returns CSV fo...' (320 chars)
   stored contract: {'outcome': '', 'verification': '', 'constraints': '', 'boundaries': '', 'stop_when': ''}
   Hermes Agent parse_contract on the same text: headline 'Ship the export endpoint' | contract fields set: ['outcome', 'verification', 'constraints', 'boundaries', 'stop_when']
2. /goal gate add <command> via WebUI
   action: set | kickoff_prompt: 'gate add uv run pytest tests/test_export.py'
   stored goal: 'gate add uv run pytest tests/test_export.py' | gates: []
```

The goal text used for case 1:

```text
Ship the export endpoint
outcome: GET /export returns CSV for every active account
verification: uv run pytest tests/test_export.py passes and the response shows a CSV header
constraints: existing export tests stay unchanged
boundaries: api/export.py and tests/test_export.py only
stop when: the schema needs a migration
```

This calls the API function rather than going through the browser, so it shows what the handler stores, not anything about the UI.

## Suggested fix shape

- **Contract parsing (small):** split the text with Hermes Agent's `parse_contract` before `mgr.set(...)`, passing the headline and a non-empty contract, as `hermes_cli.goal_command._set` does. Recognizing a leading `gate` would also stop a gate command from replacing the goal.
- **Gates (needs a decision):** a gate is a shell command the server reruns after every turn with no later approval. Hermes Agent's handler requires the adapter to explicitly authorize `gate add` ([`goal_command.py:126-129`](https://github.com/NousResearch/hermes-agent/blob/4c11aea4511123159785d5422e2dbba3867a4756/hermes_cli/goal_command.py#L126-L129)), so WebUI needs a rule for who may add gates before it supports them. Until then, refusing `gate …` with a clear message would beat silently replacing the goal.

## Related

- #8716 (`/goal draft` and `/goal show`) routes `draft` through Hermes Agent's handler. It explicitly leaves inline contract fields and `/goal gate` out of scope, and drops the native "tighten any field by re-setting the goal with inline lines" hint because WebUI doesn't parse them. This issue covers that gap.

