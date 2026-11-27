You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

add_piecewise_formulation: support a partial `active` gate (treat missing/null entries as always-active)

We need partial active triggers in pw formulations. 

> [!Note]
> AI written issue

`Model.add_piecewise_formulation(..., active=<var>)` gates a piecewise function on a binary `active` variable: when `active=0`, the auxiliary variables (and thus the output) are pushed to zero. The gating enters through `delta_var <= active` and the `bp0 * active` intercept term in `_add_incremental` (and the analogous disjunctive path).

This works when `active` is defined over the *entire* coordinate of the formulation. It breaks down when `active` is only defined over a **subset** of the indexed dimension.

### Problem

When the `active` expression is null/missing for part of the formulation's dimension, those entries get gated as if `active=0` and their output is forced to zero — rather than being treated as ungated (always on).

This surfaced downstream in PyPSA ([PyPSA/PyPSA#1755](https://github.com/PyPSA/PyPSA/pull/1755)). PyPSA builds one piecewise formulation across a mix of **committable** and **non-committable** components and passes the unit-commitment `status` variable as `active`. The `status` variable only exists for committable components; for the rest it is null. The result: non-committable components — which should always dispatch — were incorrectly forced to zero by the `_active` piecewise constraint.

### Proposed feature

Let `add_piecewise_formulation` accept an `active` expression/variable that is **defined only over a subset** of the formulation's dimension (i.e. null/missing elsewhere). Entries where `active` is missing should be treated as **always active** (gate = 1, ungated), and entries where it is present should be gated as today.

Effectively:
- `where active.isnull()` → no gating
- `where ~active.isnull()` → gated on `active`

### Notes / open questions

- The `active` semantics are already flagged as an evolving API (`EvolvingAPIWarning`), so refining them here fits.
- Decide whether the trigger is "NaN entries in a full-coordinate `active`" vs. "`active` indexed over a strict subset of the dimension" — both should resolve to the same behaviour, ideally without the caller pre-aligning.
- Applies to both the incremental/SOS2 (`_add_incremental`) and disjunctive (`_add_disjunctive`) paths; the LP path already rejects `active`.


