You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`--config-override` parses numeric-looking values as numbers, rejecting python_version=3.12

### Description

`--config-override build_config.python_version=3.12` fails validation because the value `3.12` is parsed as a float, but `python_version` is a string field. The user has to know to quote the value (`python_version="3.12"`), and the error doesn't point at that fix. `--config-override` should coerce the value to the target field's declared type (or emit an actionable message naming the quoting fix).

### Steps to reproduce

```bash
tesseract init --name demo
tesseract build . --config-override 'build_config.python_version=3.12' --generate-only
```

### Logs

```bash
ValidationError: 1 validation error for TesseractBuildConfig
python_version
  Input should be a valid string [type=string_type, input_value=3.12, input_type=float]
    For further information visit https://errors.pydantic.dev/2.13/v/string_type
```

### OS

Mac

### Tesseract version

1.10.0

