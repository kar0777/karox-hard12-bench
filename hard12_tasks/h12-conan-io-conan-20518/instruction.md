You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] `VersionRange.intersection` drops `=` conditions, silently missing version conflicts for exact bracketed ranges

### Describe the bug

When closing a diamond between two version ranges, `VersionRange.intersection` ignores `=` conditions (`[=0.1.0]`, `[0.1.0]`, or an exact branch in an OR range such as `[0.1.0 || ^0.2.0]`). Intersecting `[=0.1.0]` (or `[0.1.0 || ^0.2.0]`) with `[>=1.0]` returns `[>=1.0]` instead of `None`, so Conan silently resolves and installs `libb/1.2.0` for a package that requires `0.1.0`. Conversely, intersecting two exact bracketed ranges with no `<`/`>` bounds (such as `[0.1.0 || 0.2.0]` and `[0.1.0]`, or `[=0.1.0]` and `[=0.1.0]`) returns `None` and raises a false version conflict.

Expected behavior: `conan graph info` (and `conan install`) rejects the incompatible graph with a version conflict between `libb/[=0.1.0]` and `libb/[>=1.0]`, matching Conan's behavior when `libc/1.0.0` declares `requires = "libb/0.1.0"` without brackets (`ERROR: Version conflict: Conflict between libb/0.1.0 and libb/[>=1.0] in the graph.`), and preserves matching exact conditions when intersecting compatible ranges.

In `conan/internal/model/version_range.py`, `VersionRange.intersection` only collects `>`/`>=` and `<`/`<=` bounds via `_calculate_limits` and drops `_Condition` entries with `operator == "="`.

Environment details:
- Conan: 2.34.0 and 2.35.0-dev (`develop2` at `3fbdacf7f324`)
- Python: 3.11.2
- OS: Debian GNU/Linux 12 (x86_64), GCC 12 default profile

### How to reproduce it

```sh
mkdir -p repro/libb repro/libc && cd repro

cat > libb/conanfile.py <<'PY'
from conan import ConanFile
class LibB(ConanFile):
    name = "libb"
PY

cat > libc/conanfile.py <<'PY'
from conan import ConanFile
class LibC(ConanFile):
    name = "libc"
    version = "1.0.0"
    requires = "libb/[=0.1.0]"
PY

export CONAN_HOME="$PWD/.conan2"
conan profile detect
conan export libb --version=0.1.0
conan export libb --version=1.2.0
conan export libc

conan graph info --requires="libc/[>=1.0.0]" --requires="libb/[>=1.0]" -nr
```

The same result occurs when `libc` declares `requires = "libb/[0.1.0]"` or `requires = "libb/[0.1.0 || ^0.2.0]"`:

```text
======== Computing dependency graph ========
Graph root
    cli
Requirements
    libb/1.2.0#f6bfe055f2aec38dadfd366ea2828c1b - Cache
    libc/1.0.0#09c988ee7c7f499d5ae4bbef8d6b9323 - Cache
Resolved version ranges
    libb/[>=1.0]: libb/1.2.0
    libc/[>=1.0.0]: libc/1.0.0
```

Direct check on `VersionRange.intersection`:

```sh
python3 -c '
from conan.internal.model.version_range import VersionRange
for a, b in [("=0.1.0", ">=1.0"), ("0.1.0 || ^0.2.0", ">=1.0"), ("0.1.0 || 0.2.0", "0.1.0")]:
    r = VersionRange(a).intersection(VersionRange(b))
    print(f"{a!r} & {b!r} -> {r.version() if r else None}")
'
```

```text
'=0.1.0' & '>=1.0' -> [>=1.0]
'0.1.0 || ^0.2.0' & '>=1.0' -> [>=1.0]
'0.1.0 || 0.2.0' & '0.1.0' -> None
```

Credit: https://ucsbplse.github.io/

