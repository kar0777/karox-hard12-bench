You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

fcode: numerically-folded function base loses parentheses under a power, flipping the sign

`fcode` emits a numerically-folded function base unparenthesised under a power, which flips the sign in the generated Fortran.

When a known function has all-`Number` arguments, `CodePrinter._print_Function` folds it to a numeric literal. If that literal is negative and the function sits under a `Pow`, `_print_Pow` does not parenthesise it, because `precedence()` is asked about the *expression* (`sin`, `PRECEDENCE["Func"]` = 70) rather than about the *text* that was emitted (a unary minus). Fortran binds `**` tighter than unary minus, so `-a**2` parses as `-(a**2)`.

The result is valid Fortran that compiles without a warning and returns the wrong sign.

### Reproduce

```python
from sympy import Float, cos, pi, sin
from sympy.printing.fortran import fcode

e = sin(Float("1.265344399150595") - Float("0.5") * pi)   # stays an unevaluated sin(...)

print(fcode(e ** 2, source_format="free", standard=95))
# -0.30072421433515855d0**2

print(float(e ** 2))
# 0.09043505308749838      <- what sympy means
# -0.09043505308749834     <- what the emitted Fortran computes
```

Also reproduces without `sin`:

```python
print(fcode(cos(Float("1.0") * 2 * pi / 3) ** 2, source_format="free", standard=95))
# -0.4999999999999999d0**2
```

And in context, where it is much harder to spot — this came out of `autowrap` on a kinematic chain, via `cos(asin(x))` auto-rewriting to `sqrt(1 - x**2)`:

```python
from sympy import asin, atan, cos, pi, sin, sqrt
from sympy.printing.fortran import fcode

crank, short_side, long_side = 0.221, 0.06646, 0.21077
coupler_angle = pi / 2.0 - atan(long_side / short_side)
coupler_length = sqrt(short_side ** 2 + long_side ** 2)
x = -crank * cos(asin(coupler_length * sin(coupler_angle) / crank))

print(fcode(x, source_format="free", standard=95))
# -0.221d0*sqrt(1 - 0.999998454167605d0*-0.3007242143351585d0**2)
print(float(x))
# -0.21077017910510965   sympy
# -0.23077680...         the emitted Fortran, a 20.007 mm error in our units
```

### Expected

```
(-0.30072421433515855d0)**2
```

### Not a general parenthesisation failure

Bases that are negative *as expressions* are handled correctly, which is why this is easy to miss:

```python
from sympy import Float, Integer, Mul, Pow, Symbol

fcode(Pow(Float("-0.3"), Integer(2), evaluate=False))                        # (-0.3d0)**2   OK
fcode(Pow(Mul(Integer(-1), Symbol("x"), evaluate=False), Integer(2), evaluate=False))  # (-x)**2  OK
```

The difference is that `precedence(Float(-0.3))` reports `Add`-level, while `precedence(sin(...))` reports `Func`-level even though the emitted text is `-0.3007...`.

### Other printers

Unaffected, because they do not fold to a bare literal in this position:

```
ccode       -> pow(sin(1.265344399150595 - 0.5*M_PI), 2)
julia_code  -> sin(1.265344399150595 - 0.5 * pi) ^ 2
octave_code -> sin(1.265344399150595 - 0.5*pi)^2
```

I have not checked every printer that emits `**` or `^`; anything sharing Fortran's precedence for it and the same folding is worth checking too.

### Where

`FCodePrinter._print_Pow` (`sympy/printing/fortran.py:338`) delegates to `CodePrinter._print_Pow`, whose `parenthesize(expr.base, PREC)` decides from `precedence(expr.base)`. On `master` this code is byte-identical to 1.14.0, so it still applies.

Two possible fixes, depending on where you would rather have it:

1. In `_print_Pow`, parenthesise when the *printed* base begins with `-` (fixes the symptom wherever the folding happens).
2. Fold the base to a `Number` before the precedence decision is made, so `precedence()` sees the negative number it will actually print.

### Environment

- SymPy 1.14.0, Python 3.12.7, Linux
- `master`'s `fortran.py` `_print_Pow` unchanged, so presumably still reproduces there

Happy to open a PR for whichever of the two approaches you prefer.

