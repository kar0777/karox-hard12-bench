You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: OpenAI-compatible gateway bare APIError with real status only in message text (`status_code=502, ...`) is classified as `unknown` — no retry, no model fallback

## English summary

When an OpenAI-compatible gateway/relay fails mid-stream, the OpenAI SDK raises a **bare `openai.APIError`** (no `status_code`, no `response`) whose only status hint is plain text like:

```
status_code=502, 请联系管理员处理！ (request id: ...)
```

`extract_status_code()` only recognizes the narrow `"Streaming response failed: [5xx]"` message format, so this error is classified as `unknown` by `classify_model_error()` → **neither same-model retry nor cross-model fallback fires**, and the whole turn/cron job dies. A genuine HTTP 502 from the same gateway WOULD be `transient` and fallback-eligible, so identical upstream failures behave inconsistently depending only on how the gateway wraps them.

Observed in production today: 3 scheduled agent jobs (07:30 / 08:00 / 09:30) all failed with no fallback, no message delivered. Reproduced against `classify_model_error` with the exact logged exceptions (see below).

Suggestion: extend `error_utils.extract_status_code()` to also recognize `status_code=5xx`-style patterns in gateway messages (keep it narrow, e.g. `\bstatus_code\s*=\s*([1-5]\d{2})\b`), or treat bare `openai.APIError` with a `5xx` in the message as transient. Related but distinct from #8092 (that one is about content-inspection text being misclassified as `bad_request`; this one is about status extraction missing a gateway message format).

## 环境 / Environment

- QwenPaw 2.2.2.post1（Docker `agentscope/qwenpaw:latest`），Debian 13 宿主机
- 模型走 OpenAI 兼容中转网关（relay），主模型 `deepseek-v4.1-flash`，已配置 `fallback_models`（zhipu-cn / glm-5.3-flash），`fallback_policy.enabled=true`

## 现象 / What happened

2026-10-30 早上三个 cron 任务（07:30 备份上云、08:00 早报、09:30 巡检）准点触发（日志有 `cron execute`），但全部失败，备用模型一次都没被尝试，飞书一条消息都没发出：

```
07:30:30 ERROR runtime: unhandled error ...: Error code: 400 - {'error': {'message': 'status_code=400, 请联系管理员处理！', 'type': 'upstream_error', 'code': 'bad_response_status_code'}}
08:00:12 ERROR runtime: unhandled error ...: Error code: 400 - {'error': {'message': 'status_code=400, 请联系管理员处理！', 'type': 'upstream_error', 'code': 'bad_response_status_code'}}
09:30:40 ERROR runtime: unhandled error ...: APIError('status_code=502, 请联系管理员处理！ (request id: ...)')
```

## 复现 / Reproduction

用日志里的**原始异常形态**直接喂 `classify_model_error()`（QwenPaw 2.2.2.post1 自带实现）：

```python
import openai
from qwenpaw.providers.model_error_policy import classify_model_error

class FakeRequest: method='POST'; url='http://x/v1/chat/completions'; headers={}
class FakeResp:
    status_code = 400
    headers = {}
    request = FakeRequest()

# 形态 A：网关把上游故障包装成 HTTP 400 + type=upstream_error
e1 = openai.BadRequestError(
    message="Error code: 400 - {'error': {'message': 'status_code=400, 请联系管理员处理！', 'type': 'upstream_error', 'code': 'bad_response_status_code'}}",
    response=FakeResp(), body=None)

# 形态 B：流中失败，SDK 抛裸 APIError，真实状态码只在消息文本里
e2 = openai.APIError(
    message='status_code=502, 请联系管理员处理！ (request id: ...)',
    request=FakeRequest(), body=None)

print(classify_model_error(e1))  # kind=bad_request  retryable=False fallback_eligible=False
print(classify_model_error(e2))  # kind=unknown      retryable=False fallback_eligible=False
```

实测输出：

```
08:00  400 upstream_error: 分类=bad_request  可重试=False  会切备用=False
09:30  裸APIError 502: 分类=unknown  可重试=False  会切备用=False
```

## 期望 / Expected

- **形态 B（本 issue 核心）**：`status_code=502` 明明白白写在消息里，应被 `extract_status_code()` 提取出来并归类为 `transient` → 可重试、可切换备用模型。
- **形态 A（顺带讨论）**：`type=upstream_error` + `bad_response_status_code` 表明是网关上游故障而非请求本身问题，但被包装成 HTTP 400 后按现有设计判为 `bad_request`（不 fallback）。这个可以理解设计初衷（400 通常意味着请求有问题），但网关把 5xx 包装成 400 是常见行为，`upstream_error` 这个 type 是否值得加入 transient 判定，请作者权衡。

## 源码位置 / Source

- `qwenpaw/providers/model_error_policy.py`：`fallback_eligible = retryable or kind == "model_not_found"`，`unknown`/`bad_request` 均不在内
- `qwenpaw/providers/error_utils.py`：`_STREAMING_ERROR_STATUS_RE` 只匹配 `Streaming response failed: [5xx]` 这一种文本格式，注释里也写明"keep this fallback deliberately narrow"

同类参考：#8092（阿里网关审核文本被误分类为 bad_request，同属"网关非标准错误形态导致分类失真"家族）、#8124（已修：审核错误路由到 fallback）。

谢谢！

