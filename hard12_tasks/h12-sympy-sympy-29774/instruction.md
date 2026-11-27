You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Exponentiating a matrix times scalar should distribute the exponent to the scalar.

Exponentiating a `MatrixSymbol` times a scalar does not distribute the power, whereas exponentiating symbol times noncommutative symbol does. I expect that matrix (MatMul) behavior should match that of symbol behavior.

Reproduction code:

```py
import sympy as sp
from sympy import Identity, MatrixSymbol, expand, symbols

n = symbols("n", integer=True, positive=True)
a = symbols("a")

B = MatrixSymbol("B", n, n)
x, y = symbols("x y", commutative=False)

print("scalar product:       ", expand((a * x * y) ** 2))
print("scalar-matrix product:", expand((a * B) ** 2))
```

SymPy 1.14.0 as well as current dev output df9ff3cf4b95371c4f2:

```
scalar product:        a**2*x*y*x*y
scalar-matrix product: (a*B)**2
```

In regular `Mul` this part is responsible for separating commutative and noncommutative parts:

https://github.com/sympy/sympy/blob/df9ff3cf4b95371c4f289fcaae9bfba45d2ef091/sympy/core/mul.py#L743-L748

In `MatMul` the implementation is generic:

https://github.com/sympy/sympy/blob/df9ff3cf4b95371c4f289fcaae9bfba45d2ef091/sympy/matrices/expressions/matexpr.py#L210-L215

**Related issues:**
- https://github.com/sympy/sympy/issues/10384 now more about argument validation
- https://github.com/sympy/sympy/issues/25554 seems reasonably close but not about the commutative part
- https://github.com/sympy/sympy/issues/23364 about differentiation of (scalar * matrix) powers. Closed but doesn't fix this issue.

**AI disclosure**
I adhere to the sympy AI usage policy. I used codex to construct the repro example and do the code dive. I confirmed the repro example behavior and confirmed that the relevant locations in the code are indeed responsible for the construction of the expressions (and that the overall content makes a lot of sense).
