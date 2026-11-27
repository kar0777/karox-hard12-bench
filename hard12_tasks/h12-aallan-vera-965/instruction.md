You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Diagnostic-fields gate: the `# diag-fields-exempt` opt-out is honoured by only one of three passes

## Summary

`scripts/check_diagnostic_fields.py` tells authors to silence a violation with
`# diag-fields-exempt: <reason>`, but only **one** of its three passes actually
honours that marker.

The failure report (`main()`, near the "Populate the missing field(s) / fix the
spec_ref / register the error_code, or add `# diag-fields-exempt: <reason>` for a
genuinely ..." line) advertises the opt-out as the remedy for *every* violation
class. `_optout_lines()` is consulted only in `check_source()` (the field-presence
pass). Neither `_iter_spec_refs()` (spec_ref validity) nor
`_diagnostic_call_sites()` (error_code registration) reads it.

## Reproduction

```python
# vera/checker/x.py
REF = 'Chapter 4, Section 4.3 "Slot References"'
def check(node):
    return Diagnostic(description='d', rationale='r', fix='f',
                      spec_ref=REF)  # diag-fields-exempt: threaded constant
```

- field-presence pass: clean (opt-out honoured)
- spec_ref pass: `spec_ref is not a string literal — the gate cannot validate it`

The marker is present, carries a reason, and is ignored. The suggested fix ("make
it a literal") is also unfollowable when the value is a parameter or a module
constant.

## Why it is worth fixing

The gate exists to make "is every diagnostic fully tagged?" a mechanically
checkable contract. A gate whose own escape hatch does not work in two of three
passes is emitting advice that cannot be followed — the same "reports something
that isn't so" class the gate was built to catch.

Pre-existing; byte-identical on `main` before and after #827's narrowing (#952).
Surfaced by the adversarial review of #952 and verified against the current tree.

## Design question (why this is not a mechanical fix)

The opt-out currently means "this site is allowed to omit a required field". It is
not obvious it should also mean "this site is allowed to cite a spec section that
does not exist" or "this site is allowed to emit an unregistered error_code" —
those are content errors, not tagging omissions, and blanket-suppressing them
would weaken the gate.

Two coherent options:

1. **Honour the opt-out in all three passes.** Simple and consistent with the
   advertised contract; accepts that a reasoned opt-out can suppress a bogus
   `spec_ref` / unregistered `error_code`.
2. **Narrow the advice.** Keep the opt-out presence-only, and stop offering it in
   the report for `spec_ref` / `error_code` violations. For the specific
   "`spec_ref` is not a string literal" complaint, either drop the complaint (a
   threaded value genuinely cannot be validated statically, and the presence pass
   already accepts it) or emit a followable fix.

Option 2 preserves the gate's strength; option 1 preserves its advertised
contract. Worth deciding deliberately rather than by accident.

## Acceptance criteria

- The three passes and the failure report agree on what `# diag-fields-exempt`
  does.
- A test pins the chosen semantics for each pass, mutation-validated (neuter the
  behaviour, confirm RED).
- No change to the exempt set on `vera/` (`python scripts/check_diagnostic_fields.py`
  still exits 0).

