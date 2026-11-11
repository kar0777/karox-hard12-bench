You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Modular unit commitment: min_down_time caps status at one module

> _This issue was drafted by AI (Claude Code)._

### Version Checks

- [x] Checked that this issue has not already been reported (searched for `min_down_time` + `p_nom_mod`).
- [x] Confirmed on PyPSA 1.4.0 (latest release); the same code is on `master`.

### Issue Description

For a committable generator with modular unit commitment (`p_nom_mod` set, `status` integer in `0..p_nom/p_nom_mod`), any `min_down_time >= 1` caps the committed modules at **1**.

The min-down-time row in `pypsa/optimization/constraints.py` (loop over `("up", ..., bound 0)` / `("down", ..., bound 1)`) is

```
status_t + Σ_{k < min_down_time} shut_down_{t-k}  <=  1 - (past switches)
```

With binary status this is right. With modular status the right-hand side should be the number of modules `p_nom / p_nom_mod`. As it stands, `status <= 1` binds in every snapshot. The min-up-time row has bound 0 and is unaffected.

### Reproducible Example

```python
import pandas as pd
import pypsa

for mdt in [0, 1]:
    n = pypsa.Network()
    n.set_snapshots(pd.RangeIndex(4))
    n.add("Bus", "b")
    n.add("Load", "d", bus="b", p_set=[100, 150, 150, 100])
    n.add("Generator", "shed", bus="b", p_nom=1e3, marginal_cost=1e3)
    n.add("Generator", "g", bus="b", p_nom=150, p_nom_mod=50, committable=True,
          marginal_cost=10, min_down_time=mdt, up_time_before=0)
    n.optimize(solver_name="highs", solver_options={"output_flag": False})
    print(f"min_down_time={mdt}", "status:", n.generators_t.status["g"].tolist(),
          "shed:", n.generators_t.p["shed"].round(1).tolist())
```

Output on 1.4.0:

```
min_down_time=0 status: [2.0, 3.0, 3.0, 2.0] shed: [0.0, 0.0, 0.0, 0.0]
min_down_time=1 status: [1.0, 1.0, 1.0, 1.0] shed: [50.0, 100.0, 100.0, 50.0]
```

### Expected Behavior

With `min_down_time=1`, the result should equal the `min_down_time=0` case: status `[2, 3, 3, 2]` and no shedding. A shut-down module may not restart within `min_down_time`, but the other modules stay available. Suggested fix: use `p_nom / p_nom_mod` as the down-time bound for modular committables, and keep 1 otherwise.

Related: #1899 / #1901 (modular UC bounds), #1985 (ramp limits with modular UC).

### Installed Versions

pypsa 1.4.0, highspy (latest), Python 3.12, Linux.

