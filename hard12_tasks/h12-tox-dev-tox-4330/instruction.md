You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Unset path variable resolves to cwd and clears it

Unset path variable resolves to cwd and clears it.

### Affected code

[`Convert.to()` in `src/tox/config/loader/convert.py`](https://github.com/tox-dev/tox/blob/7988418936b730b19981ba934dc8b57186d6b957/src/tox/config/loader/convert.py#L43) at report commit `7988418936b730b19981ba934dc8b57186d6b957`.

### Mechanism

Convert.to turns an empty string into Path('.'). Environment cleanup later treats that path as the directory to clear. See [Python pathlib](https://docs.python.org/3/library/pathlib.html) for the external parser behavior.

### Reproduction

The reproducer returned `BUG` at the report commit and at main commit `d1963d076c78ed4c03c6f8c6e8fbaf9163e21f48` in a disposable container without network access.

Save the Dockerfile below in the finding directory. Build the source image from main commit `d1963d076c78ed4c03c6f8c6e8fbaf9163e21f48`, then run:

```sh
main_checkout=/path/to/tox-main
docker build -f Dockerfile.repro -t tox-sec-head "$main_checkout"

docker run --rm --network=none -u 0 -w /src -v "$PWD/repro:/tmp/repro:ro,z" -v "$PWD/repro.d:/tmp/repro.d:ro,z" tox-sec-head /tmp/repro
```

```text
CONTROL  SCRATCH_DIR=/tmp/empty-path-value/scratch: tox exit 0, project holds ['.git', '.tox', 'src', 'tox.ini']
OBSERVED SCRATCH_DIR unset: tox exit 0, project holds ['.tox']
BUG
```

Expected: An unset path setting must not resolve to the current directory for cleanup.

**repro**

```python
#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

TOX = "/opt/venv/bin/tox"
workspace = Path("/tmp/empty-path-value")
project = workspace / "project"
scratch = workspace / "scratch"

# set up: a checkout with the project's tox.ini, a source file and git metadata
shutil.rmtree(workspace, ignore_errors=True)
(project / "src").mkdir(parents=True)
(project / "src" / "main.py").write_text("print('uncommitted work')\n")
(project / ".git").mkdir()
(project / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
shutil.copy("/tmp/repro.d/tox.ini", project)
scratch.mkdir()
checkout = {"tox.ini", "src", ".git"}

env_without_scratch = {name: value for name, value in os.environ.items() if name != "SCRATCH_DIR"}
env_with_scratch = {**env_without_scratch, "SCRATCH_DIR": str(scratch)}

# control: SCRATCH_DIR names a directory
control = subprocess.run(
    [TOX, "run", "-e", "py"],
    cwd=project,
    env=env_with_scratch,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    check=True,
)
print(control.stdout)
after_control = {entry.name for entry in project.iterdir()}
print(f"CONTROL  SCRATCH_DIR={scratch}: tox exit {control.returncode}, project holds {sorted(after_control)}\n")

# trigger: the same command where SCRATCH_DIR is not set
resolved = subprocess.run(
    [TOX, "config", "-e", "py", "-k", "env_tmp_dir"],
    cwd=project,
    env=env_without_scratch,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
print(resolved.stdout)
trigger = subprocess.run(
    [TOX, "run", "-e", "py"],
    cwd=project,
    env=env_without_scratch,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
print(trigger.stdout)
after_trigger = {entry.name for entry in project.iterdir()}
print(f"OBSERVED SCRATCH_DIR unset: tox exit {trigger.returncode}, project holds {sorted(after_trigger)}\n")

# check: the checkout that survived the control run must survive this one too
print("BUG" if checkout <= after_control and not checkout & after_trigger else "OK")
```

**repro.d/tox.ini**

```ini
[tox]
no_package = true

[testenv]
env_tmp_dir = {env:SCRATCH_DIR}
commands = python -c "print('testing')"
```

**Dockerfile.repro (test harness)**

```dockerfile
FROM python:3.15-bookworm
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends man-db passwd \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash scanner-test

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY . /src
WORKDIR /src

RUN pip install --upgrade pip \
    && { git describe --tags >/dev/null 2>&1 || export SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0; } \
    && pip install -e '.[completion]' --group test \
    && pip wheel --no-deps --wheel-dir /opt/wheels .

RUN chown -R scanner-test:scanner-test /src && git config --global --add safe.directory /src
```

### Impact

An unset path variable becomes cwd and clears it; the trusted configuration and environment supply the path. Reproducibility is moderate and exposure is niche because a path setting must resolve from an empty value in a different start directory.

### Credits

Anthropic OSS Scanner, ANT-2026-9VVLCGOJ.

