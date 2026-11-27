You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Installing from source without `npm`

**Is your feature request related to a problem? Please describe.**
I'd like to install the `master` branch from source util v1.5.4 is released with the [fix](https://github.com/reata/sqllineage/pull/617) merged before.
The machine installing the code has no NodeJS installed, and it's not trivial to do so.
The setup fails with the following error:

```text
Collecting sqllineage@ https://github.com/reata/sqllineage/archive/refs/heads/master.zip (from my-package==0.0.1->-r requirements.txt (line 1))
  Downloading https://github.com/reata/sqllineage/archive/refs/heads/master.zip
     / 709.9 kB 2.7 MB/s 0:00:00
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'error'
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [2 lines of output]
      running egg_info
      error: [Errno 2] No such file or directory: 'npm'
      [end of output]
 ```

**Describe the solution you'd like**
I'd like the package to skip the javascript component when `nodes`/`npm` are unavailable, but continue with the Python installation (perhaps a warning).

The change should be simple, e.g. try-except or check if the `npm` bin is present:
https://github.com/reata/sqllineage/blob/master/setup.py#L28

**Describe alternatives you've considered**
A release would also solve my problem directly. Still I'd suggest considering this change, for future users.

**Additional context**
Add any other context or screenshots about the feature request here.

