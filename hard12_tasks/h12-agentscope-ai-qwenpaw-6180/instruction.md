You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: 更新2.x版本后，会话列表updatedAt数据未更新

## QwenPaw Version

[Provide the version of QwenPaw you are using, e.g. 0.x.x or git commit hash.]
[Using `qwenpaw --version` in your command line or checking the version in the console UI can help.]

2.0.0

## Description

[Describe the bug clearly and concisely. What happened vs what you expected?]

版本更新后，会话中发送消息后，updatedAt时间应该更新为最新时间，但当前的会话列表中数据时间未更新

**Related PR(s):** #(optional)

**Security considerations:** [If applicable, e.g. auth, env/config exposure]

## Component(s) Affected

- [ ] Core / Backend (app, agents, config, providers, utils, local_models)
- [ ] Console (frontend web UI)
- [ ] Channels (DingTalk, Feishu, QQ, Discord, iMessage, etc.)
- [ ] Skills
- [ ] CLI
- [ ] Documentation (website)
- [ ] Tests
- [ ] CI/CD
- [ ] Scripts / Deploy

## Environment

- **QwenPaw version:** [e.g. 0.x.x or git commit]
- **OS:** [e.g. macOS 14, Ubuntu 22.04, Windows 11]
- **Install method:** [pip / one-line install / Docker / from source]
- **Python version (if applicable):** [e.g. 3.10]

## Steps to Reproduce

1. 终端或者企业微信通道，发送消息给智能体
2. 智能体正常回答响应，会话详情中，消息最新时间为当前时间
3. 点击会话，查看活跃会话列表，列表未发生变化，updatedAt字段未更新为最新时间

## Actual vs Expected

- **Actual:**
- **Expected:**

## Logs / Screenshots

[Paste relevant log output or attach screenshots. Use code blocks for logs.]

```
(paste logs here)
```

## Additional Notes

[Optional: workarounds, similar issues, etc.]

