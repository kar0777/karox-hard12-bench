You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

button.clicked() never returns after Client.delete() and strands one task per abandoned page load (1.2 GB over 150k loads)

*Filed by Claude Code on @evnchn's behalf.*

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
import asyncio

from nicegui import Client, app, background_tasks, ui


@ui.page('/')
def index() -> None:
    button = ui.button('go')

    async def waiter() -> None:
        await button.clicked()  # never returns once the client is deleted
    background_tasks.create(waiter(), name='waiter')


@app.on_startup
async def monitor() -> None:
    while True:
        await asyncio.sleep(5)
        Client.prune_instances(client_age_threshold=1)
        parked = [t for t in asyncio.all_tasks() if t.get_name() == 'waiter']
        print(f'>>> live clients: {len(Client.instances):>5} | parked waiters: {len(parked):>6}', flush=True)


ui.run(reload=False)
```

Drive it with HTTP-only page loads — no browser, no websocket:

```bash
for i in $(seq 1 4000); do curl -s -o /dev/null http://localhost:8080/ & done; wait
```

### Description

**TL;DR:**

`await button.clicked()` never returns and never gets cancelled when its client is deleted, so every abandoned page load permanently strands one task.

`Client.delete()` ends with `self._connected.set()  # for terminating connected() waits`, which wakes the `await self.client.connected()` inside `clicked()` into a **success** return — so it proceeds to `await event.wait()` for a click that can no longer arrive.

Measured: 150,000 HTTP-only page loads leave 148,545 parked tasks and grow RSS by **1,215 MB**, with no reclamation.

Same root cause as #6226 — `connected()` reporting success on a deleted client — but the symptom is an unbounded task leak rather than a raise, so it is filed separately. Sibling of #6230, found in the same sweep.

**Expected**

`parked waiters` returns to 0 as the clients are pruned, the way `live clients` does.

**Actual**

`parked waiters` equals the cumulative number of page loads and never decreases:

```
>>> live clients:   192 | parked waiters:    192
>>> live clients:   519 | parked waiters:   3079
>>> live clients:     0 | parked waiters:   4000     <- first 4000 loads done
>>> live clients:   623 | parked waiters:   5360
>>> live clients:     0 | parked waiters:   8000     <- second 4000 done
>>> live clients:     0 | parked waiters:  12000     <- third 4000 done
```

`live clients` does return to 0, so the `Client` objects themselves are released correctly. It is only the stranded tasks — and everything they hold, including the `ui.button` element — that accumulate.

**Mechanism**

`Button.clicked()` (`nicegui/elements/button.py` lines 62-67) registers a one-shot event, awaits `self.client.connected()`, then awaits that event. `Client.delete()` (`nicegui/client.py` line 472) sets `_connected`, which releases the `connected()` wait as a normal return rather than an error, and nothing afterwards observes that the client is gone. The second await has no timeout, no cancellation and no deletion hook, so the task parks for the lifetime of the process.

`background_tasks.create` keeps a strong reference in its module-level `running_tasks` set until the task completes, so a parked task is never garbage collected.

Three other methods have the same `await self.client.connected()` followed by `await self._initialized_event.wait()` shape and appear to share the defect, though I only measured the button:

- `ui.scene.initialized()` — `nicegui/elements/scene/scene.py` line 187
- `ui.scene_view.initialized()` — `nicegui/elements/scene/scene_view.py` line 79
- `ui.leaflet.initialized()` — `nicegui/elements/leaflet/leaflet.py` line 105

### NiceGUI Version

3.15.0

### Python Version

3.14.2

### Browser

Other

### Operating System

macOS

### Additional Context

<details>
<summary><b>Growth to 1.2 GB — the measured run</b></summary>

30 rounds of 5,000 HTTP-only page loads on released 3.15.0 / Python 3.14.2 / macOS 26 arm64. RSS is current resident size read from `ps -o rss=`, not `ru_maxrss` (which is a high-water mark and cannot show reclamation). A `gc.collect()` ran before every sample, so nothing here is waiting on the cycle collector.

| parked waiters | RSS above baseline |
|---:|---:|
| 160 | 10.9 MB |
| 3,382 | 173.1 MB |
| 6,430 | 254.6 MB |
| 64,747 | 658.6 MB |
| 96,523 | 854.1 MB |
| 140,435 | 1,163.5 MB |
| 148,545 | **1,215.4 MB** |

Steady-state marginal cost is about 6.9 KB per stranded task. The curve is linear with no plateau, and `live clients` returned to 0 at the end of the run while the 148,545 waiters remained.

</details>

<details>
<summary><b>Why the leak needs `background_tasks.create` to be visible</b></summary>

Worth stating because it changes what a reader will see if they vary the repro.

If the waiter is started with a plain `asyncio.create_task` and nothing holds the returned task, the stranded task forms a reference cycle — task holds coroutine holds the `asyncio.Event` whose `_waiters` holds the task's future — that is unreachable from outside, and the cycle collector reclaims it. The count then returns to 0 and the leak looks like it does not exist. It is a silent destruction of a pending task rather than correct cleanup, but it does not accumulate memory.

`background_tasks.create` is the documented way to start background work in NiceGUI, and it keeps a strong reference in `running_tasks` until completion. Since the task never completes, that reference is permanent, and the leak is real and unbounded.

I initially measured this the first way and briefly concluded there was no leak. Correcting it is what produced the numbers above.

</details>

<details>
<summary><b>What is not claimed</b></summary>

- Only `Button.clicked()` was measured. The three `initialized()` methods are listed on the basis of matching source shape, not a run.
- The measurement uses HTTP-only clients pruned by `prune_instances`, which is the cheapest way to create and destroy many clients. A client that connects and later disconnects reaches the same `await event.wait()` park by inspection, but I did not measure that path, since it needs a real browser per cycle.
- `client_age_threshold=1` only shortens the wait. NiceGUI already runs `app.timer(10, Client.prune_instances)` with a 60 s default, so the same accumulation happens on the stock schedule, just more slowly.

</details>

<details>
<summary><b>Provenance</b></summary>

Found while sweeping for other instances of the shape reported in #6226. An adversarial review pass by Codex, a different model lineage, independently flagged the same four call sites from the source before any of this was measured.

</details>

