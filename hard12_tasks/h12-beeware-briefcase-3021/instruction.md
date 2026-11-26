You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Briefcase configuration error: The license configuration for 'myapp' is in PEP 639 format, but the `license` value 'Proprietary' is not a valid SPDX expression.  Update the `license` definition to a valid SPDX expression.

### Describe the bug

I ran `briefcase new` after installing briefcase on Windows 11 under Python 3.14.7

I followed the prompts including setting the license to "Proprietary"


```
-- Project License -----------------------------------------------------------

What license do you want to use for this project's code?

  1) BSD 3-Clause "New" or "Revised" License (BSD-3-Clause)
  2) MIT License (MIT)
  3) Apache License 2.0 (Apache-2.0)
  4) GNU General Public License v2.0 only (GPL-2.0)
  5) GNU General Public License v2.0 or later (GPL-2.0+)
  6) GNU General Public License v3.0 only (GPL-3.0)
  7) GNU General Public License v3.0 or later (GPL-3.0+)
  8) Proprietary
  9) Other

Project License [1]: 8
```


```
[myapp] Generating a new application 'My App'
Using app template: https://github.com/beeware/briefcase-template, branch v0.4.4
Cloning template 'https://github.com/beeware/briefcase-template'...
Using existing template (sha 6585e33ad0a9339b31aa26a4960b049f5bf18cd3, updated Sun Jul  5 22:41:31 2026)

[myapp] Generated new application 'My App'

To run your application, type:

    $ cd myapp
    $ briefcase dev 
```

```
briefcase dev

Briefcase configuration error: The license configuration for 'myapp' is in PEP 639 format, but the
`license` value 'Proprietary' is not a valid SPDX expression.

Update the `license` definition to a valid SPDX expression.
```




### How to reproduce the bug

1. Use briefcase new to create a new app
2. Fill in the template, selecting 8, Proprietary as the license
3. Try to run `briefcase dev`
4. See error


### Minimum example code

```shell

```

### Screenshots

_No response_

### Environment details

- Operating system and version:
- Python version:
- Software versions:
  - Briefcase: 0.4.4
  - Toga: (how do I find this out? It'd be good to have briefcase dump this info out)


### Logs

<!-- Paste your log content between the backticks, or upload a file. -->
```
Log reproduced on another empty project
```

[briefcase-bug.zip](https://github.com/user-attachments/files/31345091/briefcase-bug.zip) 

### Additional context

_No response_
