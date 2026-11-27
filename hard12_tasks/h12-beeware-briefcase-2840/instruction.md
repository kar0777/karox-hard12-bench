You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Disallow creating projects with an app that starts with a number

### Describe the bug

It is possible to create projects with an app that starts with a number but this is not valid.

```
❯ briefcase new -Q app_name=1hello --no-input && cd 1hello && briefcase dev

Using override value '1hello'

[1hello] Generating a new application 'Hello World'
Using app template: https://github.com/beeware/briefcase-template, branch v0.3.21
Template branch v0.3.21 not found; falling back to development template
Using existing template (sha af397117020084a0c284c65132c0e6c1019c1b65, updated Tue Dec 31 08:20:07 2024)

[1hello] Generated new application 'Hello World'

To run your application, type:

    $ cd 1hello
    $ briefcase dev


[1hello] Installing requirements...
Requirement already satisfied: toga-gtk~=0.4.7 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (0.4.9.dev300+g1b7609dd8)
Requirement already satisfied: pytest in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (8.3.4)
Requirement already satisfied: pycairo>=1.17.0 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from toga-gtk~=0.4.7) (1.27.0)
Requirement already satisfied: pygobject>=3.50.0 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from toga-gtk~=0.4.7) (3.50.0)
Requirement already satisfied: toga-core==0.4.9.dev300+g1b7609dd8 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from toga-gtk~=0.4.7) (0.4.9.dev300+g1b7609dd8)
Requirement already satisfied: travertino>=0.3.0 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from toga-core==0.4.9.dev300+g1b7609dd8->toga-gtk~=0.4.7) (0.3.0)
Requirement already satisfied: exceptiongroup>=1.0.0rc8 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from pytest) (1.2.2)
Requirement already satisfied: iniconfig in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from pytest) (2.0.0)
Requirement already satisfied: packaging in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from pytest) (24.2)
Requirement already satisfied: pluggy<2,>=1.5 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from pytest) (1.5.0)
Requirement already satisfied: tomli>=1 in /home/russell/.pyenv/versions/3.10.15/envs/briefcase-3.10/lib/python3.10/site-packages (from pytest) (2.2.1)
Installing dev requirements... done

[1hello] Starting in dev mode...
===========================================================================
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/home/russell/.pyenv/versions/3.10.15/lib/python3.10/runpy.py", line 220, in run_module
    mod_name, mod_spec, code = _get_module_details(mod_name)
  File "/home/russell/.pyenv/versions/3.10.15/lib/python3.10/runpy.py", line 146, in _get_module_details
    return _get_module_details(pkg_main_name, error)
  File "/home/russell/.pyenv/versions/3.10.15/lib/python3.10/runpy.py", line 157, in _get_module_details
    code = loader.get_code(mod_name)
  File "<frozen importlib._bootstrap_external>", line 1017, in get_code
  File "<frozen importlib._bootstrap_external>", line 947, in source_to_code
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/russell/tmp/beeware/1hello/src/1hello/__main__.py", line 1
    from 1hello.app import main
         ^
SyntaxError: invalid decimal literal

Problem running app 1hello.
```

### Steps to reproduce

Run `briefcase new -Q app_name=1hello --no-input && cd 1hello && briefcase dev`

### Expected behavior

App names that begin with a number should not be allowed.

### Screenshots

_No response_

### Environment

- Operating System: pop os 22.04
- Python version: 3.10
- Software versions:
  - Briefcase: `0.3.21.dev125+gdced62d4`

### Logs

[briefcase.2025_01_21-00_06_20.dev.log](https://github.com/user-attachments/files/18484979/briefcase.2025_01_21-00_06_20.dev.log)

### Additional context

_No response_
