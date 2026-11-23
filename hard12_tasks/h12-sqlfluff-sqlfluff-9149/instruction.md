You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Building sqlfluffrs with `pip install ./sqlfluffrs` can compile the dialects of the sqlfluff release in pip's build environment instead of the checkout

### Search before asking

- [x] I searched the issues and found no similar issues.

### What Happened

I built sqlfluffrs from a main checkout with `pip install ./sqlfluffrs`, in a virtualenv where sqlfluff was installed in editable mode from the same checkout. The Rust parser then rejected statements that the Python parser accepts on the same checkout, for example `CLOSE c1;` with the postgres dialect.

The generated dialect files did not match the checkout. `python utils/rustify.py check` reported 30 mismatching files, and the generated postgres parser was missing the segments added since the last release: CloseStatementSegment, FetchStatementSegment, DeclareStatementSegment, CheckpointStatementSegment, SetTransactionStatementSegment, the JSON_TABLE segments and others, 32 in all.

`sqlfluffrs_dialects/build.rs` runs `utils/rustify.py build` with `<checkout>/src` prepended to PYTHONPATH. I printed `sqlfluff.__file__`, PYTHONPATH and `sys.path` from rustify.py during the build (paths shortened):

```
sqlfluff.__file__: .../pip-build-env-1ltzodzq/overlay/lib/python3.14/site-packages/sqlfluff/__init__.py
PYTHONPATH:        <checkout>/src:.../pip-build-env-1ltzodzq/site
sys.path:          <checkout>/utils
                   .../pip-build-env-1ltzodzq/site
                   .../lib/python314.zip
                   .../lib/python3.14
                   .../lib/python3.14/lib-dynload
                   .../lib/python3.14/site-packages
                   .../pip-build-env-1ltzodzq/overlay/lib/python3.14/site-packages
                   .../pip-build-env-1ltzodzq/normal/lib/python3.14/site-packages
```

So the generator imported the sqlfluff that pip installs into the build environment from PyPI (4.5.0), not the checkout. `<checkout>/src` is on PYTHONPATH but not on `sys.path`. This comes from pip's build isolation: its sitecustomize (`pip/_internal/build_env/virtual.py`) removes every path that a .pth file in the outer environment adds. The editable install's `__editable__.sqlfluff-4.5.0.pth` adds exactly `<checkout>/src`, so the PYTHONPATH entry is removed with it. (That trace was from a run without the virtualenv activated, where the build script falls back to `python3` on PATH. With the virtualenv activated the generated grammar was the same older one.)

In a fresh virtualenv without sqlfluff installed, the same build generated the checkout's grammar. After `pip install -e .` in that virtualenv it generated the older one again.

CI and the release workflow do not hit this because they run `python utils/rustify.py build` before building.

### Expected Behaviour

The Rust dialects are generated from the checkout, as the comment in `sqlfluffrs_dialects/build.rs` describes, and the two parsers agree on the statements below.

### Observed Behaviour

The build succeeds, but the Rust parser uses the grammar of the sqlfluff release in the build environment:

```
CLOSE c1;                                        python: parsed, rust: unparsable
FETCH FORWARD 5 FROM mycursor;                   python: parsed, rust: unparsable
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;    python: parsed, rust: unparsable
```

`python utils/rustify.py check` reports 30 files that do not match.

### How to reproduce

From a clone of main (the generated dialect files are not in git, so the build script regenerates them; I forced the regeneration in an existing checkout by touching a dialect file):

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install ./sqlfluffrs
python utils/rustify.py check
python check.py
```

check.py:

```python
from sqlfluff.core import FluffConfig, Linter

for sql in ["CLOSE c1;\n", "FETCH FORWARD 5 FROM mycursor;\n", "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;\n"]:
    out = []
    for rust in (False, True):
        lnt = Linter(config=FluffConfig(overrides={"dialect": "postgres", "use_rust_parser": rust}))
        tree = lnt.parse_string(sql).tree
        out.append(("rust" if rust else "python") + (": unparsable" if "unparsable" in str(tree.to_tuple()) else ": parsed"))
    print(sql.strip(), ", ".join(out))
```

Running `python utils/rustify.py build` before `pip install ./sqlfluffrs` avoids it, because the build script then finds up-to-date files and does not regenerate.

On macOS I also needed `CARGO_PROFILE_RELEASE_STRIP=false` for the built library to load. That is unrelated to this issue.

### Dialect

postgres (and any dialect whose grammar changed since the last release)

### Version

sqlfluff main at a8573dd, sqlfluffrs built from the same checkout, pip 26.2.2, Python 3.14.9, macOS

### Configuration

No config file. `use_rust_parser` is set through FluffConfig overrides as in check.py.

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's Code of Conduct

