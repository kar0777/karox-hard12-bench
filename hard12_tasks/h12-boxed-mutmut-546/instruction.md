You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add mutation for ternary operators

Ternary operator errors of not covering both branches can't be detected by coverage, so it would be useful to mutate these to enable/disable each branch.  E.g.

```python
mark = "x" if count % 2 else "o"
```

mutation into:
```python
mark = "x" if count % 2 and False else "o"
````
and

```python
mark = "x" if count % 2 or True else "o"
````

This types of mutations aren't as useful for normal if statements, because branch coverage can detect when one of the alternatives isn't covered.
