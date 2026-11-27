You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SonioxSTTService drops per-token language field from TranscriptionFrame

### pipecat version

1.1.0

### Python version

3.12.8

### Operating System

Mac

### Issue description

SonioxSTTService._receive_messages builds TranscriptionFrame(...) at [services/soniox/stt.py L575-583](https://github.com/pipecat-ai/pipecat/blob/main/src/pipecat/services/soniox/stt.py) without setting language=. Even with enable_language_identification=True in SonioxSTTService.Settings, the per-token language returned by Soniox is silently dropped on its way to downstream processors.

Soniox API contract (per [the WebSocket API docs](https://soniox.com/docs/api-reference/stt/websocket-api)):

Each token in the tokens array contains a language field (string, ISO code like "en", "nl")
Observed:

TranscriptionFrame.language is always None even when Soniox returns valid per-token language info
Downstream processors that route by detected language (TranslationProcessor, language-aware aggregators) can't function

Proposed fix (one-liner):
```
# In send_endpoint_transcript():
_langs = [t.get("language") for t in self._final_transcription_buffer if t.get("language")]
language = None
if _langs:
    from collections import Counter
    _lang_str = Counter(_langs).most_common(1)[0][0]
    try:
        language = Language(_lang_str)
    except ValueError:
        pass  # Soniox returned a code Pipecat's enum doesn't cover

await self.push_frame(
    TranscriptionFrame(
        text=text,
        user_id=self._user_id,
        timestamp=time_now_iso8601(),
        result=self._final_transcription_buffer,
        finalized=True,
        language=language,  # NEW
    )
)

```

### Reproduction steps

- Configure SonioxSTTService with multiple language_hints and enable_language_identification=True
- Speak in one of the configured languages
- Inspect the emitted TranscriptionFrame.language — always None


### Expected behavior

TranscriptionFrame.language should be set

### Actual behavior

TranscriptionFrame.language is not set

### Logs

```shell

```
