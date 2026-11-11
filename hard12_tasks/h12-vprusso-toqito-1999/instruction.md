You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

measured_relative_entropy returns wrong values or crashes when rho or sigma is not full rank

I was checking `measured_relative_entropy` against cases where the answer is known, and it goes wrong whenever `rho` or `sigma` is not full rank.

```python
import numpy as np
from toqito.state_metrics import measured_relative_entropy

rng = np.random.default_rng(0)
psi = rng.normal(size=2) + 1j * rng.normal(size=2)
psi /= np.linalg.norm(psi)
rho = np.outer(psi, psi.conj())          # pure state
A = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
sigma = A @ A.conj().T / np.trace(A @ A.conj().T)   # full rank

print(measured_relative_entropy(rho, sigma))   # 12.04
print(measured_relative_entropy(np.diag([1.0, 0.0]), np.eye(2) / 2))   # LinAlgError: singular matrix
print(measured_relative_entropy(np.diag([0.7, 0.3]), np.diag([1.0, 0.0])))   # OverflowError: cannot convert float infinity to integer
```

For the first case the right value is about 0.665: for a qubit, two-outcome projective measurements are enough, and a brute-force search over them gives 0.665. Another random pure state gives 15.90 instead of 0.884, and `|+><+|` against `I/2` gives 0.695 to 0.737 depending on the run, instead of ln 2. The second case should be ln 2 and the third should be `inf`, since the support of `rho` is not inside the support of `sigma`.

The cause is `_compute_a`. It inverts `sqrtm(rho)` to get the eigenvalues of `rho^{-1/2} sigma rho^{-1/2}`, which only exist when `rho` is positive definite. For a singular `rho`, `scipy.linalg.inv` either raises, or (when the zero eigenvalue is only zero up to rounding) returns a huge matrix, so `(m, k)` is chosen from a meaningless `a` and the SDP's error bound no longer holds. When `sigma` is singular, `1 / eigs.min()` is `inf` and `int(np.ceil(...))` overflows.

What I'd propose:

1. Return `np.inf` when the support of `rho` is not contained in the support of `sigma` (a measurement onto the kernel of `sigma` then has `q = 0` and `p > 0`).
2. Raise a clear `ValueError` when `rho` or `sigma` is singular otherwise, instead of returning a wrong number. If you'd rather support these inputs, I could restrict both to the support of `sigma` when that's exact, but a singular `rho` still needs some other way to pick `(m, k)`, and I'm not sure which you'd prefer.

I'm happy to open a PR for this. toqito 1.3.1 from `master` (`4baf22e6`), numpy 2.5.4, cvxpy 1.9.3, Python 3.12, Windows.

