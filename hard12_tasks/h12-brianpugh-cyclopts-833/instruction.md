You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Allow overriding default value in `--help`

I would like to override what is shown in `--help` as the default. In my use case, I define a few `Path` arguments and each of them is resolved later, so I cannot know their value during `--help` invocation. I'd like to just set it to `"automatic"` in the help message

In typer there is a `show_default` argument that accepts a string
https://typer.tiangolo.com/tutorial/options/help/#custom-default-string

This is kind of a duplicate of #458 and #749, but in my use case, I don't use a mutable variable as a default

Example:

```
╭─ Parameters ───────────────────────────────────────────────────────────────────────────╮
│ --input-file -i   The input file with information about entries. [default: automatic]  │
│ --output-file -o  The output file with information about entries. [default: automatic] │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```
