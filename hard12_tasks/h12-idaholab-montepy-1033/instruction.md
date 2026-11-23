You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Implement HalfSpace.mcnp_str() and HalfSpace.format_for_mcnp_input()

## Is your feature request related to a problem? Please describe.

<!-- A clear and concise description of what the problem is. Ex. I'm always frustrated when [...] -->

I'm always frustrated when...

...working with a cell definition and wanting to print out just the geometry string.

```python
>>> cell = montepy.Cell("1 0 -123 234 imp:n=1 u=2")
>>> cell.mcnp_str()
1 0 -123 234 imp:n=1 u=2
>>> cell.geometry
(l: s: False, is_c: False, div: SURFACE: 123, CZ| op: Operator.INTERSECTION| r:s: True, is_c: False, div: SURFACE: 234, PZ)
>>> cell.geometry.mcnp_str()
AttributeError: 'HalfSpace' object has no attribute 'mcnp_str'
```


## Describe the solution you'd like

<!-- A clear and concise description of what you want to happen. -->

Implement `HalfSpace.format_for_mcnp_input()`. Move the geometry/region formatting to  `HalfSpace.format_for_mcnp_input()`. Call that function from within `Cell.format_for_mcnp_input()`. Finally, implement `HalfSpace.mcnp_str()`.

```python
>>> cell.geometry.mcnp_str()
-123 234
```


## Describe alternatives you've considered

<!-- A clear and concise description of any alternative solutions or features you've considered.-->

Doing the same thing with an inheritance scheme for all printable objects.


