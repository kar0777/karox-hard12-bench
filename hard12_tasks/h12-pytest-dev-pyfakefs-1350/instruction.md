You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`os.path.basename`, `os.path.splitext` and `os.path.commonpath` don't work under Windows simulation

**Describe the bug**
With Windows simulated on a POSIX host, `os.path.basename`, `os.path.splitext` and `os.path.commonpath` don't behave like they do on Windows. They only split on `/`, so backslash-separated paths come back wrong. `os.path.split`, `join`, `dirname` and `normpath` give the right answers for the same paths.

Expected: the same results as on Windows.

```
os.path.split('C:\\a/foo\\t.x')               -> ('C:\\a/foo', 't.x')    (correct)
os.path.basename('C:\\a/foo\\t.x')            -> 'foo\\t.x'              (expected 't.x')
os.path.basename('C:\\a\\foo\\t.x')           -> 'C:\\a\\foo\\t.x'       (expected 't.x')
os.path.splitext('C:\\a.b\\foo')              -> ('C:\\a', '.b\\foo')    (expected ('C:\\a.b\\foo', ''))
os.path.commonpath(['C:\\a\\b', 'C:/a\\c'])   -> ''                      (expected 'C:\\a')
```

**How To Reproduce**
Run on a POSIX host. This prints each result next to what `ntpath` returns for the same input:

```python
import ntpath
import os
from pyfakefs.fake_filesystem import OSType
from pyfakefs.fake_filesystem_unittest import Patcher

cases = [
    ('split', ('C:\\a/foo\\t.x',)),
    ('basename', ('C:\\a/foo\\t.x',)),
    ('basename', ('C:\\a\\foo\\t.x',)),
    ('splitext', ('C:\\a.b\\foo',)),
    ('commonpath', (['C:\\a\\b', 'C:/a\\c'],)),
]
# real ntpath results, computed before the Patcher is active
expected = [getattr(ntpath, name)(*args) for name, args in cases]

with Patcher() as p:
    p.fs.os = OSType.WINDOWS
    for (name, args), want in zip(cases, expected):
        got = getattr(os.path, name)(*args)
        print(f"os.path.{name}{args}: {got!r}  ntpath: {want!r}  {'' if got == want else 'DIFFERS'}")
```

Output:
```
os.path.split('C:\\a/foo\\t.x',): ('C:\\a/foo', 't.x')  ntpath: ('C:\\a/foo', 't.x')  
os.path.basename('C:\\a/foo\\t.x',): 'foo\\t.x'  ntpath: 't.x'  DIFFERS
os.path.basename('C:\\a\\foo\\t.x',): 'C:\\a\\foo\\t.x'  ntpath: 't.x'  DIFFERS
os.path.splitext('C:\\a.b\\foo',): ('C:\\a', '.b\\foo')  ntpath: ('C:\\a.b\\foo', '')  DIFFERS
os.path.commonpath(['C:\\a\\b', 'C:/a\\c'],): ''  ntpath: 'C:\\a'  DIFFERS
```

**Your environment**
```
macOS-27.0-arm64-arm-64bit-Mach-O
Python 3.14.7 (main, Aug  5 2026, 10:29:49) [Clang 21.0.0 (clang-2100.1.1.101)]
pyfakefs 6.2.0
ModuleNotFoundError: No module named 'pytest'
```
