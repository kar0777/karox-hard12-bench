You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

layout: circle_layout entry guards — TypeError on edge-only graphs (len() before materialize_nodes), bare KeyError('x') for the no-arg form, IntCastingNaNError on duplicate bounding_box keys

Found by the 2026-08 layouts/viz amplification probe. Repros on `master` @ `42b4f7f7d`, pandas 2.3.3 / py3.12.

`circle_layout` is the only layout on the surface that cannot handle an edge-only graph, and the only one whose no-argument form is a bare `KeyError`. It is also reachable from the wire as a GFQL `call('circle_layout', ...)` (`graphistry/compute/gfql/call/validation.py:805`, `graphistry/models/gfql/types/call.py:38`), where an untyped exception is a worse outcome than locally.

## Defect 1 (bare-crash): edge-only graph — `len()` runs *before* `materialize_nodes()`

`graphistry/layout/circle.py:142-147`:

```python
142:    num_nodes = len(self._nodes)      # <-- _nodes is None here
143:    if num_nodes == 0:
144:        return self
145:
146:    g = self.materialize_nodes()      # <-- the fix is one line too late
147:    g = g.nodes(g._nodes.reset_index(drop=True))
```

```python
import pandas as pd, graphistry
e = pd.DataFrame({'s':[0,1,2], 'd':[1,2,0]})
graphistry.edges(e, 's', 'd').circle_layout(bounding_box=(0,0,10,10))
```

**Observed**: `TypeError: object of type 'NoneType' has no len()`
**Expected**: nodes materialized from the edges and laid out — which is what `materialize_nodes()` two lines below is there to do.

Cross-layout comparison on that identical edge-only graph:

```
circle_layout(bounding_box=..)   TypeError: object of type 'NoneType' has no len()
circle_layout()                  TypeError: object of type 'NoneType' has no len()
tree_layout()                    OK  (3 nodes)
layout_igraph('fr')              OK  (3 nodes)
group_in_a_box_layout()          OK  (3 nodes)
modularity_weighted_layout()     OK  (3 nodes)
ring_categorical_layout('cat')   ValueError: Missing nodes      <- typed decline, fine
ring_continuous_layout('cat')    ValueError: Missing nodes      <- typed decline, fine
```

`circle_layout` is alone in producing an untyped `TypeError`, and alone in failing a case it clearly intends to support.

Secondary consequence of the same ordering: when `_nodes` is set but `_node` is unbound, `materialize_nodes()` (`ComputeMixin.py:218-255`) only warns and then *replaces* the node table with an edge-derived one — so `num_nodes` captured at `:142` is stale, and every `Series(full(num_nodes, ...))` at `:218-222`, `:280`, `:306` is built at the wrong length.

## Defect 2 (bare-crash): the no-argument form on a graph with no prior positions

`circle.py:209-216` reads `g._nodes['x']` / `g._nodes['y']` to derive the bounding box when `bounding_box is None`:

```python
import pandas as pd, graphistry
e = pd.DataFrame({'s':[0,1,2], 'd':[1,2,0]})
n = pd.DataFrame({'id':[0,1,2]})
graphistry.edges(e,'s','d').nodes(n,'id').circle_layout()      # KeyError: 'x'
```

`docs/source/gfql/builtin_calls.rst` does state *"If omitted, the graph must already have `x`/`y` node positions"*, so the **precondition** is documented — but it is never validated, and the failure is a bare `KeyError: 'x'` rather than a message naming the requirement. Over the GFQL wire, `call('circle_layout', {})` on a fresh graph is a plain `KeyError` with nothing pointing at `bounding_box`.

**Expected**: a typed error along the lines of *"circle_layout requires either bounding_box= or existing x/y node positions"*.

## Defect 3 (bare-crash): duplicate partition keys in a `bounding_box` frame

`circle.py:237-241` does an unqualified `how='left'` merge and never length-checks the result (only `node_partition_sizes` is asserted, at `:253`):

```python
import pandas as pd, graphistry
E = pd.DataFrame({'s':[0,1,2,3],'d':[1,2,0,0]})
N = pd.DataFrame({'id':[0,1,2,3],'p':['a','a','b','b']})
bb = pd.DataFrame({'partition_key':['a','a','b','b'], 'cx':[0.,5.,100.,105.],
                   'cy':[0.,0.,100.,100.], 'w':[10.]*4, 'h':[10.]*4})
graphistry.edges(E,'s','d').nodes(N,'id').circle_layout(partition_by='p', bounding_box=bb)
```

**Observed**: `IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer` — raised from pandas internals, with nothing naming the duplicate keys.
**Expected**: a typed error naming the duplicated `partition_key` values.

## Defect 4 (misleading error): a null partition key blames the wrong thing

`circle.py:194-195` raises `ValueError('Unexpected NaNs in node indices')`, but the reachable cause is a **null value in `partition_by`** — pandas `groupby(...).cumcount()` at `:190` returns NaN for rows whose group key is null.

```python
N = pd.DataFrame({'id':[0,1,2,3], 'p':['a','a',None,'b']})
# ... circle_layout(partition_by='p', bounding_box=bb)
# ValueError: Unexpected NaNs in node indices
```

The message sends the reader to node ids; the fix is in their partition column.

## Defect 5 (INDICATIVE, static only): dead engine comparison hides a CPU/GPU divergence

`circle.py:327`:

```python
327:    if engine_concrete in [EngineAbstract.CUDF, 'cudf', 'Engine.CUDF'] or hasattr(node_idx_relative, 'to_pandas'):
330:        node_angles = 2 * np.pi * node_idx_relative.reset_index(drop=True) / nodes_in_ring.reset_index(drop=True)
331:    else:
332:        node_angles = ((2 * pi * node_idx_relative) / nodes_in_ring).fillna(0.0)
```

`engine_concrete` is an `Engine`, and `Engine.CUDF in [EngineAbstract.CUDF, 'cudf', 'Engine.CUDF']` evaluates to `False` (verified — different Enum classes, and `Engine` is not a str-enum). The branch is therefore selected *only* by the `hasattr(..., 'to_pandas')` duck-type, which happens to be true for cuDF and false for pandas — so it works by accident.

The consequence is a real asymmetry: the cuDF branch has **no** `.fillna(0.0)`, so a NaN angle raises `ValueError('Unexpected NaNs in node angles')` at `:333` on GPU where CPU silently places the node at angle 0. Labelled **INDICATIVE** — no GPU run was possible here (`cupy` cannot load `libnvrtc.so.12` in this environment), so the divergence is asserted from inspection only.

## Category

Defects 1–3: **bare-crash** on valid input (untyped `TypeError` / `KeyError` / pandas-internal `IntCastingNaNError`), Defect 1 also a **surface divergence** against five sibling layouts. Defect 4: misleading typed error. Defect 5: dead condition + suspected CPU/GPU divergence, INDICATIVE.

