You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Plotting 24 or more lines raises AttributeError: 'int' object has no attribute 'lower'

Plotting a dict (e.g. from `sc.collapse`) with 24 or more entries raises:

```
AttributeError: 'int' object has no attribute 'lower'
```

## Reproducer

```python
import scipp as sc
import plopp as pp

da = sc.DataArray(sc.ones(dims=['x'], shape=[5]),
                  coords={'x': sc.arange('x', 5.0, unit='m')})
pp.plot({str(i): da for i in range(24)})   # 23 entries works, 24 raises
```

Traceback ends in

```
File "plopp/backends/matplotlib/line.py", line 293, in __init__
    if self._line.get_marker().lower() != 'none':
AttributeError: 'int' object has no attribute 'lower'
```

The data must have bin-centre coords, so that the marker style is used; histogram data takes the `step` path and has no marker.

## Cause

The default marker is cycled through the full matplotlib marker registry:

```python
markers = list(Line2D.markers.keys())
...
'marker': markers[(artist_number + 2) % len(markers)]
```

`Line2D.markers` is not a list of usable plot markers. From index 25 onwards it contains the integer tick/caret markers (`0`-`11`), and the last four entries are `'None'`, `'none'`, `' '` and `''`. So

- artist numbers 23-34 get an integer marker, which then fails the `.lower()` check,
- artist numbers 35-38 would silently produce invisible lines.

`backends/matplotlib/scatter.py` uses the same expression. It does not raise, but for artist numbers 35-38 it silently draws nothing, and before that it uses unfilled tick markers that trigger matplotlib "unfilled marker" warnings for the mask overlay.

## Suggested fix

Cycle over `Line2D.filled_markers` instead, which contains only valid, visible markers.

