You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Most methods on `QQ.algebraic_field(sqrt(2), sqrt(5))` fail, many computations on algebraic fields in general seem wrong

On `sympy==1.14.0`:

```python
from sympy import QQ, sqrt
from sympy import __version__ as sympy_version
print(sympy_version)

# example from the docs
K3 = QQ.algebraic_field(sqrt(2), sqrt(3))
print(K3.discriminant())  # 2304, correct
print(K3.integral_basis()) # looks equivalent to (1,sqrt(2),sqrt(3),sqrt(6))

K5 = QQ.algebraic_field(sqrt(2), sqrt(5))
print(K5.discriminant()) # exception
print(K5.integral_basis()) # exception
```

Although the constructor goes through with no hitch, both methods on `K5` fail with a cryptic `sympy.polys.polyerrors.CoercionFailed: Cannot convert 1/3 of type <class 'sympy.external.pythonmpq.PythonMPQ'> from QQ to ZZ`.

Some more complex extensions like `QQ.algebraic_field(sqrt(2), 2*cos(2*pi/7))` seemingly work without raising exceptions, but the results are definitely incorrect:

```python
>>> QQ.algebraic_field(sqrt(2), 2*cos(2*pi/7)).discriminant()
0
```

should be certainly non-zero.
