You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[feature] define exe_wrapper for meson cross files

### What is your suggestion?

Meson permits an `exe_wrapper` path in the `[binaries]` section of cross files.  This is used to run host binaries when cross-compiling. It is particularly important for unit tests; quoting from [the docs](https://mesonbuild.com/Cross-compilation.html#defining-the-environment):

"Meson must have exe_wrapper specified in the cross file or else **it will skip tests that attempt to run cross compiled binaries**." [emphasis mine]

Currently the `MesonToolchain` class does not provide a way to define this field.
It would be useful to define the wrapper path in my conan profile, and have it pass through to the generated meson cross file. For example:

```ini
# conan profile for host machine
# ...

[buildenv]
MESON_EXE_WRAPPER=/usr/bin/qemu-aarch64 -L /usr/aarch64-linux-gnu
# ...
```

```ini
# generated meson crossfile
# ...

[binaries]
exe_wrapper = ['/usr/bin/qemu-aarch64', '-L', '/usr/aarch64-linux-gnu']
# ...
```

Notes:
- `MesonToolchain` already sets the `needs_exe_wrapper` flag in the generated meson cross file, even though it doesn't provide a wrapper path
- "MESON_EXE_WRAPPER" is an appropriate env variable name for this purpose, as it is already used by meson to pass the path on down to test scripts.


I am willing to prepare a PR for this feature, but I may need some help writing tests for it. 

### Have you read the CONTRIBUTING guide?

- [x] I've read the CONTRIBUTING guide
