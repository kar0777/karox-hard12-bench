You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Overly aggressive bundle identifier validator rejects valid bundle IDs

### Describe the bug

Similar to #1212 although pretty much the opposite example, Briefcase won't let me use `is.oja` as my bundle ID, despite it being valid (`https://oja.is` will be the website for the app).  There are plenty of examples of  allowing bundle ids along these lines.  I get:

```
Briefcase configuration error: 'is' is not a valid bundle identifier.

The bundle should be a reversed domain name. It must contain at least 2 dot-separated sections; each section may only include letters, numbers, and hyphens; and each section may not contain any reserved words (like 'switch', or 'while').
```

It's true that a bundle ID does have to have at least one dot, however Briefcase is actually asking for the bundle ID prefix here, since it forms the ID from this prefix plus a dot and the app name, thus supplying the required dot.  If the actual bundle ID was validated, instead of just the prefix, there would not be a problem.

### How to reproduce the bug

Create a new briefcase project, with the following in `pyproject.toml`

```pyproject.toml
[tool.briefcase]
project_name = "oja"
bundle = "is"
```

Attempt to build with briefcase.  Get the error:

```
Briefcase configuration error: 'is' is not a valid bundle identifier.

The bundle should be a reversed domain name. It must contain at least 2 dot-separated sections; each section may only include letters, numbers, and hyphens; and each section may not contain any reserved words (like 'switch', or 'while').
```
Expect the app to build.

### Minimum example code

```shell

```

### Screenshots

_No response_

### Environment details

- Operating system and version: 26.3.1 (a) (25D771280a)
- Python version: 3.13
- Software versions:
  - Briefcase: 0.4.2
  - Toga: 0.5.4


### Logs

<!-- Paste your log content between the backticks, or upload a file. -->
```

```


### Additional context

_No response_
