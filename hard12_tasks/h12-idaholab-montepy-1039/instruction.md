You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Adjacent shortcuts don't round-trip (lost padding, parse crash, dropped interpolate start)

<!--
**Reminders**
1. This is not a place to debug your MCNP models
1. MCNP is export controlled and only its 6.2 and 6.3 user manuals are public. Don't include any information about MCNP which is not in those manuals.
1. Your model may be export controlled, or proprietary. Please change specific numbers (e.g., dimensions, material compositions, etc.) in your minimum working examples. -->

## Bug Description

Found while testing #1019. Three related problems with shortcuts that touch each other, all on `develop` at 98cfe30a:

1. **Trailing padding lost after a run of shortcuts.** In `shortcut_phrase`, two adjacent shortcuts come back from `shortcut_sequence` as a `ListNode`, and `sequence.end_padding = p.padding` sets a plain attribute on that `ListNode` that nothing reads. `vol 2 3m 2m 1` formats as `vol 2 3m 2m1`. Edit any value in the card and that string is what gets written, and it no longer parses.
2. **Three or more adjacent shortcuts fail to parse.** `_expand_repeat` and `_expand_interpolate` take `p[0].nodes[-1]` as the previous value, which is a `ShortcutNode` when `p[0]` is that `ListNode`. `_expand_multiply` already unwraps it. `vol 2 3m 2m 2r 1` raises `AttributeError: 'ShortcutNode' object has no attribute 'value'`.
3. **An interpolate's own start value gets folded into the previous shortcut.** `_format_interpolate` reuses the previous shortcut's last node as its start whenever the values match, even when the interpolate has its own start node. `vol 9 r 9 1i 27` (9 9 9 18 27) formats as `vol 9 r 2i 27`, which MCNP reads as 9 9 15 21 27.

## To Reproduce

``` python
from montepy.input_parser.mcnp_input import Input
from montepy.input_parser.block_type import BlockType
from montepy.data_inputs import volume

for line in ["vol 2 3m 2m 1", "vol 9 r 9 1i 27", "vol 2 3m 2m 2r 1"]:
    v = volume.Volume(Input([line], BlockType.DATA), in_cell_block=False)
    print(repr(v._tree.format()))
```

```
'vol 2 3m 2m1'
'vol 9 r 2i 27'
```

## Error Message 

The third line raises:

<details open> 

``` python
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
  File "~/dev/montepy/montepy/mcnp_object.py", line 49, in wrapped
    add_line_number_to_exception(e, self)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "~/dev/montepy/montepy/exceptions.py", line 235, in add_line_number_to_exception
    raise error
  File "~/dev/montepy/montepy/mcnp_object.py", line 41, in wrapped
    return func(*args, **kwargs)
  File "~/dev/montepy/montepy/data_inputs/volume.py", line 34, in __init__
    super().__init__(input, in_cell_block, key, value)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/dev/montepy/montepy/mcnp_object.py", line 49, in wrapped
    add_line_number_to_exception(e, self)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "~/dev/montepy/montepy/exceptions.py", line 235, in add_line_number_to_exception
    raise error
  File "~/dev/montepy/montepy/mcnp_object.py", line 41, in wrapped
    return func(*args, **kwargs)
  File "~/dev/montepy/montepy/data_inputs/cell_modifier.py", line 39, in __init__
    super().__init__(input, fast_parse)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "~/dev/montepy/montepy/mcnp_object.py", line 49, in wrapped
    add_line_number_to_exception(e, self)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "~/dev/montepy/montepy/exceptions.py", line 235, in add_line_number_to_exception
    raise error
  File "~/dev/montepy/montepy/mcnp_object.py", line 41, in wrapped
    return func(*args, **kwargs)
  File "~/dev/montepy/montepy/data_inputs/data_input.py", line 62, in __init__
    super().__init__(input, self._parser)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "~/dev/montepy/montepy/mcnp_object.py", line 49, in wrapped
    add_line_number_to_exception(e, self)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "~/dev/montepy/montepy/exceptions.py", line 259, in add_line_number_to_exception
    raise error.with_traceback(trace)
  File "~/dev/montepy/montepy/mcnp_object.py", line 41, in wrapped
    return func(*args, **kwargs)
  File "~/dev/montepy/montepy/mcnp_object.py", line 127, in __init__
    self._tree = parser.parse(tokenizer, input)
                 ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "~/dev/montepy/montepy/input_parser/parser_base.py", line 147, in parse
    tree = super().parse(token_generator)
  File "~/dev/montepy/.venv/lib/python3.14/site-packages/sly/yacc.py", line 2137, in parse
    value = p.func(self, pslice)
  File "~/dev/montepy/montepy/input_parser/parser_base.py", line 280, in shortcut_sequence
    short_cut = syntax_node.ShortcutNode(p)
  File "~/dev/montepy/montepy/input_parser/syntax_node.py", line 2122, in __init__
    self._expand_repeat(p)
    ~~~~~~~~~~~~~~~~~~~^^^
  File "~/dev/montepy/montepy/input_parser/syntax_node.py", line 2216, in _expand_repeat
    if last_val.value is None:
       ^^^^^^^^^^^^^^
AttributeError: 'ShortcutNode' object has no attribute 'value'

Error came from an object of type <class 'montepy.data_inputs.volume.Volume'> from an unknown file.
```

</details>

## MCNP input file snippet

```
vol 2 3m 2m 1
vol 9 r 9 1i 27
vol 2 3m 2m 2r 1
```

## Version

 - Version: `develop` at 98cfe30a

## Additional context

Fix with tests is up as a PR.

