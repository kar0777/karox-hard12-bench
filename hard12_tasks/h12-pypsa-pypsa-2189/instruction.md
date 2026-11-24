You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Function build_linexpr_from_weights() in MGA not aligned to newest Linopy "v1" semantics?

### Version Checks (indicate both or one)

- [x] I have confirmed this bug exists on the lastest [release](https://github.com/pypsa/pypsa/releases) of PyPSA.

- [ ] I have confirmed this bug exists on the current [`master`](https://github.com/pypsa/pypsa/tree/master) branch of PyPSA.


### Issue Description

After updating both PyPSA and Linopy to their latest versions, I have noticed warnings appearing when using the `build_linexpr_from_weights()` function, part of the [MGA code](https://github.com/PyPSA/PyPSA/blob/master/pypsa/optimization/mga.py). The warnings are, for instance, like the one below:

```
LinopySemanticsWarning: Coordinate mismatch in merge along dim '_term' silently aligned by legacy (positional when sizes match, otherwise outer join by label). Under v1 this raises ValueError.
 Dim: 'name': left=['OCGT', 'solar_bus1', 'wind_bus1', 'solar_bus2', 'wind_bus2'], right=['battery_bus1', 'battery_bus2']
 Resolve: `.sel(...)` / `.reindex(...)` to align
 `.assign_coords(...)` to relabel one side
 `linopy.align(...)` to pre-align several operands
 or pass an explicit `join=` argument.
 Opt in: linopy.options['semantics'] = 'v1'
 Silence: warnings.filterwarnings('ignore', category=LinopySemanticsWarning)
 return merge(expr)
```

If forcing the "v1" semantics of Linopy via `linopy.options["semantics"] = "v1"`, the warning becomes an error that breaks the code:

```
ValueError: Coordinate mismatch on shared dimension 'name': left=['OCGT', 'solar_bus1', 'wind_bus1', 'solar_bus2', 'wind_bus2'], right=['battery_bus1', 'battery_bus2']. Resolve with `.sel(...)`
```

I understand the problem is a simple missing update on the last line of the `build_linexpr_from_weights()`, where `return merge(expr)` should be something like: `return merge(expr, join="outer")`, as per the recommendations in the [documentation](https://linopy.readthedocs.io/en/latest/user-guide/migrating-to-v1/).



### Reproducible Example

```python
import pypsa
n = pypsa.examples.model_energy()
n.optimize()
weights = {"Generator": {"p_nom": {"wind": 1}}, "StorageUnit": {"p_nom": {"battery storage": 1}}}
n.optimize.optimize_mga(slack=0.05, weights=weights, sense="min")
```

### Expected Behavior

```
ValueError: Coordinate mismatch on shared dimension 'name': left=['wind', 'solar'], right=['battery storage']. Resolve with `.sel(...)` 
```

### Installed Versions

<details>
PyPSA: 1.4.0
Linopy: 0.10.1
</details>

