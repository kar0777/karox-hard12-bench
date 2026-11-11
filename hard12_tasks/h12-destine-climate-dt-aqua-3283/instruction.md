You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Intake] Fix precedence of user kwargs over xarray catalog defaults

### machine

Others: local macOS; the collision is independent of machine.

### catalog

ci / any catalog containing `xarray_kwargs` defaults.

### version

main (after #3161)

### What happened?

Review finding B7 from #3161 affects the STAC, NetCDF, and Zarr Intake drivers. They construct readers with separate `**xarray_kwargs` and `**kwargs` expansions. If a catalog supplies `xarray_kwargs.chunks` and the user supplies `chunks`, Python raises a duplicate-keyword TypeError before any data is read. Other repeated options have the same problem.

Expected precedence: explicit source/Reader kwargs override the catalog's `xarray_kwargs`, which override driver defaults. Explicit `chunks=None` must survive, and chunk mappings should be replaced as a whole. Merge without changing either input dictionary. Expose those same effective options through the source's `xarray_kwargs` attribute, which BackendIntakeXarray uses again when reading; otherwise a stale catalog value can undo the override.

### Code to reproduce the issue

```python
from aqua.core.intake_drivers.xarray import IntakeNetCDFSource

# Fails at construction, before opening the path.
source = IntakeNetCDFSource(
    "dummy.nc",
    xarray_kwargs={"chunks": {"time": 12}},
    chunks={"time": 1},
)
```

The same conflicting arguments affect IntakeZarrSource and IntakeSTACSource.

### Error messages

```text
TypeError: ... got multiple values for keyword argument 'chunks'
```

### Are you interested in making a pull request?

Yes. Use a small shared helper in the existing xarray adapter module, apply it to all three drivers, document precedence, and add parametrized coverage for catalog-only options, runtime overrides, explicit None, effective backend read options, and unchanged inputs. Track this separately from the remaining STAC fixes in #3281.

