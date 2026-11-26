You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ChatPromptBuilder silently drops every content part after the first TextContent

**Describe the bug**

`ChatPromptBuilder` accepts a template that is a list of `ChatMessage` objects, and a `ChatMessage` can carry several
content parts (more than one `TextContent`, plus `ImageContent` / `FileContent`). The builder however only ever looks at
`message.text`, which returns the text of the **first** `TextContent` part. Two consequences:

- `run()` rebuilds the rendered message as `replace(message, _content=[TextContent(text=rendered_text)])`, so every
  other content part is silently removed from the rendered prompt;
- `__init__()` infers template variables from `message.text` only, so a variable that lives in one of the dropped parts
  is never reported as a required input.

For a prompt that mixes text and images the generator therefore receives only the first text, and the image just
disappears — with no warning.

**Error message**

None. The failure is silent, which is why it is easy to miss.

**Expected behavior**

Every `TextContent` part of a template message is rendered, non-text content parts are passed through unchanged, and
template variables are inferred from all text parts.

**Additional context**

The same one-part assumption also hides the `templatize_part` filter check for text parts after the first one.

**To Reproduce**

On current `main` (`4354727`):

```python
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder
from haystack.dataclasses import ChatMessage, ImageContent, TextContent

image = ImageContent(base64_image="cHJldGVuZC1wbmctYnl0ZXM=", mime_type="image/png")
template = [
    ChatMessage.from_user(
        content_parts=[
            TextContent(text="Describe {{ thing }}"),
            image,
            TextContent(text="Also {{ other }}"),
        ]
    )
]

builder = ChatPromptBuilder(template=template)
print(builder.variables)  # actual: ['thing'] -- 'other' is never detected
prompt = builder.run(thing="this", other="x")["prompt"][0]
print(prompt.texts)  # actual: ['Describe this'] -- "Also x" is gone
print([type(p).__name__ for p in prompt._content])  # actual: ['TextContent'] -- the image is gone too
```

**FAQ Check**

- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**

- OS: Windows 11
- Haystack version: main @ `4354727`

