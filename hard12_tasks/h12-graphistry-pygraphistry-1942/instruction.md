You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

bug(gfql): public filter_by_dict/filter_nodes_by_dict crash on polars frames (resolver says POLARS, mask builder is pandas-idiom)

Amplification round-001 (agent-03): `filter_nodes_by_dict`/`filter_by_dict` on polars frames raise `AttributeError: 'assign'` — the resolver routes POLARS while `filter_mask_by_dict` remains pandas-idiom. Same class as the resolve_input_engine migrations in #1873/#1878: either migrate the surface or route it through the polars predicate path. Also from the same sweep: `seeded_typed_hop` fast path declines on ANY lazy frame (values correct, sub-ms path silently lost — chain_fast_paths.py:391), and `get_degrees` on nodes-only diverges (polars bare assert vs pandas typed message).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
