You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

hallways.py: _HALLWAY_FILE is hardcoded to ~/.mempalace/hallways.json, not palace-scoped

`mempalace/hallways.py:52` hardcodes the hallway store path:

```python
_HALLWAY_FILE = os.path.join(os.path.expanduser("~"), ".mempalace", "hallways.json")
```

This path is not derived from `MempalaceConfig.palace_path`, so two palaces on one host share one global `hallways.json`. Mining hallways into one palace silently pollutes the others. `tunnels.json` was migrated to palace-scoped in 3.3.6; hallways didn't get the same treatment.

## Reproduction (mempalace 3.4.0)

```python
import os
os.environ["MEMPALACE_PALACE_PATH"] = "/tmp/a/palace"
from mempalace.config import MempalaceConfig
from mempalace import hallways
cfg = MempalaceConfig()
print(cfg.tunnel_file)        # /tmp/a/tunnels.json
print(hallways._HALLWAY_FILE) # ~/.mempalace/hallways.json

hallways._save_hallways([{"id": "hall_a", "wing": "wing_a", ...}])

os.environ["MEMPALACE_PALACE_PATH"] = "/tmp/b/palace"
cfg = MempalaceConfig()
print(cfg.tunnel_file)        # /tmp/b/tunnels.json    ← scoped
print(hallways._HALLWAY_FILE) # ~/.mempalace/hallways.json  ← unchanged

hallways._load_hallways()     # returns palace-a's records
```

## Suggested fix

Apply the `palace_graph._get_tunnel_file()` pattern: add `MempalaceConfig.hallway_file` resolving to `<dirname(palace_path)>/hallways.json`, read via `_get_hallway_file(config)`, with a `_legacy_hallway_file()` fallback that logs a one-line warning when the legacy file exists but the configured one doesn't. Keep atomic-write and 0600-perm semantics.

## Environment

- Verified against HEAD (`2ec4bae`) and v3.4.0 (`pip install mempalace==3.4.0`).
- Linux, Python 3.9.

## Related

- Discussion #1220 — multi-palace isolation. Names the same pattern for `known_entities.json` and `config.json`.
- #1454 — multi-palace deployment recipe docs (#832, #1096, #1043, #678, #1300).
- 3.3.6 tunnel-file scoping (`palace_graph._get_tunnel_file` + `_legacy_tunnel_file`) is the precedent worth matching.
- #1741 — exposed `list_hallways`/`delete_hallway` via MCP. Newly visible at the MCP surface.

