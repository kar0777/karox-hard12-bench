You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Oversized image stored in context makes a session permanently unusable

## What happened

A conversation died permanently after an image passed through it.

I was generating a report and having it send an image out. The image was
taller than what the provider accepts, so the provider rejected that request.
Every later message in the same conversation then failed with the same 400 —
including plain-text turns that carried no media at all. The offending image
block is stored in the session context and replayed on every subsequent
request, so the conversation never recovered on its own and stayed unusable.

The only way out was to repair the stored session file by hand.

## Expected

A media payload the provider refuses should cost the media, not the
conversation: the request retries without it, and the stored context is
repaired so later turns go through.

## Why it cannot self-heal today

The rejection matches none of the recovery branches in
`react_agent._reasoning`:

- it does not name the model's capability, so
  `_is_explicit_media_capability_error()` returns `False`;
- in some wordings it also names no size/pixel/limit signal, so the
  request-scoped handling never engages either.

`_reasoning` therefore re-raises, and because the block is still sitting in
the stored context it is replayed forever — the same 400 on every turn,
permanently.

DeepSeek is a concrete case. An image whose side exceeds 8192 px is answered
with:

```
You have uploaded an unsupported image. Please make sure your image is valid
and has one of the following formats: webp, png, jpeg, and gif.
```

That message names neither the limit nor the model's capability, so nothing
classifies it as recoverable.

## Note

`_REQUEST_SCOPED_MEDIA_LIMIT_SIGNALS` already documents that these errors
"may justify a media-free retry, but must never poison the model-wide
`rejects_media` cache" — but no code implements that retry. A PR adding the
missing branch follows.

