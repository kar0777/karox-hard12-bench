You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Inproper error message for LimitedChoice when all grouped agument are boolean values

# Version

Python 3.13.11
cyclopts 5.3.2

# TL;DR
LimitedChoice doesn't work with boolean flags, pardon my unemployment for this long issue.

# Explanation
I'm currently refactoring the logic of this particular command

```python
import sys
import cyclopts
from cyclopts import Parameter, Group
from cyclopts.validators import MutuallyExclusive, LimitedChoice
from rich import print as r_print
from typing import Annotated, Sequence, Any, Optional, Literal


app = cyclopts.App(name="Descartes", alias="dkrt", help="French maxxed CLI for managing task via Markdown tables")


add_mode_group = Group("mandatory flags for additions", validator=LimitedChoice(min=1, max=1))


@app.command()
def add_v2(data: Annotated[
    str,
    Parameter(help="String that is either the path to the .toml file or the list to add")
],
           task_file: Annotated[
               str | None,
               Parameter(help="Name of the task file, defaults to the closest one")
           ] = None,
           /,
           *,
           formatted_list: Annotated[
               bool,
               Parameter(name=("--list", "-l"),
                         group=add_mode_group,
                         help="Tells to Descartes that data is a formatted string (i.e. a single separator le a CSV line) to fill in the table.")
           ] = False,
           file_path: Annotated[
               bool,
               Parameter(name=("--file", "-f"),
                         group=add_mode_group,
                         help="Tells to Descartes that data is the path to the Descartes-specific TOML file that will be read as the source"),
           ] = False,
           table: Annotated[
               bool | None,
               Parameter(alias="-t",
                         negative="-no-t",
                         help="Defines whether the addition should link a TODO.md file with a table or not\n"
                              f"see [link={Path('ajout.md').resolve().as_uri()}]ajout.md[/link]")
           ] = None):
    """Command to add rows, either from a formatted string
    or from a TOML file.
    The status is serialized: it must be included in the STATUT Enum,
    but a STATUT_BALISE tag is also accepted.
    """
```
I'm working on flag behavior
as you can see I include **--file** and **--list** in the Group  AND put False as default value but the problem stay with True.
For context, the -l and -f flag are used to tells to the program how to treat the string passed in the data argument,
so one is mandatory but only one is needed.
I tried this :
```python
(base) (descartes) PS A:\descartes> dkrt ajout-v2 "add unit test for add command,1,-d,unit_test_add" -no-t
and get this message
╭─ Error ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Invalid values for group Mandatory flags for add command. Received 0 arguments: {}. Only [1, 1] choices may be specified.                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
I was waiting this : 
```python
(base) (descartes) PS A:\descartes> dkrt ajout-v2 "add unit test for add command,1,-d,unit_test_add" -no-t
and get this message
╭─ Error ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Invalid values for group Mandatory flags for add command. Received 0 arguments: {--liste,--file}. Only [1, 1] choices may be specified.                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
It should have been produce if I understand correctly this : 

```python
    """class LimitedChoice
        [...]"""
    def __call__(self, argument_collection: "ArgumentCollection"):
        group_size = len(argument_collection)
        print([a._value.__mro__ for a in argument_collection])
        populated_argument_collection = argument_collection.filter_by(value_set=True)
        n_arguments = len(populated_argument_collection)

        if self.allow_none and n_arguments == 0:
            return
        elif self.min < 0:
            # Require all arguments in the group to be supplied.
            if group_size == n_arguments:
                return
            all_names = {a.name for a in argument_collection}
            supplied_names = {a.name for a in populated_argument_collection}
            missing_names = sorted(all_names - supplied_names)
            if len(missing_names) == 1:
                raise ValueError(f"Missing argument: {missing_names[0]}")
            else:
                raise ValueError(f"Missing arguments: {missing_names}")
        elif self.min <= n_arguments <= self.max:
            return
        else:
            offenders = (
                "{"
                + ", ".join(
                    a.tokens[0].keyword if (a.tokens and a.tokens[0].keyword) else a.name
                    for a in populated_argument_collection
                )
                + "}"
            )
            if self.min == 0 and self.max == 1:
                raise ValueError(f"Mutually exclusive arguments: {offenders}")
            else:
                raise ValueError(
                    f"Received {n_arguments} arguments: {offenders}. Only [{self.min}, {self.max}] choices may be specified."
                )
```

I investigate the LimitedChoice class and find the problem because it was pretty trivial 
````python
    def __call__(self, argument_collection: "ArgumentCollection"):
        group_size = len(argument_collection)
        print([a._value for a in argument_collection])
        populated_argument_collection = argument_collection.filter_by(value_set=True)
        n_arguments = len(populated_argument_collection)
    #[<UNSET>, <UNSET>]
````
Unfortunately I don't have time to go deeper inside the OOP layer more than using \_\_mro__ dunder

````python
print([a._value.__mro__ for a in argument_collection])
#[(<UNSET>, <Sentinel>, <class 'object'>), (<UNSET>, <Sentinel>, <class 'object'>)]
````
As I understand now after analyzing LimitedChoice's documentation verbatim there is a problem with using LimitedChoice with boolean flag.
Since validating this kind of boolean logic is trivial code I don't know if it's a voluntary design or you wanted to fix this.

