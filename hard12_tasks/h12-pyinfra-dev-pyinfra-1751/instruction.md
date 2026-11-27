You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

config.TEMP_DIR is not applied for sudo operations when defined in a deploy file

## Describe the bug
config.TEMP_DIR changes are not applied for sudo when defined in a deploy file, but are applied when defined as part of an inventory file.

I work with RHEL systems that have `noexec` set on /tmp, so I need to change the TEMP_DIR.
During my tests I noticed that it only works when in set `config.TEMP_DIR` as part of the inventory file (or config.py file), and not in the deploy file.

## To Reproduce
Steps to reproduce the behavior, please include where possible:
deploy.py:
```
#!/usr/bin/env python3

from pyinfra.context import config
from pyinfra.operations import files

config.TEMP_DIR = '/home/my_user/tmp/'
files.directory(name='Ensure other directory exists', path='/tmp/other', _sudo=True)
```
This fails with the following error:

```
↳ uv run pyinfra inventory.py deploy.py -vv
--> Loading config...
--> Loading inventory...
--> Connecting to hosts...
    [my_host.local.net] Connected

--> Preparing operation files...
    Loading: deploy.py
[my_host.local.net] >>> sudo -H -n sh -c '! (test -e /tmp/other || test -L /tmp/other ) || ( stat -c '"'"'user=%U group=%G mode=%A atime=%X mtime=%Y ctime=%Z size=%s %N'"'"' /tmp/other 2> /dev/null || stat -f '"'"'user=%Su group=%Sg mode=%Sp atime=%a mtime=%m ctime=%c size=%z %N%SY'"'"' /tmp/other || ls -ld /tmp/other )'
[my_host.local.net] sudo password:
[my_host.local.net] >>> env SUDO_ASKPASS=/tmp/pyinfra-sudo-askpass-8NpsYLQAHYt1 *** sudo -H -A -k sh -c '! (test -e /tmp/other || test -L /tmp/other ) || ( stat -c '"'"'user=%U group=%G mode=%A atime=%X mtime=%Y ctime=%Z size=%s %N'"'"' /tmp/other 2> /dev/null || stat -f '"'"'user=%Su group=%Sg mode=%Sp atime=%a mtime=%m ctime=%c size=%z %N%SY'"'"' /tmp/other || ls -ld /tmp/other )'
    [my_host.local.net] sudo: unable to run /tmp/pyinfra-sudo-askpass-8NpsYLQAHYt1: Permission denied
    [my_host.local.net] sudo: no password was provided
    [my_host.local.net] sudo: a password is required
    [my_host.local.net] Error: could not load fact: files.Directory path=/tmp/other

--> Disconnecting from hosts...
--> pyinfra error in deploy.py line 10: No hosts remaining!
```

Whereas if I set `config.TEMP_DIR = '/home/my_user/tmp/'` in the inventory, I get the following:

```
↳ uv run pyinfra inventory.py deploy.py -vv
--> Loading config...
--> Loading inventory...
--> Connecting to hosts...
    [my_host.local.net] Connected

--> Preparing operation files...
    Loading: deploy.py
[my_host.local.net] >>> sudo -H -n sh -c '! (test -e /tmp/other || test -L /tmp/other ) || ( stat -c '"'"'user=%U group=%G mode=%A atime=%X mtime=%Y ctime=%Z size=%s %N'"'"' /tmp/other 2> /dev/null || stat -f '"'"'user=%Su group=%Sg mode=%Sp atime=%a mtime=%m ctime=%c size=%z %N%SY'"'"' /tmp/other || ls -ld /tmp/other )'
[my_host.local.net] sudo password:
[my_host.local.net] >>> env SUDO_ASKPASS=/home/my_user/tmp//pyinfra-sudo-askpass-ViOtoBDombJZ *** sudo -H -A -k sh -c '! (test -e /tmp/other || test -L /tmp/other ) || ( stat -c '"'"'user=%U group=%G mode=%A atime=%X mtime=%Y ctime=%Z size=%s %N'"'"' /tmp/other 2> /dev/null || stat -f '"'"'user=%Su group=%Sg mode=%Sp atime=%a mtime=%m ctime=%c size=%z %N%SY'"'"' /tmp/other || ls -ld /tmp/other )'
    [my_host.local.net] Loaded fact files.Directory (path=/tmp/other)
    [my_host.local.net] Ready: deploy.py

--> Detected changes:
    Operation                       Change                                     Conditional Change
    Ensure other directory exists   1 (my_host.local.net)   -

    Detected changes may not include every change pyinfra will execute.
    Hidden side effects of operations may alter behaviour of future operations,
    this will be shown in the results. The remote state will always be updated
    to reflect the state defined by the input operations.

    Detected changes displayed above, skip this step with -y

--> Beginning operation run...
--> Starting operation: Ensure other directory exists
[my_host.local.net] >>> env SUDO_ASKPASS=/home/my_user/tmp//pyinfra-sudo-askpass-ViOtoBDombJZ *** sudo -H -A -k sh -c '! (test -e /tmp/other || test -L /tmp/other ) || ( stat -c '"'"'user=%U group=%G mode=%A atime=%X mtime=%Y ctime=%Z size=%s %N'"'"' /tmp/other 2> /dev/null || stat -f '"'"'user=%Su group=%Sg mode=%Sp atime=%a mtime=%m ctime=%c size=%z %N%SY'"'"' /tmp/other || ls -ld /tmp/other )'
    [my_host.local.net] Loaded fact files.Directory (path=/tmp/other)
[my_host.local.net] >>> env SUDO_ASKPASS=/home/my_user/tmp//pyinfra-sudo-askpass-ViOtoBDombJZ *** sudo -H -A -k sh -c 'mkdir -p /tmp/other'
    [my_host.local.net] Success

--> Results:
    Operation                       Hosts   Success   Error   No Change
    Ensure other directory exists   1       1         -       -
    Grand total                     1       1         -       -

--> Disconnecting from hosts...
```

We can see that this time the `pyinfra-sudo-askpass-...` is in the correct temp dir.

## Expected behavior
I was expecting it to work when setting the `config.TEMP_DIR` value from the deploy file, the same way it works when set in the inventory file. 

## Meta
+ Include output of `pyinfra --support`.
```
↳ uv run pyinfra --support
    If you are having issues with pyinfra or wish to make feature requests, please
    check out the GitHub issues at https://github.com/Fizzadar/pyinfra/issues .
    When adding an issue, be sure to include the following:

    System: Linux
      Platform: Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.42
      Release: 6.6.87.2-microsoft-standard-WSL2
      Machine: x86_64
    pyinfra: v3.8.0
      click: v8.3.3
      distro: v1.9.0
      gevent: v26.4.0
      jinja2: v3.1.6
      packaging: v26.2
      paramiko: v4.0.0
      pydantic: v2.13.3
      python-dateutil: v2.9.0.post0
      typeguard: v4.5.1
      types-paramiko: v4.0.0.20260408
      typing-extensions: v4.15.0
    Executable: /home/arnaud/git/CI/ci-tools/python/pyinfra/.venv/bin/pyinfra
    Python: 3.14.4 (CPython, GCC 15.2.1 20260123 (Red Hat 15.2.1-7))
```
+ How was pyinfra installed (source/pip)?
Installed using uv


