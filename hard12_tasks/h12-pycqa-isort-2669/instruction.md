You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`--sort-reexports` hardcodes LF line endings regardless of platform

Hi, it's me again about `--sort-reexports` (sorry).

I saw that PR #2605 resolving my issue #2578 was merged and tried it out from GitHub directly (because I'm impatient) and to my delight, it works! Thank you for that!

However, now my editor (PyCharm) as well as my pre-commit config for `mixed-line-endings` seemed to fight with every run of `isort` with `--sort-reexports`, causing lots of files to be rewritten by `mixed-line-endings` (which makes sure files have a consistent line ending).

I checked what was going on and apparently isort is currently hardcoding `\n` for the exports. You can see the effect in the following file, named `repro.py`:

```python
from .somewhere import FirstClass, SecondClass

__all__ = (
    "FirstClass",
    "SecondClass",
)
```
On my **Windows** machine in Notepad++ with invisible chars made visible, the before & after looks like this:
(apologies for screenshots of code but I thought this was the most visible way to convey this)

| Before | After running `isort repro.py --sort-reexports --profile black` |
|-|-|
|<img width="400" alt="Image" src="https://github.com/user-attachments/assets/78ce7621-2fcd-4e69-b6b5-7398337f96bb" /> | <img width="400" alt="Image" src="https://github.com/user-attachments/assets/f233b229-a014-439f-9df6-cdf07670631c" /> |

To be clear, it _does_ correctly sort the exports and it _does_ correctly keep the trailing comma, my issue report is just about the fact that it produces mixed line endings in the file.

Tested with `pip install git+https://github.com/PyCQA/isort@f00e091982aa174f1700beab29c94512de9d64fd` (f00e091982aa174f1700beab29c94512de9d64fd, which was the most recent commit on `main` at the time of me testing this out)
- Windows 11
- Python 3.14.7
