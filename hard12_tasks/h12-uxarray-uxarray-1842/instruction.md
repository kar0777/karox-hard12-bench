You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

UxDataArray.integrate() ignores `quadrature_rule` and `order` kwargs

### Version

2026.6.0

### How did you install UXarray?

Source

### What happened?

Calling UxDataArray.integrate(order=8), for example, does not actually utilize order=8. Similarly, adjusting quadrature_rule has no effect on results. This was introduced by #1379, which swapped to using `self.uxgrid.face_areas` instead of `self.uxgrid.compute_face_areas(quadrature_rule, order)` here, but failed to remove the quadrature_rule and order kwargs from the function signature and docstring.

Related: #1567, #1568, #1571, #1577.



### What did you expect to happen?

I expected these documented kwargs to be handled properly inside the function, or for these kwargs to be removed or be documented as "deprecated".

If the decision ends up being to properly handle these kwargs, it might make sense to wait until after #1577 gets merged. If the decision is to remove them, maybe there should be a deprecation cycle?

### Can you provide a MCVE to repoduce the bug?

```python

```
