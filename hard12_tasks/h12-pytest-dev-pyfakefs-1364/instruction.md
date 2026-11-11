You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

shutil.rmtree fails on directory containing a symlink to a directory (Python >= 3.12.4)

**Describe the bug**

`shutil.rmtree()` fails with `NotADirectoryError` if the fake directory contains a symlink to a directory. It also deletes the contents of the symlink target first. On the real filesystem it just removes the link.

Cause: since CPython 3.12.4, `shutil._rmtree_unsafe` calls `os.walk(..., followlinks=os._walk_symlinks_as_files)`. The fake `walk()` in `fake_scandir.py` doesn't know this sentinel and treats it as `followlinks=True`.

```
  File ".../shutil.py", line 693, in _rmtree_unsafe
    os.rmdir(fullname)
  File ".../pyfakefs/fake_os.py", line 871, in rmdir
    self.filesystem.rmdir(path)
  File ".../pyfakefs/fake_filesystem.py", line 3181, in rmdir
    self.raise_os_error(errno.ENOTDIR, target_directory)
NotADirectoryError: [Errno 20] Not a directory: '/xyzzy/link_to_dir'
```

**How To Reproduce**

```python
import os
import shutil


def test_rmtree_with_symlink_to_dir(fs):
    fs.create_file("/target_dir/file")
    fs.create_symlink("/xyzzy/link_to_dir", "/target_dir")
    shutil.rmtree("/xyzzy")
    assert not os.path.exists("/xyzzy")
    assert os.path.exists("/target_dir/file")
```

Passes on Python 3.11, fails on 3.12.11, 3.13.15 and 3.14.10 (also with current `main`). I have a fix, will open a PR.

**Your environment**

```
Linux-7.1.6-1rodete1-amd64-x86_64-with-glibc2.43
Python 3.14.10 (chromium.1, Oct 26 2026, 08:21:54) [GCC 10.2.1 20210130 (Red Hat 10.2.1-11)]
pyfakefs 6.1.3
pytest 9.0.2
```

