You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add possibility to change cmap on existing figure

Currently, this does not work
```Py
import plopp as pp

da = pp.data.data2d()
f = da.plot()

f.view.colormapper.cmap = 'hot'
f.view.colormapper.autoscale()  # Call autoscale to update
```
It fails with `TypeError: 'str' object is not callable`.

We need to pass `matplotlib.colormaps['hot']` for it to work, and this then bypasses some changes we make to the cmap (setting bad value color etc).

