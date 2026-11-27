You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Detail Bug] YAML DTMF values like 010 or 0x10 are silently changed into different key sequences

# Detail Bug Report

https://app.detail.dev/org_1fa3c5ff-f485-452b-8fbd-870cbd985e00/bugs/bug_c1e2830c-ee35-4567-a146-b513c54a14e5

Introduced in [#4849](https://github.com/pipecat-ai/pipecat/pull/4849) by @aconchillo on Jun 22, 2026

# Summary
- **Context**: The framework supports unquoted integer DTMF but corrupts YAML octal (`010` → `"8"`) and hex (`0x10` → `"16"`) values.
- **Bug**: The framework supports unquoted integer DTMF but corrupts YAML octal (`010` → `"8"`) and hex (`0x10` → `"16"`) values.
- **Actual vs. expected**: **Expected**: `dtmf: 010` is treated as the digit sequence `"010"` (three keypresses), and `dtmf: 0x10` is treated as `"0x10"`. **Actual**: YAML 1.1 SafeLoader parses these as integers (`8` and `16`), and the framework coerces them to strings (`"8"`, `"16"`), silently changing the DTMF sequence while still passing validation.
- **Impact**: Silent corruption of DTMF sequences (especially leading-zero PINs / sequences) causes scenarios/tests to send the wrong keys without any load-time error or warning, making failures confusing to debug.

# Code with Bug
```python
def _parse_dtmf(dtmf: Any, path: Path, turn_idx: int) -> str | None:
    if dtmf is None:
        return None
    if isinstance(dtmf, int):
        dtmf = str(dtmf)  # <-- BUG 🔴 silently normalizes YAML 1.1 octal/hex ints, losing original digit sequence
    # ... rest of validation
```

# Explanation
- PyYAML 6.0.3 `SafeLoader` implements YAML 1.1 numeric rules, which interpret values like `010` as octal and `0x10` as hex *before* application code sees them.
- By the time `_parse_dtmf` runs, it receives `int(8)` / `int(16)` and cannot recover the original token (`"010"` / `"0x10"`). Coercing to string therefore produces the wrong DTMF sequence.
- This is silent because the resulting characters (e.g., `8`, `1`, `6`) are valid DTMF keys, so downstream validation does not fail.

## Codebase Inconsistency
- The framework both (a) tests support for unquoted integer DTMF (e.g., `dtmf: 123`) and (b) documents quoting DTMF values, yet currently provides no warning/error for the YAML 1.1 octal/hex cases that silently change meaning.

# Recommended Fix
Add a warning when `dtmf` arrives as an `int` to alert users that YAML 1.1 may have rewritten their input (octal/hex) and to quote DTMF strings to preserve the intended sequence. A lower-noise variant is to warn only for small integers (`0..9`), which are the common outcomes of octal-like literals such as `010 → 8`.

# History
This bug was introduced in commit 02a01a82. The commit added DTMF turn support with integer-to-string coercion for convenience (`dtmf: 123` → `"123"`), but didn't account for YAML 1.1's octal (`010` → 8) and hex (`0x10` → 16) interpretation that silently corrupts leading-zero or hex-prefixed sequences.
