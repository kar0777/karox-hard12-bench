You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

dcmread leaks ValueError("embedded null character") on SpecificCharacterSet with leading/middle NUL

### Description

`pydicom.dcmread(force=True)` leaks `ValueError("embedded null character")` when `SpecificCharacterSet` (0008,0005) contains a NUL byte in a leading or middle position. The exception comes from `codecs.lookup` inside `pydicom.charset._python_encoding_for_corrected_encoding` (`src/pydicom/charset.py:733-738` on `main` @ `fb1f24e4f0`):

```python
# fallback: assume that it is already a python encoding
try:
    codecs.lookup(encoding)
    return encoding
except LookupError:
    _warn_about_invalid_encoding(encoding)
    return default_encoding
```

CPython's encoding-name normalisation raises `ValueError` (not `LookupError`) on NUL-containing strings, so the catch never fires. The same `convert_encodings` docstring (`charset.py` lines ~674-679) already documents `LookupError` as the only raised exception under `reading_validation_mode=RAISE`; today's behaviour silently violates that.

### Steps to Reproduce

Minimal in-memory repro (Implicit VR Little Endian body so the `CS` value is stored verbatim without VR-level normalisation):

```python
import io
import struct
import pydicom

def explicit(group, elem, vr, value):
    if vr in (b"OB",):
        return (
            struct.pack("<HH", group, elem) + vr + b"\x00\x00"
            + struct.pack("<I", len(value)) + value
        )
    return struct.pack("<HH", group, elem) + vr + struct.pack("<H", len(value)) + value

def implicit(group, elem, value):
    return struct.pack("<HHI", group, elem, len(value)) + value

preamble = b"\x00" * 128 + b"DICM"
meta  = explicit(0x0002, 0x0001, b"OB", b"\x00\x01")
meta += explicit(0x0002, 0x0002, b"UI", b"1.2.840.10008.5.1.4.1.1.7\x00")
meta += explicit(0x0002, 0x0003, b"UI", b"1.2.3.4\x00")
meta += explicit(0x0002, 0x0010, b"UI", b"1.2.840.10008.1.2\x00")
meta += explicit(0x0002, 0x0012, b"UI", b"1.2.3\x00")
group_length = explicit(0x0002, 0x0000, b"UL", struct.pack("<I", len(meta)))
ds = implicit(0x0008, 0x0005, b"ISO\x00_IR 100")  # middle-NUL

pydicom.dcmread(io.BytesIO(preamble + group_length + meta + ds), force=True)
```

### Actual Result

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
  File ".../pydicom/charset.py", line 696, in convert_encodings
    py_encodings.append(python_encoding[encoding])
KeyError: 'ISO\x00_IR 100'
During handling of the above exception, another exception occurred:
  File ".../pydicom/charset.py", line 698, in convert_encodings
    py_encodings.append(_python_encoding_for_corrected_encoding(encoding))
  File ".../pydicom/charset.py", line 735, in _python_encoding_for_corrected_encoding
    codecs.lookup(encoding)
ValueError: embedded null character
```

### Expected Result

The same warn-and-fallback path as truly unknown encodings: a `UserWarning("Unknown encoding 'ISO\x00_IR 100' - using default encoding instead")` and a parsed dataset. Under `enforce_valid_values`, `LookupError` (which `_warn_about_invalid_encoding` already raises for unknown encodings on `charset.py:760`), not `ValueError`.

### Prior Art

Issue #940 (closed 2019-09-06, label `question`) reported the same traceback for a `SpecificCharacterSet` value ending in a NUL (`b"ISO_IR 100\x00"`). The discussion proposed a NUL-stripping fix in `valuerep.MultiString`, and that fix appears to have landed in some form — on current `main`, **trailing**-NUL `SpecificCharacterSet` values are absorbed by `valuerep` before reaching `convert_encodings`. I verified empirically: `dcmread` on a file with `SpecificCharacterSet = b"ISO_IR 100\x00\x00"` parses cleanly and returns `SpecificCharacterSet == "ISO_IR 100"`.

That implicit fix does **not** cover NULs in leading or middle positions, which is what this issue reports. The minimal repro above uses `b"ISO\x00_IR 100"` because that's the case that still leaks on current `main`.

This issue is intentionally narrower than #940's framing: #940 was a question about whether the file should parse (the maintainer concern at closure was "chasing invalid DICOM endlessly... every extra check hits performance"). The cost here is zero in the happy path — the `try/except` is already present at the call site; this change widens the matched exceptions, it does not add a new check.

### Alternatives Considered

1. **Widen `except LookupError` to `except (LookupError, ValueError)`** in `_python_encoding_for_corrected_encoding`. Minimal diff, but `codecs.lookup` re-raises *any* exception from a third-party codec search function registered via `codecs.register`; widening the except silently swallows those.
2. **Pre-check `"\x00" in encoding`** before `codecs.lookup`, falling through the same `_warn_about_invalid_encoding(encoding); return default_encoding` path used for `LookupError`. (My local branch takes this approach.) Documents intent in code and leaves third-party `codecs.register` ValueErrors surfaced as real bugs.
3. **Extend `valuerep.MultiString` NUL handling** to also strip leading/middle NULs. Larger blast radius — affects every `CS`/`SH`/etc. value, not just `SpecificCharacterSet` — and changes parsed-value semantics for tags where a middle NUL might be semantically meaningful in another stack.

Option (2) is the narrowest fix that preserves the documented `convert_encodings` contract without changing any other value-decoding behaviour.

### Versions

- pydicom: current `main` @ `fb1f24e4f0` (also reproduces against PyPI 3.0.2)
- Python: 3.13
- OS: Windows 11

### Related

- Same shape of "Python BCL exception leaking from `dcmread`'s public contract" as #2330/PR #2331 (`RecursionError` on deep SQ), #2332/PR #2333 (`OSError` on truncated SQ item), and #2336/PR #2337 (`NotImplementedError` on unknown VR). I have a local branch with the option-(2) fix + parametrised tests in `test_charset.py` + an end-to-end `test_filereader.py` case mirroring #2337's pattern; happy to open a PR if option (2) is the path you'd like.

