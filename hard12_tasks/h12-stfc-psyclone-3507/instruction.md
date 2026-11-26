You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Derived types and initialisers

Consider the program:

```fortran
module pair
  type :: pair
    integer :: x, y
  end type
  type(pair) :: p = pair(1, 2)
end module
```

In the PSyIR symbol table for this module, the variable `p` is an `UnsupportedFortranType`. The reason is that the datatype of `p` does not pass the following check in the frontend:

  https://github.com/stfc/PSyclone/blob/2c736380cc11bd5138629e34734acc76342e794e/src/psyclone/psyir/frontend/fparser2.py#L2207-L2210

It's not clear to me whether the behaviour is intentional or not. If we wanted to allow `p` to have an initial value then we'd have to allow allow `DataTypeSymbol` in the check and also allow `Call` as a valid node inside the `DataSymbol.initial_value` setter. Would this be somehow bad?  It would permit some invalid Fortran, such as calling a function rather than a data constructor, but that could be potentially checked by the frontend or permitted under the assumption that the input code is valid fortran without leading to major issues?

I encountered this issue while trying to understand why the following program gives an error:

```fortran
module pair
  type :: pair
    integer :: x, y
  end type
  type(pair) :: ps(1) = [pair(1, 2)]
end module
```

This program passes the frontend check (because it's an array not a `DataTypeSymbol`) but then hits the lack of support for `Call` in  `DataSymbol.initial_value`. I'm trying to figure out what might be the right current solution for PSyclone:

1. allow `Call` nodes in initial values, or
2. disallow initial values for derived types.
