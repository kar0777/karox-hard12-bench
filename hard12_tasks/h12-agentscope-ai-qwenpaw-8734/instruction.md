You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: cloudpaw plugin fails to load on Chinese Windows (legacy_cloudpaw.py reads JSON without an explicit encoding)

## QwenPaw Version

2.3.0 (pip install). The same code is on `main` as of `f47dd19b`.

## Description

On Chinese Windows (system ANSI code page = `cp936` / GBK) the built-in `cloudpaw` plugin fails to load at all.

`src/qwenpaw/plugins/legacy_cloudpaw.py` reads three kinds of JSON file — the uninstall marker, `workspaces/<agent>/agent.json`, and the skill pool `skill.json` — with `Path.read_text()` and **no explicit `encoding`**, so Python falls back to the process locale encoding. QwenPaw itself writes those files as UTF-8, so any `agent.json` that contains CJK text raises `UnicodeDecodeError` while the loader imports the module, and the plugin is marked as failed.

`loader.py` reports this as a generic "plugin failed to load", so nothing in the message points at the code page and the user has no way to know why.

The file is inconsistent with itself: line 30 already pins `encoding="utf-8"`; seven other reads do not:

| Line | Expression | File read |
|-----:|------------|-----------|
| 83 | `json.loads(_marker().read_text())` | uninstall marker |
| 142 | `json.loads(path.read_text())` | uninstall marker |
| 159 | `json.loads(agent_file.read_text())` | `workspaces/<agent>/agent.json` |
| 182 | `json.loads(manifest.read_text())` | `<skill pool>/skill.json` |
| 240 | `json.loads(_marker().read_text())` | uninstall marker |
| 347 | `json.loads(profile_path.read_text())` | `workspaces/<agent>/agent.json` |
| 364 | `json.loads(manifest_path.read_text())` | `<skill pool>/skill.json` |

**Related PR(s):** opening right after this issue.

**Security considerations:** none — this is a decoding failure, not a disclosure.

## Component(s) Affected

- [x] Core / Backend (app, agents, config, providers, utils, local_models)
- [ ] Console (frontend web UI)
- [ ] Channels (DingTalk, Feishu, QQ, Discord, iMessage, etc.)
- [ ] Skills
- [ ] CLI
- [ ] Documentation (website)
- [ ] Tests
- [ ] CI/CD
- [ ] Scripts / Deploy

## Environment

- **QwenPaw version:** 2.3.0 (and `main` at `f47dd19b`)
- **OS:** Windows Server 2022 (AMD64); also seen on Windows 11
- **Install method:** pip
- **Python version (if applicable):** 3.12
- **Locale:** `locale.getencoding()` returns `cp936`

## Steps to Reproduce

1. Use Windows with a Chinese system locale, so `locale.getencoding()` returns `cp936`.
2. Have an agent whose `workspaces/<agent>/agent.json` contains CJK text. QwenPaw writes that file as UTF-8, so any Chinese agent name is enough.
3. Start QwenPaw and let the loader import `cloudpaw`.

The underlying mechanics, reproducible anywhere:

```python
import json
blob = json.dumps({"name": "药老"}, ensure_ascii=False).encode("utf-8")
blob.decode("gbk")   # UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 ...
```

## Actual vs Expected

- **Actual:** plugin load aborts and the plugin is marked failed; `cloudpaw` is unusable on every Chinese Windows install that has a CJK agent name.
- **Expected:** the plugin loads, because the JSON it reads was written by QwenPaw as UTF-8.

```
ERROR  plugin 'cloudpaw' failed to load
  File "...\qwenpaw\plugins\legacy_cloudpaw.py", line 159, in remember
    profile = json.loads(agent_file.read_text())
UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 137:
                     illegal multibyte sequence
```

## Logs / Screenshots

See the traceback above. `loader.py` surfaces only `plugin 'cloudpaw' failed to load` plus that traceback; the byte offset (`position 137`) lands in the middle of a multi-byte character that was valid UTF-8, which is the giveaway.

## Additional Notes

This cannot be caught by CI as it stands, and it is worth knowing why: `Path.read_text()` delegates to `io.open()`, which resolves `encoding=None` through the **C-level** locale encoding. Patching `locale.getencoding()` from Python does not change it, so a UTF-8 CI runner cannot be turned into a failing one by monkeypatching. A regression test therefore has to assert the encoding contract rather than depend on the locale — which is what the PR does.

Workarounds for affected users are all unpleasant: enable *Region → Administrative → Change system locale → Beta: Use Unicode UTF-8 for worldwide language support*, or strip non-ASCII characters out of `agent.json`.

