You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug] Tool-returned image/PDF binary sent as bare base64 ("type":"data") triggers 400 "file must have a file_id or file_data"

> This issue was drafted with the assistance of an AI agent (**deepseek-v4-flash-vision-exp**).
> 本 issue 由 AI agent（**deepseek-v4-flash-vision-exp**）代笔。

## Summary

When an **agent tool returns an image or PDF binary** (e.g. `send_file_to_user`, `view_image`, or any tool whose result carries base64 media), QwenPaw serializes it into the model request as a bare `{"type": "data", "data": "<base64>"}` content part — **without a `data:<mime>;base64,` URI prefix**. Providers that lint content parts (e.g. DeepSeek's OpenAI-compatible endpoint) reject it with:

```
openai.BadRequestError: Error code: 400 - {'error': {'message': 'file must have a file_id or file_data', ...}}
```

The user-visible error is a generic `claw internal error` / `internal error`, masking the real cause.

## Environment

- **QwenPaw**: 2.2.0 (python3.13, Debian)
- **Provider**: DeepSeek OpenAI-compatible chat completions endpoint, vision model
- **Channel**: console / `default` agent
- **Trigger**: agent invokes a tool that returns an image/PDF; the tool result binary is injected into the message history

## Repro

1. Configure a DeepSeek vision model as the active model.
2. Send the agent a request that causes it to use a tool whose result contains an image or PDF (e.g. `send_file_to_user` a PDF, `view_image` a local file, or any tool returning base64 media).
3. The agent tries to call the model again with the tool result in context.

**Actual**: `400 BadRequestError: file must have a file_id or file_data`.

## Diagnosis

The error occurs at `messages[43]`. Dumping the failing request shows the offending content part(s):

```json
{
  "type": "data",
  "data": "iVBORw0KGgoAAAANSUhEUgAA...",   // PNG magic bytes, bare base64
  ...
}
```

A failing request contains **10** such `{"type": "data", "data": "<base64>"}` parts. Critically:

- No `data:` MIME prefix (it is *not* `data:image/png;base64,...`).
- No `image_url` wrapper.
- No `media_type` field.

The same builder correctly emits `data:image/png;base64,` in the image-probe path (`openai_provider.py` `_probe_image_support`), so this is a **missed path in tool-result / message serialization**, not a general inability to handle media.

## Root-cause location

- `qwenpaw/_compat/message.py` — for `user` messages the allowed content-part types include `{"text", "data"}`, and tool-returned binary is carried as a `{type: "data", data: <b64>}` block.
- The provider / chat-model serialization layer forwards that block to the OpenAI-compatible endpoint **as-is** instead of converting it to the expected `{"type": "image_url", "image_url": {"url": "data:<mime>;base64,<data>"}}`.

## Suggested fix

In the message serialization path, when emitting an OpenAI-compatible request:

- If a content part is `{type: "data", data: <b64>}` with a known `media_type`, wrap it as `data:image/png;base64,...` / `data:application/pdf;base64,...` data URL and emit `{"type": "image_url", "image_url": {"url": <data-url>}}`.
- If `media_type` is unknown, either infer it from the magic bytes or degrade gracefully (skip the part / replace with a short text stub) rather than sending an invalid part.

## Notes / related

- Clearing historical bad content parts is only a workaround: fresh tool-returned media re-triggers the error every time. This is a serialization bug, not a stale-data problem.
- Possibly related: #7516, #7370 (base64 data URIs on WeCom), #7051 (image attachments lost on session reload).

---

## 中文版

> 本 issue 由 AI agent（**deepseek-v4-flash-vision-exp**）代笔起草。经用户（仓库维护者/使用者）确认后发布，用于向 QwenPaw 项目反馈缺陷。

### 概述

当 **agent 工具返回图片或 PDF 二进制**（例如 `send_file_to_user`、`view_image`，或任何结果携带 base64 媒体的工具）时，QwenPaw 在发给模型的请求里会把它序列化成裸的 `{"type": "data", "data": "<base64>"}` content part —— **缺少 `data:<mime>;base64,` 前缀**。会对 content part 做校验的 provider（例如 DeepSeek 的 OpenAI 兼容端点）会拒绝它并报错：

```
openai.BadRequestError: Error code: 400 - {'error': {'message': 'file must have a file_id or file_data', ...}}
```

用户实际看到的是通用的 `claw internal error` / `internal error`，掩盖了真实原因。

### 环境

- **QwenPaw**：2.2.0（python3.13，Debian）
- **Provider**：DeepSeek OpenAI 兼容 chat completions 端点，视觉模型
- **通道**：console / `default` agent
- **触发条件**：agent 调用一个返回图片/PDF 的工具；工具结果二进制被注入消息历史

### 复现

1. 将 DeepSeek 视觉模型配置为 active model。
2. 向 agent 发送一个会触发它使用某工具（结果含图片/PDF，例如 `send_file_to_user` 发 PDF、`view_image` 读本地文件，或任何返回 base64 媒体的工具）的请求。
3. 下一次带着工具结果调用模型。

**实际结果**：`400 BadRequestError: file must have a file_id or file_data`。

### 诊断

错误发生在 `messages[43]`。导出失败的请求可见问题 content part：

```json
{
  "type": "data",
  "data": "iVBORw0KGgoAAAANSUhEUgAA...",   // PNG 魔数，裸 base64
  ...
}
```

一个失败请求里包含 **10** 个这样的 `{"type":"data","data":"<base64>"}` part。关键点：

- 没有 `data:` MIME 前缀（它**不是** `data:image/png;base64,...`）。
- 没有 `image_url` 包裹。
- 没有 `media_type` 字段。

同一构建逻辑在 image-probe 路径（`openai_provider.py` `_probe_image_support`）里会正确生成 `data:image/png;base64,`，所以这是**工具结果/消息序列化路径上的遗漏**，而不是不能处理媒体。

### 根因定位

- `qwenpaw/_compat/message.py` —— 对 `user` 消息，允许的 content part 类型包含 `{"text","data"}`，工具返回二进制被作为 `{type:"data", data:<b64>}` block 携带。
- provider / chat-model 序列化层把该 block **原样**转发给 OpenAI 兼容端点，而没有转换成期望的 `{"type":"image_url","image_url":{"url":"data:<mime>;base64,<data>"}}`。

### 建议修复

在消息序列化路径、发包给 OpenAI 兼容请求时：

- 如果 content part 是 `{type:"data", data:<b64>}` 且已知 `media_type`，则包成 `data:image/png;base64,...` / `data:application/pdf;base64,...` data URL，并输出 `{"type":"image_url","image_url":{"url":<data-url>}}`。
- 如果 `media_type` 未知，则从 magic bytes 推断，或优雅降级（跳过该 part / 用简短文本占位），而不是发送一个无效 part。

### 备注 / 相关

- 只清历史坏 content part 只是权宜之计：每次新增工具返回媒体都会重新触发。这是序列化 bug，不是旧数据问题。
- 可能相关：#7516、#7370（WeCom 的 base64 data URI）、#7051（session 重载时图片附件丢失）。

