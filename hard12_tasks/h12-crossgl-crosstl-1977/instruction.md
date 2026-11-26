You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Index excluded source intervals during Metal entry discovery

## Problem

Metal entry discovery checks every candidate position against an entire interval list with `_position_in_spans`:

```python
return any(start <= position < end for start, end in spans)
```

This repeats a linear scan for each entry and unresolved-host-name candidate. Macro-expanded files with many string literals or excluded declarations therefore spend substantial time on interval membership rather than discovering entries.

## Evidence

Implementation: `662748e3a37e9daec80eff69120f39e050597ea3`, `crosstl/backend/Metal/preprocessor.py`, `_position_in_spans`, `_unresolved_metal_host_name_diagnostics`, and `discover_metal_entry_points`.

A profile of the public runtime manifest builder for one `ss_Powercomplex64` artifact at MLX `d9add9d11f3154111a4c85f267ec2fd307ecd18e` invokes entry discovery four times. The discovery itself can also be reproduced directly:

```python
from pathlib import Path
from crosstl.translator.source_registry import SOURCE_REGISTRY, register_default_sources

root = Path("/path/to/pinned/mlx")
source = root / "mlx/backend/metal/kernels/binary.metal"
register_default_sources()
discovery = SOURCE_REGISTRY.get("metal").discover_entry_points(
    source.read_text(), file_path=str(source), include_paths=[str(root)]
)
assert not discovery.diagnostics
```

Across four discoveries, `cProfile` records:

- 32,988 `_position_in_spans` calls, 84.65 cumulative seconds.
- 410,221,528 membership-generator evaluations, 40.42 seconds in the generator alone.
- 158.51 cumulative seconds across the four full discovery calls.

Measurements are from Python 3.14.7 / Apple M2 Max under concurrent test load and include profiler overhead. The algorithmic call counts are the main evidence; no wall-time threshold is proposed for CI.

## Acceptance Criteria

- Build a reusable interval index or equivalent membership structure once per relevant source/span collection, instead of linearly scanning every interval for every candidate.
- Preserve the exact half-open `start <= position < end` behavior, including boundaries, empty lists, adjacent, duplicate, nested and overlapping intervals. Do not assume concatenated exclusion lists are already sorted or disjoint.
- Preserve entry order, names, locations, provenance, stages and all unresolved-name diagnostics. Comment/literal/template-only false positives fixed in #1863 must not return.
- Bound index lifetime to the corresponding source and retain source-option/include/define isolation.
- Add deterministic complexity-oriented tests and cold/warm discovery equivalence on representative large generated fixtures and the pinned corpus.

This is a general Metal discovery cost exposed by MLX, not an MLX-specific fast path. It is related to #1971 but distinct from caching function/type discovery during template materialization.

