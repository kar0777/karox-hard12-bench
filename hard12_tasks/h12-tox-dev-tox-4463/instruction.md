You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Uppercase hexadecimal --hash digests are rejected before pip runs

## Issue

A requirements-file hash with uppercase or mixed-case hexadecimal digits is rejected by tox before pip runs, even though pip accepts and verifies the same digest. This affects SHA-256, SHA-384, and SHA-512. Lowercase digests work.

Reproduced with tox 4.67.15 and current main (`794908a7f242ef6c82450a9ad7207d3a9bb2fa7f`). The validator accepts only `[a-f0-9]` in each digest. The algorithm name can remain lowercase and the existing length/nonhex checks can remain strict.

## Environment

- OS: Linux x86_64
- Python: 3.12.14

<details>
<summary>Output of <code>pip list</code> in the isolated tox 4.67.15 environment</summary>

```text
Package           Version
----------------- --------
cachetools        8.0.2
colorama          0.4.6
distlib           0.4.4
filelock          4.3.1
packaging         26.3
pip               26.3
platformdirs      4.14.8
pluggy            1.7.0
pyproject-api     1.12.6
python-discovery  1.9.7
tomli_w           1.2.0
tox               4.67.15
typing_extensions 4.16.0
virtualenv        21.15.12
```

</details>

## Output of running tox

`python -m tox -rvv` exits 1. Relevant final output (virtualenv setup omitted):

```text
py: 652 E failed with argument --hash: sha256:DADB80EF868DA112C670DEA8FFD49DE3DFA806A87DDB70BA2A01559E7A2BF20C for tox env py within deps [tox/session/cmd/run/single.py:70]
  py: FAIL code 1 (0.16 seconds)
  evaluation failed :( (0.20 seconds)
```

The same requirements file is accepted by pip:

```console
$ python -m pip install --dry-run --ignore-installed --no-index --require-hashes -r requirements.txt
Processing ./hash_probe-1.0-py3-none-any.whl (from -r requirements.txt (line 1))
Would install hash-probe-1.0
```

## Minimal example

In an empty directory, run the following script to create a tiny local wheel, a requirements file with its uppercase SHA-256 digest, and a tox configuration. The package install uses no package index.

```python
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

wheel = Path("hash_probe-1.0-py3-none-any.whl")
with ZipFile(wheel, "w") as archive:
    archive.writestr("hash_probe.py", "VALUE = 42\n")
    archive.writestr("hash_probe-1.0.dist-info/METADATA", "Metadata-Version: 2.1\nName: hash-probe\nVersion: 1.0\n")
    archive.writestr("hash_probe-1.0.dist-info/WHEEL", "Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
    archive.writestr("hash_probe-1.0.dist-info/RECORD", "")
digest = sha256(wheel.read_bytes()).hexdigest().upper()
Path("requirements.txt").write_text(f"{wheel.resolve().as_uri()} --hash=sha256:{digest}\n")
Path("tox.ini").write_text(
    "[tox]\nenv_list = py\n[testenv]\npackage = skip\ndeps = -r requirements.txt\n"
    "set_env = PIP_NO_INDEX=1\n"
    'commands = python -c "import hash_probe; assert hash_probe.VALUE == 42"\n'
)
```

Then compare the two commands above. Removing `.upper()` from the digest calculation makes tox install the wheel and run the import successfully. The same failure occurs with SHA-384/SHA-512 and mixed-case digests.

