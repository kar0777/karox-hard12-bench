You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

toml postargs: passed as str not list from cli


Say you have something like this..

```toml
commands = [[
    "pylint",
    "--",
    { replace = "posargs", default = ["tests"], extend = true }
]]
```

If you try to run: 
   `tox -- tests src` 
it will throw an error like: 
    `ERROR: file or directory not found: tests src` 
and the pytest command looks like 
    `testenv: commands[0]> pytest -- 'tests src'`
it's treating 'tests src' as a single argument.

(tox 4.60.1, python 3.14)

I would expect it to pass the values as separate arguments

`testenv: commands[0]> pytest -- 'tests' 'src'`
