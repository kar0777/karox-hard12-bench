You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Failing macOS tests in CI

Since the macos-latest runner has been replaced by macOS 26, a few tests are failing due to some behavior changes, for example:
```
======================================================================
ERROR: test_broken_symlink_with_trailing_separator_macos (pyfakefs.tests.fake_os_test.RealOsModuleTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/runner/work/pyfakefs/pyfakefs/pyfakefs/tests/fake_os_test.py", line 764, in test_broken_symlink_with_trailing_separator_macos
    self.os.symlink(link_path + self.os.sep, link_path + self.os.sep)
FileNotFoundError: [Errno 2] No such file or directory: '/var/folders/8j/sfr9qqcj73j4p6nhwcfpr0th0000gn/T/tmph7fzdy2x/link/' -> '/var/folders/8j/sfr9qqcj73j4p6nhwcfpr0th0000gn/T/tmph7fzdy2x/link/'

======================================================================
ERROR: test_circular_readlink_with_trailing_separator_macos (pyfakefs.tests.fake_os_test.RealOsModuleTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/runner/work/pyfakefs/pyfakefs/pyfakefs/tests/fake_os_test.py", line 793, in test_circular_readlink_with_trailing_separator_macos
    self.os.readlink(file_path + self.os.sep)
OSError: [Errno 62] Too many levels of symbolic links: '/var/folders/8j/sfr9qqcj73j4p6nhwcfpr0th0000gn/T/tmplt9_kh13/foo/'

======================================================================
ERROR: test_readlink_circular_link_with_trailing_sep_macos (pyfakefs.tests.fake_os_test.RealOsModuleTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/runner/work/pyfakefs/pyfakefs/pyfakefs/tests/fake_os_test.py", line 2685, in test_readlink_circular_link_with_trailing_sep_macos
    self.assertEqual(path0, self.os.readlink(path0 + self.os.sep))
OSError: [Errno 62] Too many levels of symbolic links: '/var/folders/8j/sfr9qqcj73j4p6nhwcfpr0th0000gn/T/tmpcqz130w6/bar/'

======================================================================
FAIL: test_islink_with_trailing_separator_macos (pyfakefs.tests.fake_os_test.RealOsModuleTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/runner/work/pyfakefs/pyfakefs/pyfakefs/tests/fake_os_test.py", line 662, in test_islink_with_trailing_separator_macos
    self.assertTrue(self.os.path.islink(file_path + self.os.sep))
AssertionError: False is not true

======================================================================
FAIL: test_lexists_with_trailing_separator_macos (pyfakefs.tests.fake_os_test.RealOsModuleTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/runner/work/pyfakefs/pyfakefs/pyfakefs/tests/fake_os_test.py", line 648, in test_lexists_with_trailing_separator_macos
    self.assertTrue(self.os.path.lexists(file_path + self.os.sep))
AssertionError: False is not true
```
The failing tests also depend on the Python version.
The code and tests have to be adapted to work on this version.

