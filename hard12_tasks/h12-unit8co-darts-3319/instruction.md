You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add a signed percentage bias metric (or signed=True option in ope) to darts.metrics

### Is your feature request related to a problem?

In demand forecasting and S&OP (Sales & Operations Planning), evaluating accuracy with magnitude metrics like `wmape` or `mae` is always paired with a **signed percentage bias metric** to diagnose systematic over-forecasting ($+$, excess inventory risk) versus under-forecasting ($-$, stockout risk).

Currently, `darts.metrics` provides:
- `wmape` ($100 \cdot \frac{\sum |y - \hat{y}|}{\sum |y|}$) — unsigned
- `ope` ([`darts/metrics/metrics.py` L2081–L2147](https://github.com/unit8co/darts/blob/master/darts/metrics/metrics.py#L2081-L2147), $100 \cdot \left|\frac{\sum y - \sum \hat{y}}{\sum y}\right|$) — takes `np.abs(...)` at L2143, so the sign (direction of bias) is lost
- `merr` ($\frac{1}{T}\sum (y - \hat{y})$) — signed, but in raw scale units rather than percentage, so it cannot be aggregated or compared across SKUs with different volume scales

Because `ope` applies `np.abs()`, there is currently no built-in metric in `darts.metrics` that returns a **signed percentage bias**.

### Describe the solution you'd like

Provide a signed percentage bias metric in `darts.metrics`, for example via one (or both) of the following approaches:

1. **Add a signed percentage bias function** (e.g., `mpe` or `wpe` / `pbias` / `signed_wmape`):
   $$\text{Bias\%} = 100 \cdot \frac{\sum_{t=1}^{T} (\hat{y}_t - y_t)}{\sum_{t=1}^{T} |y_t|} \quad \text{or} \quad 100 \cdot \frac{\sum_{t=1}^{T} (y_t - \hat{y}_t)}{\sum_{t=1}^{T} y_t}$$
   Sharing the same denominator ($\sum |y_t|$) as `wmape` makes it directly comparable to `wmape` (where $|\text{Bias\%}| \le \text{WMAPE}$) and robust when individual time steps have zeros.
2. **Or add a `signed: bool = False` parameter to `ope()`**:
   In `ope()` (`darts/metrics/metrics.py` L2143), allow `signed=True` to skip `np.abs()` and return the signed overall percentage error while keeping `signed=False` as the default for backward compatibility.

