You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Universe 0 in a `u` data input: a repeated 0 crashes the write, and trailing zeros are dropped

## Bug Description

When MontePy writes a `u` data input, it turns each universe 0 into a jump. That causes two problems, both on a problem that is read and written back without changes:

1. **A repeated 0 crashes the write.** `u 0 2r 5` reads correctly as `[0, 0, 0, 5]`, but `write_problem` raises `IndexError: deque index out of range`.
2. **Trailing zeros are dropped.** `u 5 0 0 0` is written as `u 5 `, one entry for four cells. MontePy reads its own output back as `[5, 0, 0, 0]`. The 6.2 manual, though, says that for the `U` data card "there must be an entry (which can be 0) for each cell in the problem" (§3.3.1.5.1, Table 3-20).

Both inputs are valid. That same note allows 0 entries, and the input shortcuts allow `nR` after any number (§2.8). With four cells:

| `u` input | Written as |
|---|---|
| `u 0 2r 5` | `IndexError` |
| `u 5 0 0 0` | `u 5 ` |
| `u 0 0 0 5` | `u 3J 5` |
| `u 1 2r 5` | `u 1 2r 5` |
| `u 5 j 5 j` | `u 5 j 5 j` |

The cause looks like this:

1. On write, `UniverseInput._collect_new_values` sets the value of each cell in universe 0 to `None`, so that it's written as a jump ([universe_input.py#L166-L168](https://github.com/idaholab/MontePy/blob/afa42093526b696297e6e6a4c2928149b0b08e9c/montepy/data_inputs/universe_input.py#L166-L168)).
2. `update_with_new_values` empties each shortcut and offers it the new values. In the first case, the first value offered to the `2r` repeat is now that jump. In `ShortcutNode._can_consume_node`, a repeat holding no values accepts only a value that isn't `None`, so the jump falls through to `self.nodes[-1]` on the empty deque ([syntax_node.py#L2329-L2333](https://github.com/idaholab/MontePy/blob/afa42093526b696297e6e6a4c2928149b0b08e9c/montepy/input_parser/syntax_node.py#L2329-L2333)).
3. In the second case, the trailing zeros become a jump that wasn't in the input. `update_with_new_values` then removes it as a "jump the user left off".

## To Reproduce

``` python
import io

import montepy

deck = "toy deck\n1 0 -1 fill=5\n2 0 1 -2\n3 0 2\n4 0 -3\n\n1 so 1.0\n2 so 2.0\n3 so 5.0\n\nu 0 2r 5\nimp:n 1 1 0 1\nnps 1\n"
problem = montepy.read_input(io.StringIO(deck))
print([cell.universe.number for cell in problem.cells])
# [0, 0, 0, 5]
problem.write_problem(io.StringIO())
```

For the dropped zeros, swap in this deck. The four cells' universes are `[5, 0, 0, 0]`, and the problem is written with `u 5 `:

``` python
deck = "toy deck\n1 0 -3\n2 0 -1 fill=5\n3 0 1 -2\n4 0 2\n\n1 so 1.0\n2 so 2.0\n3 so 5.0\n\nu 5 0 0 0\nimp:n 1 1 1 0\nnps 1\n"
```

## Error Message

<details open>

``` python
Traceback (most recent call last):
  File "repro.py", line 8, in <module>
    problem.write_problem(io.StringIO())
  File ".../site-packages/montepy/mcnp_problem.py", line 548, in write_problem
    self._write_to_stream(new_file)
  File ".../site-packages/montepy/mcnp_problem.py", line 602, in _write_to_stream
    lines = obj.format_for_mcnp_input(self.mcnp_version)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../site-packages/montepy/mcnp_object.py", line 49, in wrapped
    add_line_number_to_exception(e, self)
  File ".../site-packages/montepy/exceptions.py", line 259, in add_line_number_to_exception
    raise error.with_traceback(trace)
  File ".../site-packages/montepy/mcnp_object.py", line 41, in wrapped
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File ".../site-packages/montepy/data_inputs/cell_modifier.py", line 299, in format_for_mcnp_input
    self._update_values()
  File ".../site-packages/montepy/data_inputs/cell_modifier.py", line 236, in _update_values
    self.data.update_with_new_values(new_vals)
  File ".../site-packages/montepy/input_parser/syntax_node.py", line 1775, in update_with_new_values
    self._expand_shortcuts(new_vals, new_vals_cache)
  File ".../site-packages/montepy/input_parser/syntax_node.py", line 1846, in _expand_shortcuts
    if try_expansion(shortcut, new_vals[i]):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../site-packages/montepy/input_parser/syntax_node.py", line 1811, in try_expansion
    status = shortcut.consume_edge_node(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../site-packages/montepy/input_parser/syntax_node.py", line 2408, in consume_edge_node
    if self._can_consume_node(node, direction, last_edge_shortcut):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../site-packages/montepy/input_parser/syntax_node.py", line 2326, in _can_consume_node
    edge = self.nodes[-1]
           ~~~~~~~~~~^^^^
IndexError:     StringIO, line 10

        11| u 0 2r 5
deque index out of range
```

</details>

## MCNP input file snippet

```
toy deck
1 0 -1 fill=5
2 0 1 -2
3 0 2
4 0 -3

1 so 1.0
2 so 2.0
3 so 5.0

u 0 2r 5
imp:n 1 1 0 1
nps 1
```

## Version

 - Version 1.5.0 (Python 3.12.15). I haven't run it on `develop`, but the code linked above is unchanged at `afa4209`.

