You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Utilities/catalog] SafeLock race condition when analysing multiple realizations at the same time

### machine

Lumi

### catalog

climatedt-gen2

### version

main

### What happened?

When I run multiple aqua-analysis at the same time for multiple realizations, these will try to write to the catalogue at the same time. This results sometime in trouble, as shown by the log below.
Apparently our SafeLock is not that safe ...

### Code to reproduce the issue

```python

```

### Error messages

^[[37m2026-10-08 02:11:08 :: OutputSaver :: DEBUG    -> Locking catalog file /users/jvonhar/.aqua/catalogs/climatedt-gen2/catalog/IFS-NEMO-10km/baseline-hist.yaml^[[0m
Traceback (most recent call last):
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA-diagnostics/aqua/diagnostics/biases/cli_biases.py", line 210, in <module>
    main()
    ~~~~^^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA-diagnostics/aqua/diagnostics/biases/cli_biases.py", line 123, in main
    biases_dataset.compute_climatology(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        seasonal=seasons,
        ^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        areas=bool(show_stats),
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA-diagnostics/aqua/diagnostics/biases/climatology.py", line 277, in compute_climatology
    self.savenetcdf(
    ~~~~~~~~~~~~~~~^
        data=self.climatology,
        ^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        extra_keys=extra_keys,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA-diagnostics/aqua/diagnostics/biases/climatology.py", line 190, in savenetcdf
    super().save_netcdf(
    ~~~~~~~~~~~~~~~~~~~^
        data=data,
        ^^^^^^^^^^
    ...<6 lines>...
        extra_keys=extra_keys,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA-diagnostics/aqua/diagnostics/base/diagnostic.py", line 224, in save_netcdf
    return outputsaver.save_netcdf(
           ~~~~~~~~~~~~~~~~~~~~~~~^
        dataset=data,
        ^^^^^^^^^^^^^
    ...<4 lines>...
        extra_keys=extra_keys,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA-diagnostics/aqua/diagnostics/base/output_saver.py", line 303, in save_netcdf
    self._create_catalog_entry(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^
        metadata=metadata,
        ^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        wildcardlist=dict_catalog_entry.get("wildcardlist", None),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA-diagnostics/aqua/diagnostics/base/output_saver.py", line 569, in _create_catalog_entry
    with SafeFileLock(catalogfile + ".lock", loglevel=self.loglevel):
         ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA/aqua/core/lock/safelock.py", line 101, in __enter__
    self.acquire()
    ~~~~~~~~~~~~^^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA/aqua/core/lock/safelock.py", line 74, in acquire
    self._remove_stale()
    ~~~~~~~~~~~~~~~~~~^^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA/aqua/core/lock/safelock.py", line 46, in _remove_stale
    if self._is_stale():
       ~~~~~~~~~~~~~~^^
  File "/pfs/lustrep4/scratch/project_465002727/jvonhar/AQUA/aqua/core/lock/safelock.py", line 41, in _is_stale
    age = time.time() - os.path.getmtime(self.lock_path)
                        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "<frozen genericpath>", line 91, in getmtime
FileNotFoundError: [Errno 2] No such file or directory: '/users/jvonhar/.aqua/catalogs/climatedt-gen2/catalog/IFS-NEMO-10km/baseline-hist.yaml.lock'

### Are you interested in making a pull request?

None
