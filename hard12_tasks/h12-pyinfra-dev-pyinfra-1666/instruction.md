You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Per-host TEMP_DIR override

Hello!
First of all, thank you for this amazing project! Thank you for taking some of your time to read this issue :) !

## Summary

Allow defining a per-host temporary directory that overrides `config.TEMP_DIR`, enabling safe and ergonomic handling of environments where `/tmp` is not usable (e.g. `noexec`, restricted mounts).

## Background

On some systems, such as TrueNAS, the default `/tmp` directory may be:

* mounted with restrictive options (e.g. `noexec`)
* otherwise unsuitable for executing temporary scripts

This breaks internal mechanisms in pyinfra that rely on temporary files, notably `SUDO_ASKPASS`.


## Current Workarounds

### Global override via `config.TEMP_DIR`

```python
from pyinfra.context import config

config.TEMP_DIR = "/run/user/950"
```

**Limitations:**

- Applies to all hosts
- Not suitable for heterogeneous environments
- AFAIK, not thread-safe under parallel execution (if someone was to set it multiple times based on something stored in `host.data`)

### Per-operation `_temp_dir` (introduced in v3.7)

```python
server.shell(..., _temp_dir=host.data.temp_dir)
```

**Limitations:**

- Must be repeated on every operation
- Does not affect internal operations (e.g. askpass helpers)
- Poor ergonomics and maintainability


## Proposed Solution

Introduce a per-host `temp_dir` attribute, defined in inventory:

```python
app_servers = [
    ("truenas.tld", {"ssh_user": "truenas-admin", "temp_dir": "/run/user/950"}),
    ("otherserver.tld", {"install_postgres": True}),
]
```

This value would be automatically used by pyinfra when resolving temporary directories.


### Resolution Order (precedence)

1. `_temp_dir` (operation-level override)
2. `host.data.temp_dir` (new)
3. `config.TEMP_DIR`
4. `config.DEFAULT_TEMP_DIR`

> I don't remember where the host environment variable `TMPDIR` fits in this...

### Expected Behavior

* All operations (including internal ones like `SUDO_ASKPASS`) respect the resolved temp directory
* No need to modify individual operations
* Safe under parallel execution (no shared global mutation)

### Benefits

* Enables correct behavior on systems with restricted `/tmp`
* Eliminates need for global state mutation
* Improves ergonomics and reduces boilerplate
* Aligns with existing per-host configuration patterns in pyinfra

---

Thank you!
