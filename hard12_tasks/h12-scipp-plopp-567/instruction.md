You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`Inspector tool`: Cannot select coordinate for reduced dimension

It is currently not possible to specify which coordinate to be used when plotting the 3rd dimension, i.e. the dimension which is reduced, which is annoying when dealing with arrays with multiple coordinates along each dimension.

Steps to reproduce:
```python
import plopp as pp
tof = sc.arange('t', 0, 10, 1, unit='s')
wavelengths = sc.arange('t', 0, 200, 20, unit='nm')
x = sc.arange('x', 0, 7, 1, unit='m')
y = sc.arange('y', 0, 7, 1, unit='m')
data = sc.ones(dims=['t', 'y', 'x'], shape=[10, 6, 6])
array = sc.DataArray(
    data=data,
    coords={
        'tof': tof,
        'y': y,
        'x': x,
        'wavelengths': wavelengths,
    },
)
pp.inspector(array, dim='t', coords=['x', 'y', 'tof'])
```
Error message:

```python
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[40], [line 16](vscode-notebook-cell:?execution_count=40&line=16)
     12         'x': x,
     13         'wavelengths': wavelengths,
     14     },
     15 )
---> [16](vscode-notebook-cell:?execution_count=40&line=16) pp.inspector(array, dim='t', coords=['x', 'y', 'tof'])

File c:\Users\christianvedel\EasyScienceSource\imaging-lib\.pixi\envs\default\Lib\site-packages\plopp\plotting\_inspector.py:361, in inspector(obj, dim, aspect, autoscale, cbar, clabel, cmax, cmin, continuous_update, coords, errorbars, figsize, grid, legend, logc, mask_cmap, mask_color, mode, nan_color, norm, operation, orientation, title, vmax, vmin, xlabel, xmax, xmin, ylabel, ymax, ymin, with_slider, **kwargs)
    339 f2d_args = dict(
    340     aspect=aspect,
    341     cbar=cbar,
   (...)    357     **kwargs,
    358 )
    360 if with_slider:
--> [361](file:///C:/Users/christianvedel/EasyScienceSource/imaging-lib/.pixi/envs/default/Lib/site-packages/plopp/plotting/_inspector.py:361)     slicer_plot = SlicerPlot(
    362         bin_edges_node, keep=set(data.dims) - {dim}, operation=operation, **f2d_args
    363     )
    364     f2d = slicer_plot.figure
    365     span = f1d.ax.axvspan(
    366         data.coords[dim].min().value,
    367         data.coords[dim].max().value,
   (...)    370         zorder=-np.inf,
    371     )

File c:\Users\christianvedel\EasyScienceSource\imaging-lib\.pixi\envs\default\Lib\site-packages\plopp\plotting\_slicer.py:237, in SlicerPlot.__init__(self, obj, coords, enable_player, keep, mode, operation, **kwargs)
    235     make_figure = partial(imagefigure, **args['2d'])
    236 else:
--> [237](file:///C:/Users/christianvedel/EasyScienceSource/imaging-lib/.pixi/envs/default/Lib/site-packages/plopp/plotting/_slicer.py:237)     raise ValueError(
    238         f'Slicer plot: the number of dims to be kept must be 1 or 2, '
    239         f'but {ndims} were requested.'
    240     )
    242 self.figure = make_figure(*self.slicer.reduce_nodes)
    243 require_interactive_figure(self.figure, 'slicer')

ValueError: Slicer plot: the number of dims to be kept must be 1 or 2, but 3 were requested.
```

