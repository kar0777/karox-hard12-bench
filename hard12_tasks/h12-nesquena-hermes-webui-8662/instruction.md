You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Agent update no longer waits for active Gateway runs and restarts the Gateway under them (exp-v0.52.587+, #8486 follow-up)

## What happens

Since **exp-v0.52.587** (#8486, which fixed #7293), an **Agent** update no longer waits for active Gateway-backed runs. A run whose resumable identity has been saved ("durable") is left out of the update's blocker check, because it survives a *WebUI* restart. An Agent update also restarts the Hermes Gateway, though: `_apply_update_inner` and `_apply_force_update_inner` call `_ensure_gateway_restart_for_agent_update()`. That restart is what is executing the run.

So with a Gateway-routed chat still running, an unforced Agent update now goes ahead. It changes the Agent checkout and restarts the Gateway, without the "Update anyway (interrupts N runs)" confirmation that #8486 added for runs it does count:
- **Older Agents:** the Gateway restart interrupts the run.
- **Newer Agents:** the restart may refuse after the checkout has already changed.

v0.52.544 (current stable) and exp-v0.52.586 refuse the same update before touching anything.

## Reproduction

The script is `docs/evidence/stable-3-audit-20261020/range-544-593/probe_agent_update_gateway.py` in the private workspace. It runs in each tag's own exported tree, registers a Gateway run exactly as that tree's `gateway_chat` does, and marks it durable on trees that have the #7293 handoff. It then calls the tree's real `apply_update("agent")`. The Agent dir is a temp dir, and the inner update step is a recorder, so nothing is mutated.

| tree | blocker snapshot | `apply_update("agent")` |
|---|---|---|
| v0.52.544 | 1 active run, blocked | refused: "Cannot update agent while 1 active chat stream and 1 active agent run is running" |
| exp-v0.52.586 | 1 active run, blocked | refused |
| exp-v0.52.587 | 0 runs, not blocked | **proceeds** to `_apply_update_inner(agent)` |
| exp-v0.52.593 | 0 runs, not blocked | **proceeds** |

## Cause

`api/updates.py` `_restart_blocker_snapshot()` takes its runs from `run_drain.webui_owned_active_runs()`, which excludes durable Gateway runs. That exclusion is right for a WebUI-only update, but wrong for `target == "agent"`. All three entry points share `_run_fenced_update(target, force_active_runs, run)`, so all three are affected:
- `apply_update`;
- `apply_force_update`;
- `apply_clear_lock`, the lock-recovery path.

## Fix shape

Make the admission check target-aware:
- **Agent updates:** active durable Gateway runs block an unforced update (v0.52.544 parity), both before and after the fence. The forced path's "interrupts N runs" count includes them.
- **WebUI updates:** keep the #7293 exemption, since those runs survive a WebUI-only restart.

Cover all three entry points.

Found by the whole-range forward audit for the next stable promotion (v0.52.544 → exp-v0.52.593). It is a range regression, so `exp-v0.52.587` is held until a fix ships.

