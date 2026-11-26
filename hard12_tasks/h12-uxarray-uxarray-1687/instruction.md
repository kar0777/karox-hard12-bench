You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Determine the Skewness of a Grid using "equiangle" method

Sub-issue of #1305 to track "equiangle" formula implementation for skewness.

For a given face, the equiangle skewness can be defined as:

```math
\text{(equiangle skewness)} = \max\left[\frac{\theta_{max} - \theta_{reg}}{\pi - \theta_{reg}},\ \frac{\theta_{reg} - \theta_{min}}{\theta_{reg}}\right]
```

where $\theta_{min}, \theta_{min}$ are the minimum, maximum internal angles at each node of the face; and $\theta_{reg}$ is the internal angle for a regular polygon with the same number of sides and covering the same area as this face:
```math
\theta_{reg} = \sum(\text{internal angles of this face}) / n
```
where $n$ = number of sides of this face.

This value should be (nearly) 0 for perfectly-regular polygonal faces, and approach 1 for extremely skew / almost degenerate faces.

While this measure is reasonably simple to reason about, it also isn't perfect, because it only considers angles, not side lengths too. For example, a long skinny rectangle will lead to a value close to 0, because all angles would be close to 90 degrees, even though one might expect a long skinny rectangle to be labeled with high skewness. That is not a bug in the implementation, it is just a downside of using the "equiangle" skewness measurement. Other measurements of skewness can be tracked in other issues.
