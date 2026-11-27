You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

tool_create_tunnel masks room-existence ValueError as generic 'Internal tool error'

## Summary

`tool_create_tunnel` in `mempalace/mcp_server.py` swallows the `ValueError` raised by `palace_graph.create_tunnel()` when a referenced room doesn't exist. The MCP framework wraps the uncaught exception as the generic `"Internal tool error"`, so the caller never sees the real, useful reason: which room was missing, in which wing.

This makes the fail-loud behavior added in #1467 (and related room-existence validation) hard to act on in practice — operators see only a generic error and have to guess.

## Repro

With any MemPalace setup:

```
mempalace_create_tunnel(
    source_wing="wing_minerva",
    source_room="fx-invariants",        # exists
    target_wing="wing_minerva",
    target_room="does-not-exist-probe", # does NOT exist
)
```

Actual response (via MCP client):

```
{"error": "MCP call failed: McpError: Internal tool error"}
```

Expected response (mirroring how sibling tools `tool_add_drawer`, `tool_list_rooms`, `tool_update_drawer`, etc. handle `ValueError`):

```
{"error": "Target room 'does-not-exist-probe' does not exist in wing 'wing_minerva'"}
```

## Root cause

`mempalace/mcp_server.py` around line 906–921:

```python
def tool_create_tunnel(...):
    try:
        source_wing = sanitize_name(source_wing, "source_wing")
        source_room = sanitize_name(source_room, "source_room")
        target_wing = sanitize_name(target_wing, "target_wing")
        target_room = sanitize_name(target_room, "target_room")
    except ValueError as e:
        return {"error": str(e)}
    return create_tunnel(            # <-- this can also raise ValueError
        source_wing, source_room,
        target_wing, target_room,
        label=label,
        source_drawer_id=source_drawer_id,
        target_drawer_id=target_drawer_id,
    )
```

`palace_graph.create_tunnel()` raises `ValueError(f"Target room '{target_room}' does not exist in wing '{target_wing}'")` (palace_graph.py:531-532), but it's outside the `try` block, so it propagates out of the tool function and is rewritten by the MCP layer.

## Suggested fix

Extend the existing `try/except ValueError` around the `create_tunnel(...)` call, matching the pattern used in `tool_add_drawer`, `tool_update_drawer`, `tool_list_rooms`, etc:

```python
def tool_create_tunnel(...):
    try:
        source_wing = sanitize_name(source_wing, "source_wing")
        source_room = sanitize_name(source_room, "source_room")
        target_wing = sanitize_name(target_wing, "target_wing")
        target_room = sanitize_name(target_room, "target_room")
        return create_tunnel(
            source_wing, source_room,
            target_wing, target_room,
            label=label,
            source_drawer_id=source_drawer_id,
            target_drawer_id=target_drawer_id,
        )
    except ValueError as e:
        return {"error": str(e)}
```

Happy to send a PR with a regression test (`tests/test_mcp_server.py`) asserting the JSON-shape error message round-trips through `tool_create_tunnel` when the target room is missing.

## Environment

- mempalace `86a0b9c` (post-3.3.5, fix #1467 applied)
- Reproduced via MCP over stdio from a third-party client.

