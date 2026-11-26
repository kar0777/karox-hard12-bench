You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add cell.is_mass_dens

## Is your feature request related to a problem? Please describe.

I was trying to free-hand code and I first attempted `cell.is_mass_dens` instead of the correct, `cell.is_atom_dens`. Also sometimes for me saying `not cell.is_atom_dens` takes me an extra second to comprehend.


## Describe the solution you'd like

I'd like to add the simple propery:

``` python

class Cell:
    ...

    @propety
    def is_mass_dens(self):
         return not self.is_atom_dens
```

## Describe alternatives you've considered

Keep the status quo.

