You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Path components longer than NAME_MAX (255) succeed instead of raising ENAMETOOLONG

### Description

Path components longer than 255 bytes succeed in the fake filesystem, while the real Posix filesystem raises `OSError: [Errno 36] File name too long` (`ENAMETOOLONG`).

Found by a differential fuzz run comparing the fake filesystem against the real filesystem, so a tested code path can pass under pyfakefs and fail in production.

### Reproduce

```python
import os
import tempfile
from pyfakefs.fake_filesystem import FakeFilesystem, FakeOsModule

fs = FakeFilesystem()
fake_os = FakeOsModule(fs)
long = "a" * 300

fake_os.mkdir("/d")                    # real: tempfile + os.mkdir
fake_os.mkdir("/d/" + long)            # -> succeeds (no error)
os.mkdir(os.path.join(tempfile.mkdtemp(), long))  # -> OSError errno 36

fake_os.stat("/d/" + long)             # -> FileNotFoundError (2)
fake_os.listdir("/d/" + long)          # -> succeeds
fake_os.remove("/d/" + long)           # -> FileNotFoundError (2)
fake_os.truncate("/d/" + long, 0)      # -> FileNotFoundError (2)
```

Affected operations seen in the fuzz run: `mkdir`, `makedirs`, `stat`, `listdir`, `scandir`, `remove`, `rmdir`, `truncate`, `rename` (old and new path), `link` (destination), symlink creation and file open — all with an existing parent directory. With a missing parent, the real OS reports `ENOENT`, which the fake already matches.

### Environment

Python 3.13 on Linux; pyfakefs main branch (82ec77a).

