You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Can't plot anything without ipywidgets?

I do my scientific work without Ipython / Jupyter Notebook and all that Jazz - I use plain Python scripts and [Tmux](https://github.com/tmux/tmux) & a terminal editor.

Something is wrong with `plopp` backend resolution, as the following:

```sh
python -c 'import scipp as sc; sc.arange("x", 5.0).plot()'
```

Fails with:

```python
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import scipp as sc; sc.arange("x", 5.0).plot()
                        ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\msys64\home\owner\repos\calibrate-reprate\.venv\Lib\site-packages\scipp\plotting.py", line 14, in plot
    return _plot(*args, **kwargs)
  File "C:\msys64\home\owner\repos\calibrate-reprate\.venv\Lib\site-packages\plopp\plotting\_plot.py", line 182, in plot
    return linefigure(*nodes, **args['1d'])
  File "C:\msys64\home\owner\repos\calibrate-reprate\.venv\Lib\site-packages\plopp\graphics\figures.py", line 31, in linefigure
    return backends.get(group='2d', name='figure')(view_maker, *nodes, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\msys64\home\owner\repos\calibrate-reprate\.venv\Lib\site-packages\plopp\backends\matplotlib\figure.py", line 222, in Figure
    return InteractiveFigure(*args, **kwargs)
  File "C:\msys64\home\owner\repos\calibrate-reprate\.venv\Lib\site-packages\plopp\backends\matplotlib\figure.py", line 134, in __init__
    from ...widgets import HBar, VBar, make_toolbar_canvas2d
  File "C:\msys64\home\owner\repos\calibrate-reprate\.venv\Lib\site-packages\lazy_loader\__init__.py", line 78, in __getattr__
    submod = importlib.import_module(submod_path)
  File "C:\Users\owner\AppData\Local\Programs\Python\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\msys64\home\owner\repos\calibrate-reprate\.venv\Lib\site-packages\plopp\widgets\box.py", line 4, in <module>
    from ipywidgets import HBox, VBox, Widget
ModuleNotFoundError: No module named 'ipywidgets'
```
