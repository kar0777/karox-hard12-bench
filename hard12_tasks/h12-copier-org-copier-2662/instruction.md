You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

"ValueError: Invalid Choice" with neither property name nor value

### Describe the problem

During `copier update` I get `ValueError: Invalid Choice` but there is no mention of the property name or the invalid value.
This is caused an earlier update in copier.yaml making difficult to debug (i.e. I don't know which change is causing this.)
Issue may be related to multi select choice, I will update if I figure it out.

### Template

Sorry, cannot provide the template.


### To Reproduce

_No response_

### Logs

```console

```

### Expected behavior

The exception message includes property name, valid choices and bad choice causing the error.

### Screenshots/screencasts/logs

_No response_

### Operating system

Linux

### Operating system distribution and version

Fedora 40

### Copier version

9.7.1

### Python version

3.12.9

### Installation method

uvx+pypi

### Additional context

Install is `uv venv ...; uv pip ...`
