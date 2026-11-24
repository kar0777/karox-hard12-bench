You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

redact_secrets masks the detail after an exception class name (KeyError: '[REDACTED]')

## Summary

`redact_secrets` (`pipecat/utils/security/redaction.py`, shipped in 1.13.0) masks the value of a `Name: detail` pair when the NAME contains a credential word, and an exception class name often does: `KeyError` holds `key`, `InvalidTokenError` holds `token`, `ExpiredSignatureError` holds `signature`.
So the text an `ErrorFrame` (or any string passed through it) carries for such an exception loses its detail: `KeyError: '[REDACTED]'`.

## Repro (pipecat-ai 1.13.0)

```python
from pipecat.utils.security.redaction import redact_secrets

for text in (
    "KeyError: 'audio_content'",
    "InvalidTokenError: signature has expired",
    "ExpiredSignatureError: Signature has expired",
    "TokenExpiredError: jwt expired",
):
    print(repr(text), "->", repr(redact_secrets(text)))
```

Output:

```
"KeyError: 'audio_content'" -> "KeyError: '[REDACTED]'"
'InvalidTokenError: signature has expired' -> 'InvalidTokenError: [REDACTED] has expired'
'ExpiredSignatureError: Signature has expired' -> 'ExpiredSignatureError: [REDACTED] has expired'
'TokenExpiredError: jwt expired' -> 'TokenExpiredError: [REDACTED] expired'
```

## Why it matters

`ErrorFrame.__post_init__` masks `error` with `redact_secrets`, and services build that text from the exception (`llm_service.py` formats `f"{type(e).__name__}: {e}"`, and many services use `f"...{e}"`).
A message that starts with the class name is the shape that loses its detail, so the frame, the log line and the RTVI message all lose the one fact that says what failed (the missing dict key, the reason a token was refused), with nothing in the output to say the text was masked.

## Proposal

A name whose last word is `error`, `exception` or `warning` is not a credential name; the credential words stay as they are.
In `_is_credential_name`, before the `return`:

```python
    # An exception or warning name (KeyError, InvalidTokenError) names what went wrong,
    # not a credential; the text after it is the explanation.
    if parts and parts[-1] in {"error", "exception", "warning"}:
        return False
```

With that guard the four examples above print unchanged, and the credential cases still mask:

```
'api_key: abc123'              -> 'api_key: [REDACTED]'
'X-Api-Key: abc123'            -> 'X-Api-Key: [REDACTED]'
'Authorization: Bearer abc123' -> 'Authorization: Bearer [REDACTED]'
'token=abc123'                 -> 'token=[REDACTED]'
'password: hunter2'            -> 'password: [REDACTED]'
```

Limits, for the record:
- A name that does not end in one of the three words (`SignatureDoesNotMatch: ...`) still masks.
- A credential field that really ends in `error` (`token_error`) would stop being masked; its value is an error description, not a secret.
- An alternative with the same effect for the common shape: skip a `Name:` whose name is a CamelCase identifier ending in `Error` or `Exception`. The last-word rule is the smaller change and also covers snake_case and kebab-case names.

Happy to send a PR if the rule is agreeable.

