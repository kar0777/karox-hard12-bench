You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] Binary built with a different package_id_abi_options value is selected as a compatible package

### Describe the bug

A dependency can declare `package_id_abi_options` so that the values of those options become part of the package ID of its static/shared consumers. This works for the consumer's main package ID: when the option value changes, the main package ID changes and the binary is reported as missing.

However, Conan then looks for compatible configurations (here with the default `compatibility.py` plugin) and selects the consumer binary that was built against the **old** option value as a "compatible package". The reported diff is **empty**. A binary built against an ABI-incompatible dependency configuration is silently reused, which defeats the purpose of `package_id_abi_options`.

### How to reproduce it

Self-contained script (uses a temporary `CONAN_HOME` and the default `compatibility.py` plugin):

```bash
#!/usr/bin/env bash
set -e
export CONAN_HOME="$(mktemp -d)"
conan profile detect >/dev/null 2>&1
WORK="$(mktemp -d)"; cd "$WORK"; mkdir dep pkg

cat > dep/conanfile.py <<'PY'
from conan import ConanFile
class Dep(ConanFile):
    name = "dep"
    version = "1.0"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {"my_option": [True, False]}
    default_options = {"my_option": True}
PY

cat > pkg/conanfile.py <<'PY'
from conan import ConanFile
class Pkg(ConanFile):
    name = "pkg"
    version = "1.0"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    requires = "dep/1.0"
PY

conan create dep -o "dep/*:my_option=True" >/dev/null 2>&1
conan create pkg -o "dep/*:my_option=True" 2>&1 | grep -E "^pkg/1.0: Package '.*' built"

# dep now declares that 'my_option' affects consumers' ABI
echo '    package_id_abi_options = ["my_option"]' >> dep/conanfile.py
conan create dep -o "dep/*:my_option=False" >/dev/null 2>&1
conan install --requires=pkg/1.0 -o "dep/*:my_option=False" 2>&1 | grep -E "^pkg/1.0:|pkg/1.0#.*:"
```

Output (macOS, apple-clang, Conan 2.34.0):

```
pkg/1.0: Package '9c857ee9a8418d33728ae06838ce1c48fba0a753' built
pkg/1.0: Main binary package '0122ef39771a13d17585289b5a6e050ebd98afdc' missing
pkg/1.0: Checking 14 compatible configurations
pkg/1.0: Found compatible package '9c857ee9a8418d33728ae06838ce1c48fba0a753': 
    pkg/1.0#b7a8fe8fdd5ee1793c8400673fcf3d8b:9c857ee9a8418d33728ae06838ce1c48fba0a753#95546528e0d48c467edfac3b4ddc07c4 - Cache
pkg/1.0: Already installed! (2 of 2)
```

The main ID `0122ef…` (with `dep/*:my_option=False`) is missing, so Conan returns the stale binary `9c857e…`, which was built against `dep/*:my_option=True`, as a compatible package with an empty diff.

`pkg` should be reported as missing and require a build. The binary built against `dep/*:my_option=True` should not be selected as compatible when `dep/*:my_option=False` is used, because the dependency declares `my_option` in `package_id_abi_options`.
