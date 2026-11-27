You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ArrowStringArray from NetCDF loading breaks optimize() on pandas >= 2.0

## Description

Networks loaded from `.nc` files with **pandas >= 2.0** have Arrow-backed string columns and indices (`ArrowStringArray`). When these are passed to `optimize()`, xarray/linopy operations fail or produce incorrect results because `ArrowStringArray` doesn't behave identically to object-dtype strings for index operations.

This silently affects all users who:
1. Save a network with `network.export_to_netcdf()`
2. Reload it with `pypsa.Network("network.nc")`
3. Call `network.optimize()` or operate on the reloaded network

## Reproduction

```python
import pypsa
import pandas as pd

# Create and solve a simple network
n = pypsa.Network()
n.set_snapshots(pd.date_range("2025-01-01", periods=24, freq="h"))
n.add("Bus", "bus0")
n.add("Generator", "gen0", bus="bus0", p_nom=100, marginal_cost=10)
n.add("Load", "load0", bus="bus0", p_set=50)

n.optimize(solver_name="highs")
n.export_to_netcdf("test_network.nc")

# Reload — indices are now ArrowStringArray
n2 = pypsa.Network("test_network.nc")
print(type(n2.generators.index.values))  # <class 'pandas.core.arrays.string_arrow.ArrowStringArray'>

# Operations on n2 may fail or behave unexpectedly
# e.g. network.copy() + bus remapping + optimize() in redispatch patterns
```

## Current workaround

We convert Arrow strings to object dtype manually after loading:

```python
def _convert_arrow_strings(network):
    """Convert ArrowStringArray columns/indices to regular object dtype."""
    for c in network.components:
        df = c.static
        if not df.empty:
            if isinstance(df.index.values, pd.arrays.ArrowStringArray):
                c.static.index = pd.Index(df.index.astype(object))
            for col in df.columns:
                if isinstance(df[col].values, pd.arrays.ArrowStringArray):
                    c.static[col] = df[col].astype(object)
        for key in c.dynamic:
            dyn_df = c.dynamic[key]
            if isinstance(dyn_df, pd.DataFrame) and not dyn_df.empty:
                if isinstance(dyn_df.columns.values, pd.arrays.ArrowStringArray):
                    c.dynamic[key].columns = pd.Index(dyn_df.columns.astype(object))
```

This must be called after every `pypsa.Network()` load from NetCDF and after every `network.copy()` + `remove()`/`add()` operation (which can reintroduce Arrow strings).

## Proposed fix

Handle Arrow-to-object conversion automatically in `Network.import_from_netcdf()` or at the start of `optimize()`, so users don't need a manual workaround.

**Effort**: Low — add the conversion to the NetCDF import path.
**Benefit**: Prevents silent failures for all users on pandas >= 2.0 who load from NetCDF.

## Environment

- pandas: 2.2+ (Arrow strings enabled by default)
- PyPSA: 0.31.x (also applies to 1.0+)
- Python: 3.11+
