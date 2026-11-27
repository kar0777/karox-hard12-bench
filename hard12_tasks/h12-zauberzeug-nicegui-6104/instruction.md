You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Character loss in ui.input validation with high network latency

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
from nicegui import ui

def simple_validation(value: str) -> str | None:
    """Simple validation that requires minimum length and specific characters"""
    if len(value) < 3:
        return "Must be at least 3 characters long"
    if not value.isalnum():
        return "Must contain only letters and numbers"
    return None

# Minimal reproduction case
test_input = ui.input(
    label="Test Input",
    validation=simple_validation,
)

...
```

### Description

When typing quickly in `ui.input` fields with validation functions, characters are being deleted/lost during the validation process. This only occurs with network latency - the same application works perfectly when running locally. I live in southern hemisphere so I can say that I have an estimated latency of ~200 to ~400ms. 

### Observation

- Works fine locally: No character loss when running the same code locally
- Geographic dependency: Colleagues near the AZ don’t experience this issue
- Reproducible: Happens consistently when typing at normal speed with validation enabled

This appears to be the same underlying problem described in #[287](https://github.com/zauberzeug/nicegui/issues/287), specifically related to this comment:
		“All input elements involving typing (ui.input, ui.number, and ui.color_input) show flickering and lost characters. … So we probably need to set their state sometime, maybe on change but with some throttling.”
The issue seems to be the roundtrip validation process where each keystroke triggers a client→server→client cycle for validation, and with high latency, this causes desynchronization between user input and the field state.

### Expected Behavior
Input validation should work smoothly regardless of network latency, possibly by implementing automatic throttling for validation functions or debouncing validation calls

### NiceGUI Version

2.24.1

### Python Version

3.12.11

### Browser

Chrome

### Operating System

macOS

### Additional Context

_No response_
