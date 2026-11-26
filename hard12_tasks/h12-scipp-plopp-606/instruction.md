You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Colors of clippings in 3d scatter plots do not match original colors

Example:
```Py
import plopp as pp
import scipp as sc

a = pp.data.scatter(1000)
b = a.copy()
b.coords['x'] += sc.scalar(60, unit='m')
pp.scatter3d({'a': a, 'b': b})
```
And then make a spatial clip in Y using the `clip3d` tool under the figure, the green and red opaque clipping should be blue and orange instead, respectively.
![Screenshot at 2024-10-28 14-14-59](https://github.com/user-attachments/assets/824109f0-817d-4c7e-b6c1-a25d1e636f16)

This is because the clippings are added as new data on the figure, and they automatically get given an incremented artist number, which cycles through the colors.

We don't see this when using `cbar=True` because all artists are using the same colormapper.
