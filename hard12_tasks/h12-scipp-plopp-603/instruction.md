You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

test_move_cut fails on Python 3.14

FYI:

```py
=================================== FAILURES ===================================
________________________________ test_move_cut _________________________________

    def test_move_cut():
        da = scatter()
        fig = scatter3dfigure(Node(da), x='x', y='y', z='z', cbar=True)
        clip = ClippingPlanes(fig)
        clip.add_x_cut.click()
        xcut = clip.cuts[-1]
        assert xcut.outlines[0].position[0] == xcut.slider.value[0]
        assert xcut.outlines[1].position[0] == xcut.slider.value[1]
        pts = list(fig.artists.values())[-1]
        npoints = pts._data.shape[0]
>       xcut.slider.value = [xcut.slider.min, xcut.slider.value[1]]
        ^^^^^^^^^^^^^^^^^

tests/widgets/clip3d_test.py:52: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/nix/store/i7lysg4h0dccnxkxx2m2pbn67pdzlzm4-python3.14-traitlets-5.14.3/lib/python3.14/site-packages/traitlets/traitlets.py:716: in __set__
    self.set(obj, value)
/nix/store/i7lysg4h0dccnxkxx2m2pbn67pdzlzm4-python3.14-traitlets-5.14.3/lib/python3.14/site-packages/traitlets/traitlets.py:706: in set
    obj._notify_trait(self.name, old_value, new_value)
/nix/store/i7lysg4h0dccnxkxx2m2pbn67pdzlzm4-python3.14-traitlets-5.14.3/lib/python3.14/site-packages/traitlets/traitlets.py:1513: in _notify_trait
    self.notify_change(
/nix/store/ks44k0nb3ka3c92qhav1w4a5w1hfvkcd-python3.14-ipywidgets-8.1.7/lib/python3.14/site-packages/ipywidgets/widgets/widget.py:701: in notify_change
    super().notify_change(change)
/nix/store/i7lysg4h0dccnxkxx2m2pbn67pdzlzm4-python3.14-traitlets-5.14.3/lib/python3.14/site-packages/traitlets/traitlets.py:1525: in notify_change
    return self._notify_observers(change)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/nix/store/i7lysg4h0dccnxkxx2m2pbn67pdzlzm4-python3.14-traitlets-5.14.3/lib/python3.14/site-packages/traitlets/traitlets.py:1568: in _notify_observers
    c(event)
/nix/store/dqbgkmik163hrjsdcwa4qf3l28yw1lws-python3.14-plopp-25.11.0/lib/python3.14/site-packages/plopp/widgets/clip3d.py:177: in move
    self._throttled_update()
/nix/store/dqbgkmik163hrjsdcwa4qf3l28yw1lws-python3.14-plopp-25.11.0/lib/python3.14/site-packages/plopp/widgets/debounce.py:51: in debounced
    timer.start()
/nix/store/dqbgkmik163hrjsdcwa4qf3l28yw1lws-python3.14-plopp-25.11.0/lib/python3.14/site-packages/plopp/widgets/debounce.py:23: in start
    self._task = asyncio.ensure_future(self._job())
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/nix/store/pmb8clh66mryha2ijzz3dg969drrkgj7-python3-3.14.2/lib/python3.14/asyncio/tasks.py:730: in ensure_future
    loop = events.get_event_loop()
           ^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <asyncio.unix_events._UnixDefaultEventLoopPolicy object at 0x7ffdf6f78ad0>

    def get_event_loop(self):
        """Get the event loop for the current context.
    
        Returns an instance of EventLoop or raises an exception.
        """
        if self._local._loop is None:
>           raise RuntimeError('There is no current event loop in thread %r.'
                               % threading.current_thread().name)
E           RuntimeError: There is no current event loop in thread 'MainThread'.

/nix/store/pmb8clh66mryha2ijzz3dg969drrkgj7-python3-3.14.2/lib/python3.14/asyncio/events.py:715: RuntimeError
=========================== short test summary info ============================
SKIPPED [5] tests/plotting/plot_1d_test.py:24: Skipping because kaleido is not installed
SKIPPED [1] tests/plotting/plot_1d_test.py:360: Log scale with datetime not supported in plotly
SKIPPED [1] tests/plotting/plot_1d_test.py:375: Log scale with datetime not supported in plotly
SKIPPED [1] tests/plotting/plot_1d_test.py:390: Log scale with datetime not supported in plotly
FAILED tests/widgets/clip3d_test.py::test_move_cut - RuntimeError: There is no current event loop in thread 'MainThread'.
================== 1 failed, 1204 passed, 8 skipped in 54.87s ==================
Traceback (most recent call last):
  File "/nix/store/pmb8clh66mryha2ijzz3dg969drrkgj7-python3-3.14.2/lib/python3.14/_py_warnings.py", line 856, in _warn_unawaited_coroutine
    _wm.warn(
    ~~~~~~~~^
        msg, category=RuntimeWarning, stacklevel=2, source=coro
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
RuntimeWarning: coroutine 'Timer._job' was never awaited

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/pytest/__main__.py", line 9, in <module>
    raise SystemExit(pytest.console_main())
                     ~~~~~~~~~~~~~~~~~~~^^
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/config/__init__.py", line 201, in console_main
    code = main()
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/config/__init__.py", line 175, in main
    ret: ExitCode | int = config.hook.pytest_cmdline_main(config=config)
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/nix/store/96vzxj35a0jjk3cwrp9jd90agvs3zmmh-python3.14-pluggy-1.6.0/lib/python3.14/site-packages/pluggy/_hooks.py", line 512, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/nix/store/96vzxj35a0jjk3cwrp9jd90agvs3zmmh-python3.14-pluggy-1.6.0/lib/python3.14/site-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/nix/store/96vzxj35a0jjk3cwrp9jd90agvs3zmmh-python3.14-pluggy-1.6.0/lib/python3.14/site-packages/pluggy/_callers.py", line 167, in _multicall
    raise exception
  File "/nix/store/96vzxj35a0jjk3cwrp9jd90agvs3zmmh-python3.14-pluggy-1.6.0/lib/python3.14/site-packages/pluggy/_callers.py", line 121, in _multicall
    res = hook_impl.function(*args)
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/main.py", line 336, in pytest_cmdline_main
    return wrap_session(config, _main)
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/main.py", line 331, in wrap_session
    config._ensure_unconfigure()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/config/__init__.py", line 1131, in _ensure_unconfigure
    self._cleanup_stack.close()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/nix/store/pmb8clh66mryha2ijzz3dg969drrkgj7-python3-3.14.2/lib/python3.14/contextlib.py", line 627, in close
    self.__exit__(None, None, None)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/nix/store/pmb8clh66mryha2ijzz3dg969drrkgj7-python3-3.14.2/lib/python3.14/contextlib.py", line 619, in __exit__
    raise exc
  File "/nix/store/pmb8clh66mryha2ijzz3dg969drrkgj7-python3-3.14.2/lib/python3.14/contextlib.py", line 604, in __exit__
    if cb(*exc_details):
       ~~^^^^^^^^^^^^^^
  File "/nix/store/pmb8clh66mryha2ijzz3dg969drrkgj7-python3-3.14.2/lib/python3.14/contextlib.py", line 482, in _exit_wrapper
    callback(*args, **kwds)
    ~~~~~~~~^^^^^^^^^^^^^^^
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/unraisableexception.py", line 95, in cleanup
    collect_unraisable(config)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/unraisableexception.py", line 79, in collect_unraisable
    raise errors[0]
  File "/nix/store/87niicfndnfqsi1wvjkzzh05fg8y7jhb-python3.14-pytest-8.4.2/lib/python3.14/site-packages/_pytest/unraisableexception.py", line 67, in collect_unraisable
    warnings.warn(pytest.PytestUnraisableExceptionWarning(msg))
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pytest.PytestUnraisableExceptionWarning: Exception ignored while finalizing coroutine <coroutine object Timer._job at 0x7ffdfe6f8ee0>: None
```

Reference:

-  https://github.com/NixOS/nixpkgs/pull/482111
