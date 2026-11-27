You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Detail Bug] TTS word-timestamp mode duplicates words and misattributes context when whitespace-only token slots are skipped

# Detail Bug Report

https://app.detail.dev/org_1fa3c5ff-f485-452b-8fbd-870cbd985e00/bugs/bug_2149b541-1418-4420-9990-eb9582629322

Introduced in [#4380](https://github.com/pipecat-ai/pipecat/pull/4380) by @filipi87 on May 20, 2026

# Summary
- **Context**: The `AggregatedFrameSequencer.process_word` method handles TTS word-timestamp events, force-completing slots when a word arrives for a later slot before the current slot is complete.
- **Bug**: When force-completing a slot whose remaining TTS text is whitespace-only (normalizes to empty), the frame text fallback incorrectly uses the incoming word instead of the slot's actual remaining text.
- **Actual vs. expected**: The method emits a `TTSTextFrame` with the wrong word text (the incoming word for the next slot) attributed to the wrong context. Expected behavior is to skip emitting a frame for the whitespace-only slot and only emit the word with its correct context.
- **Impact**: In token streaming mode with word-timestamp services (Cartesia, ElevenLabs, etc.), whitespace-only tokens cause subsequent words to be duplicated in the transcript with incorrect context attribution, corrupting the conversation context.

# Code with Bug
```python
# aggregated_frame_sequencer.py

frame_text = (
    active.tracker.get_word_for_frame() if (active and active.tracker) else word
) or word  # <-- BUG 🔴 falls back to incoming word when get_word_for_frame() returns "" for whitespace-only slots
```

# Explanation
`WordCompletionTracker.get_word_for_frame()` strips whitespace from the tracked slot’s `_frame_word`. If a slot is whitespace-only (e.g. `" "`), `get_word_for_frame()` returns `""` (falsy), so the `(... ) or word` expression uses `word` from the *next* slot. When TTS providers skip whitespace entries in word timestamps (common behavior), `process_word()` force-completes the whitespace slot and incorrectly emits a `TTSTextFrame` containing the next real word but with the whitespace slot’s `context_id`. The same word is then emitted again when processing the correct slot, producing duplicates and wrong context attribution.

## Codebase Inconsistency
`force_complete()` already guards against emitting empty remaining text:

```python
# force_complete()
if remaining_text:  # <-- guard against empty text
    frames.append(self._build_word_frame(...))
```

`process_word()` lacks an equivalent guard, leading to fabrication of a frame for whitespace-only slots.

# Failing Test
```python
def test_whitespace_slot_force_complete_skips_emission(self):
    """When a whitespace-only slot is force-completed, no frame should be emitted for it."""
    seq = AggregatedFrameSequencer(name="test")

    tracker1 = WordCompletionTracker(" ")
    frame1 = AggregatedTextFrame(" ", AggregationType.TOKEN)
    seq.register_spoken(frame1, "ctx1", tracker1, append_to_context=True)

    tracker2 = WordCompletionTracker("World")
    frame2 = AggregatedTextFrame("World", AggregationType.TOKEN)
    seq.register_spoken(frame2, "ctx2", tracker2, append_to_context=True)

    # Word for ctx2 arrives, forcing ctx1 (whitespace) to complete
    result = seq.process_word("World", pts=10, context_id="ctx2")

    word_frames = [f for f in result if isinstance(f, TTSTextFrame)]

    # Should only emit ONE frame with ctx2, not duplicate with ctx1
    assert len(word_frames) == 1, f"Expected 1 frame, got {len(word_frames)}"
    assert word_frames[0].text == "World"
    assert word_frames[0].context_id == "ctx2"
```

# Recommended Fix
Add a guard similar to `force_complete` to skip emitting frames for whitespace-only slots during force-complete in `process_word` (i.e., if `active.tracker.get_word_for_frame()` is empty/whitespace-only, mark the slot complete, flush, and continue processing overflow without emitting a `TTSTextFrame` for that slot).

# History
This bug was introduced in commit deefc32fa. The commit introduced the `AggregatedFrameSequencer` class to fix an ordering problem where skipped TTS frames (e.g., code blocks filtered via `skip_aggregator_types`) were emitted immediately instead of waiting for preceding spoken frames to complete. The `process_word` method needed to handle the case where `get_word_for_frame()` returns an empty string for whitespace-only slots, but the `or word` fallback incorrectly uses the incoming word from the next slot instead of skipping emission for the empty slot, causing duplicate frames with wrong context attribution.
