You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

OpenAIChatGenerator: default gpt-5-mini shuts down 11 Dec, and gpt-5.6-terra refuses its tool calls on Chat Completions (HTTP 400)

At main @ 622967d:

- **The default model shuts down.** `OpenAIChatGenerator(model="gpt-5-mini")` is the default (`haystack/components/generators/chat/openai.py:124`; the docs page also says "The default model is `gpt-5-mini`"). OpenAI shuts it down on 11 December 2026 and names `gpt-5.6-terra` as the replacement ([deprecations page](https://developers.openai.com/api/docs/deprecations), entry "2026-06-11: GPT-5 and o3 model deprecations").
- **The replacement refuses tool calls on this endpoint.** The component sends `tools` on Chat Completions (`openai.py:539-554`) with no reasoning setting. Sent live on 25 Oct in that shape (one user message, one function tool, `n=1`): `gpt-5-mini` answers; `gpt-5.6-terra` returns HTTP 400 "Function tools with reasoning_effort are not supported for gpt-5.6-terra in /v1/chat/completions."

So an `Agent` on the default generator stops on 11 December, and changing only the default model name does not bring it back.

I sent the requests directly, not through a pipeline.

---
*I'm Lakshya; I'm building a tool that checks model migrations on a team's real requests.*

