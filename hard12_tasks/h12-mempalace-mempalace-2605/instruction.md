You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Historical add_triple replay duplicates an identical closed validity interval

**What happened?**
In an isolated MemPalace 3.10.0 pilot, retrying an identical closed historical relationship through `KnowledgeGraph.add_triple` produced two different IDs and two identical as-of results. Open-fact deduplication and supersession are separate cases.

This is a specific historical-interval continuation of the broader duplication concern in #655, not a claim that all graph inserts duplicate. Related #2268 / #2286 and #1139 concern open-fact provenance/reporting rather than replay of a closed interval.

**What did you expect?**
A supported way to replay the same historical source assertion after interruption without creating another logical assertion or losing its interval/provenance. Distinct recurring intervals and genuinely independent source assertions must remain distinguishable; unconditional subject/predicate/object deduplication would be incorrect.

Is `add_triple` intentionally append-only for closed intervals? If so, is there a supported historical import/replay API or stable assertion identity callers should use instead? Asking for the intended contract before proposing a patch.

**How to reproduce:**
The following reduces the executed synthetic pilot case (no private corpus):

```python
from mempalace.knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph(":memory:")
kwargs = dict(
    valid_from="2025-01-01T00:00:00Z",
    valid_to="2025-02-01T00:00:00Z",
    source_closet="synthetic-replay-fixture",
)
first = kg.add_triple("Pilot History", "was", "Archived", **kwargs)
second = kg.add_triple("Pilot History", "was", "Archived", **kwargs)
rows = kg.query_entity("Pilot History", as_of="2025-01-15T00:00:00Z")
print(first == second, len(rows))
kg.close()
```

Executed file-backed pilot result: different IDs; two identical historical relationships persisted and returned by the as-of query. Database quick_check returned `ok`. The in-memory snippet is a reduction of that case, not a claim of a separately executed test.

**Source inspection:**
At develop commit `8c4865f70c49b6346c53474a9e5684c5f17d3fa9`, the duplicate lookup still selects only `valid_to IS NULL`; new IDs include filing time. That head was inspected, not installed/tested.

**Environment:**
- Linux
- Python 3.11 dedicated runtime
- MemPalace 3.10.0, stock SQLite knowledge graph

A useful acceptance case would preserve one logical assertion across an identical historical retry while retaining distinct validity intervals and source identities. No workaround or production data changes were made.

