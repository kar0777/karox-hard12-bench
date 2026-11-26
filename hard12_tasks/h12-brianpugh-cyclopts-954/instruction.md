You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Inline binding of list[Model] silently drops a nested collection field

### Summary

When a command parameter is a `list[Model]` and that model has a field which is itself a **collection of models** (e.g. `list[SubModel]`), binding an inline JSON token fills the model's scalar fields but **silently drops the nested collection** — no error, just an empty list. The result is a structurally-valid but wrong object.

A `list` of a *flat* model (scalar fields only) binds correctly from the same JSON form, which makes the failure surprising and easy to miss.

### Reproduction

```python
import sys, cyclopts, pydantic
from pydantic import BaseModel

class Bucket(BaseModel):
    bid: str
    amt: str

class Alloc(BaseModel):
    partner: str
    buckets: list[Bucket]   # a nested collection of models

app = cyclopts.App(name="repro")

@app.command
def flat(*, items: list[Bucket] | None = None):
    print("flat   =>", items)

@app.command
def nested(*, allocs: list[Alloc] | None = None):
    print("nested =>", allocs)

for argv in (
    ["flat",   "--items",  '[{"bid":"b1","amt":"10"}]'],
    ["nested", "--allocs", '[{"partner":"p1","buckets":[{"bid":"b1","amt":"10"}]}]'],
):
    try:
        app(argv, exit_on_error=False)
    except SystemExit:
        pass
```

### Output

```
flat   => [Bucket(bid='b1', amt='10')]
nested => [Alloc(partner='p1', buckets=[])]
```

### Expected

`nested` should parse `buckets` the same way `flat` parses its models — i.e. `[Alloc(partner='p1', buckets=[Bucket(bid='b1', amt='10')])]` — or raise a conversion error. It should not silently discard the nested collection.

### Actual

The scalar field (`partner`) is populated but the nested `buckets` list is silently dropped to `[]`. No warning or error is emitted, so the caller has no signal that data was lost.

### Environment

- cyclopts 4.11.0
- pydantic 2.13.4
- Python 3.11.7 (also reproduced on 3.12)

### Notes

The one-level-deep case (`list[flat model]`) works, so this appears specific to a collection-of-models nested *inside* a model bound from a single JSON token. Happy to help narrow it further.
