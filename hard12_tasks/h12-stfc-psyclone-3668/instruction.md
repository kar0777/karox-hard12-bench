You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

PSyclone loses things at the end of a subroutine (e.g. bind)

```
subroutine x() bind(c)
  integer :: i
  integer, pointer, dimension(:, :) :: a => null()


end subroutine x
```

results in

```
subroutine x()
  integer :: i
  integer, pointer, dimension(:, :) :: a => null()


end subroutine x
```
which is a bit naughty.
