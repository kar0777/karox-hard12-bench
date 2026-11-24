You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Implement a search by comment function

## Is your feature request related to a problem? Please describe.

Many times MCNP objects are identifiable by their comments, and less so their number. It's desirable to be able to find objects by what their comments contain. 



## Describe the solution you'd like

I was thinking in `NumberedObjectCollection` (also it may be time to make `MCNP_Problem.data_inputs` its own class) of implementing something like:

``` python
import re

def get_by_comment(self, searcher: str | re.Pattern): -> Generator[MCNP_Object, None, None]
     pass
```

Or also possible following `montepy.Materials.get_containing_(all|any)` where you can search by multiple strings. 

## Describe alternatives you've considered

For now users can just do this manually (after #972).

## Additional context

This is a follow-on to #185.


