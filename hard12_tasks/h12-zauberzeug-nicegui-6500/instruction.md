You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Choice change callbacks return frontend models or indices as previous_value

### First Check
- [x] I added a descriptive title.
- [x] This is an ordinary callback-data bug, not a security issue.
- [x] This is not a Q&A; the callback exposes the previous choice in the wrong representation.
- [x] I searched existing issues and PRs without finding a matching fix.

### Example Code
```python
from nicegui import ui

changes = []
radio = ui.radio({101: 'Alice', 205: 'Bob'}, value=101,
                 on_change=lambda e: changes.append((e.value, e.previous_value)))
radio.set_value(205)
print(changes)  # [(205, 0)], expected [(205, 101)]
```

### Description
`value` is the public Python selection, but `previous_value` comes from the old frontend prop. With dict-backed choices this mixes a selected record ID with an array index. Single select returns an old frontend model dictionary; multiple select returns a list of those dictionaries. Plain input and checkbox controls return the expected prior Python value.

I traced this to `ValueElement._handle_value_change`. Before implementing, I would like to check the intended boundary, per the contribution guide. A local last-value cache fixes ordinary choices, but `BindableProperty` propagates bindings before notifying the original element. A bound callback can assign the original element again first:
```python
source = ui.input(value='first', on_change=lambda e: print(e.value, e.previous_value))
target = ui.input(value='first')
source.bind_value_to(target)
def change_source(e):
    if e.value == 'second':
        source.set_value('third')
target.on_value_change(change_source)
source.set_value('second')
# observed: third first, then second third
```
The assignments were first→second→third. A local event cache cannot capture the actual prior assignment in this sequence. Should `previous_value` represent the immediate prior Python assignment, or the previous delivered event? If it means the assignment, capturing the transition before binding propagation seems necessary. I have not changed notification order or any library code.

### NiceGUI Version
Main source `5072d1649adaa81c9abdce7fe8733fb05d79b0ea`, imported from a verified clean Git clone. The reused archive environment reports metadata 0.0.0, which is not a release-version claim for this source.

### Python Version
3.13.14

### Browser
Other: programmatic constructor/set_value/callback replay only, no browser execution.

### Operating System
macOS, Apple Silicon

### Additional Context
Reproduced five choice cases and two passing controls, plus the input-only binding example above. No full pytest or frontend suite result is claimed. No production incidence or first affected release is established. Diagnosis and reproduction used GPT-6.1 Sol (high) through Codex.

