You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

CLI rejects field-name options when a model uses `validate_by_name=True` (pydantic ≥ 2.11)

**Repo:** BrianPugh/cyclopts
**File:** `cyclopts/field_info.py` (line 174, in `_pydantic_field_infos`)
**Rule reference:** pydantic 2.11 split `validate_by_name` from `populate_by_name`

## Summary

When a pydantic model sets `validate_by_name=True` (pydantic ≥ 2.11, so the model **accepts its field names during validation**), cyclopts still decides which CLI option names to register by reading **only** `populate_by_name`:

```python
if pydantic_field.alias:
    if model.model_config.get("populate_by_name", False):
        names.append(python_name)
    names.append(pydantic_field.alias)
```

As a result, for aliased fields whose Python name is not a hyphen/underscore variant of the alias, the field-name CLI option is **rejected as "Unknown option"**, even though the underlying model would happily validate input by field name.

## Reproduction

cyclopts 4.23.3 + pydantic 2.11.10:

```python
from cyclopts import App
from pydantic import BaseModel, Field, ConfigDict

class Model(BaseModel):
    model_config = ConfigDict(validate_by_name=True)  # NOT populate_by_name
    full_name: str = Field(alias="userName")

app = App()

@app.default
def main(model: Model):
    ...

app(["--model.full_name", "Alice"])
```

Result:

```
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Unknown option: --model.full_name. Did you mean --model.username?            │
╰──────────────────────────────────────────────────────────────────────────────╯
SystemExit: 1
```

while pydantic itself accepts the field name:

```python
Model.model_validate({"full_name": "Alice"})   # OK
```

and `--model.user-name` / `--model.username` parse fine. Only the **field-name** form — exactly what `validate_by_name=True` opts into — is missing.

## Expected vs actual

- **Expected:** a model configured with `validate_by_name=True` should accept its field names on the CLI (that is the whole point of the config), i.e. `--model.full_name` should parse.
- **Actual:** field-name options are only registered when `populate_by_name` is set; with the newer `validate_by_name` alone, they are rejected.

## Root cause

pydantic 2.11 split the old `populate_by_name` semantics: `populate_by_name` now covers name-based population (e.g. `construct`), while `validate_by_name` independently governs whether field names are accepted **during validation**. cyclopts' name-registration decision only reads the former, so it ignores the latter. This mirrors a bug polyfactory had with the same config key (fixed upstream by reading both).

## Suggested fix

Read both flags:

```python
if pydantic_field.alias:
    if model.model_config.get("validate_by_name", False) or model.model_config.get("populate_by_name", False):
        names.append(python_name)
    names.append(pydantic_field.alias)
```

Verified against cyclopts 4.23.3 + pydantic 2.11.10: with this one-line change, `--model.full_name` parses correctly, `--model.user-name` / `--model.username` still work, and models with only `populate_by_name=True` are unaffected. Full patch attached in `fix.patch`.

## Notes

- For simple aliases (`alias="firstName"` with field `first_name`), the failure is masked by cyclopts' fuzzy hyphen/underscore matching against the legacy lowercase alias form — the bug is visible whenever the field name is not a case/hyphen/underscore variant of the alias (e.g. `full_name` vs `userName`), or when the legacy alias form is undesirable.
- `validate_by_name` requires pydantic ≥ 2.11; cyclopts already requires `>=2.11.2`, so the key is always supported on the supported pydantic range.
