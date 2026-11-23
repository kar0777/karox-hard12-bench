You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

compute_fpp returns a larger value than compute_fvar for white noise

**Gammapy version**
main at 37288a67. The line in question has not changed since `compute_fpp` was added in #4726.

**Bug description**
`compute_fpp` divides the sum of squared differences of consecutive points by `N - 1`. Eq. 3 of Edelson et al. (2002), which the docstring cites, has `2 (N - 1)`. For white noise `E[(x_{i+1} - x_i)^2] = 2 sigma^2`, so F_pp comes out too large.

**Expected behavior**
The docstring says F_pp and F_var give the same value for white noise.

**To Reproduce**
```python
import numpy as np
from gammapy.stats import compute_fvar, compute_fpp

rng = np.random.default_rng(0)
flux = 10 + rng.normal(0, 2, 200_000) + rng.normal(0, 1, 200_000)  # intrinsic sigma 2, errors 1
flux_err = np.full(flux.size, 1.0)

print(compute_fvar(flux, flux_err)[0], compute_fpp(flux, flux_err)[0])
```
Expected about 0.2 for both. Output: `0.2000516...  0.3004934...`

**Other information**
I found this while reading the code. The fix is one line plus updated tests, and I am happy to open a PR.

