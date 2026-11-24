You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: 邮箱 name 字段含完整地址时，mail monitor 拼成 name@domain@domain 导致 AUTHENTICATIONFAILED（升级后老配置失效）

**TL;DR (EN)**
The mail monitor builds the IMAP login name as `f"{credential.name}@{credential.domain}"`, but an existing mailbox configured with the **full address in `name`** (e.g. `name="3855686217@qq.com"`, `domain="qq.com"`) produces `3855686217@qq.com@qq.com` → `[AUTHENTICATIONFAILED]` from the provider. The credential itself is valid.

---

### 环境

- QwenPaw `2.2.2.post1`（Docker）
- 邮箱：QQ 邮箱 `3855686217@qq.com`，IMAP/SMTP 已开启，授权码有效
- 该邮箱账号是 **2026-10-21 配置**的（`mail_state/3855686217_at_qq.com/` 建于 10-21 21:14）

### 现象

`qwenpaw.log` 自 **2026-10-22 18:09** 起持续报错，每 120 秒重试一次：

```
WARNING | qwenpaw/app/mail/monitor.py:1528 | mail monitor poll error for agent kTpb23;
retrying in 120s: b'[AUTHENTICATIONFAILED] Login fail. Account is abnormal, service is
not open, password is incorrect, login frequency limited, or system is busy.
More information at https://help.mail.qq.com/detail/108/1023'
```

### 排查结论（问题不在授权码，也不在邮箱服务商）

同一台机器、同一份凭据，直接用 Python 登录是**成功**的：

```
IMAP4_SSL("imap.qq.com", 993).login("3855686217@qq.com", <auth_code>)
→ ('OK', [b'Success login ok'])
→ INBOX: OK [b'529']
SMTP smtp.qq.com:465 → 认证通过
```

而用 monitor 自己拼出来的账号名登录，报的错误**与日志一字不差**：

```
login("3855686217@qq.com@qq.com", <auth_code>)
→ error b'[AUTHENTICATIONFAILED] Login fail. Account is abnormal, ...'
```

### 根因

`qwenpaw/app/mail/monitor.py:1096`：

```python
self.email_address = f"{credential.name}@{credential.domain}"
```

而 `agent.json` 里存的是：

```json
"mail": { "credential": { "name": "3855686217@qq.com", "domain": "qq.com", "provider": "" } }
```

`name` 里已经带了完整地址，于是拼成 `name@domain@domain`。
`pydantic` 的 `AgentMailCredential.name` 没有校验"不得包含 `@`"，`_validate_mail_config()` 也没拦，所以这种配置能一直存在并在启动时被原样使用。

时间点也对得上：10-21 配置时是旧语义（`name` 直接当账号），10-22 升级到 2.2.x 后 start building `name@domain`，老配置就全挂了。

### 另外一个连带坑（同一个字段）

`credentials.yaml` 的 `public.name` 参与身份比对：

```python
if record.public and record.public != _agent_mail_public_identity(mail):
    return mail      # 身份不一致就不注入 auth_code
```

把 `name` 从 `3855686217@qq.com` 改成 `3855686217` 时，如果 YAML 里没加引号写成 `name: 3855686217`，会被解析成 **int**，而 `agent.json` 里是 **str** → 比对失败 → `auth_code` 不注入 → MCP 报 `Missing required environment variables QWENPAWMAIL_EMAIL and/or QWENPAWMAIL_AUTH_CODE`，看起来像"凭据丢了"，其实还在。建议 `_agent_mail_public_identity()` 对 `name` 做 str 归一化，或不把纯数字字符串写进 YAML 时省略引号。

### 建议

1. `_validate_mail_config()` 增加校验：`name` 含 `@` 时要么报错、要么自动拆成 `name/domain`（对老配置做一次迁移最友好）；
2. 或者在 `monitor.py` 里防御：`if "@" in credential.name: email_address = credential.name`；
3. `_agent_mail_public_identity()` 里对 `name`/`domain` 做 `str()` 归一化，避免 int/str 比对失败；
4. 顺便：`public.name` 与 `agent.json` 不一致时目前是**静默跳过**（日志里没有任何提示），这类"凭据静默失效"很难排查，建议至少打一条 WARNING。

### 临时处理（我这边已生效）

`agent.json` → `mail.credential.name = "3855686217"`；`credentials.yaml` → `name: '3855686217'`（带引号）。之后：

```
INFO | mail/monitor.py:1207 | mail monitor started for agent kTpb23 (3855686217@qq.com, mode=agent_all)
```

报错归零，MCP `qwenpawmail` 也恢复正常。

