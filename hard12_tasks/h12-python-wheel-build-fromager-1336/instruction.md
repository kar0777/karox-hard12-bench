You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Top-level pre-resolution leaves an unprocessed, edge-less node in graph.json when a second rule for the same package bypasses cooldown

With `--min-release-age` set, two top-level requirements for the same package (an unpinned rule followed by an exact `==` pin on a release younger than the cooldown window) leave a node in graph.json that bootstrap never processed: no sdist, no build-system edges. `build-parallel` then schedules that node in round 1 and fails to install its build backend from the local wheel server.

## Reproduction

requirements.txt, in this order:

```
codeflare-sdk
codeflare-sdk==0.39.1
```

At the time of the run, 0.39.1 (released 2026-09-15) was inside a 3-day cooldown and 0.39.0 was the newest release outside it.

```
$ fromager --min-release-age 3 bootstrap -r requirements.txt
...
codeflare-sdk: cooldown blocked 1 version(s): 0.39.1
codeflare-sdk: codeflare-sdk resolves to 0.39.0
codeflare-sdk: cooldown bypassed as the top-level requirement uses == pin
codeflare-sdk: codeflare-sdk==0.39.1 resolves to 0.39.1
...
codeflare-sdk-0.39.1: new toplevel dependency codeflare-sdk==0.39.1 resolves to 0.39.1
```

There is no `new toplevel dependency codeflare-sdk==0.39.0` line and no sdist for 0.39.0 is produced, but graph.json contains both nodes:

```
"codeflare-sdk==0.39.0": {"pre_built": false, "edges": []}          # only a ROOT edge points to it
"codeflare-sdk==0.39.1": {"pre_built": false, "edges": [{"key": "poetry-core==2.4.1", "req_type": "build-system", ...}, ...]}
```

```
$ fromager build-parallel work-dir/graph.json
round 1: starting to build 16 node(s): codeflare-sdk==0.39.0, flit-core==3.12.0, ..., poetry-core==2.4.1, ...
ERROR codeflare-sdk-0.39.0: Failed to install build-system dependency ... poetry-core>=1.6.0
```

Swapping the two lines (pin first) makes the problem disappear, so it is order-dependent.

## Root cause

1. `Bootstrapper.bootstrap()` calls `_resolve_and_add_top_level()` for each rule in file order, which resolves and immediately adds the result to the graph ([`_bootstrapper.py#L139-L189`](https://github.com/python-wheel-build/fromager/blob/0883ce2/src/fromager/bootstrapper/_bootstrapper.py#L139-L189)). It then pushes a `Resolve` item that resolves the same rule a second time ([`_bootstrapper.py#L277-L288`](https://github.com/python-wheel-build/fromager/blob/0883ce2/src/fromager/bootstrapper/_bootstrapper.py#L277-L288)).
2. The resolver caches known versions per package and filters them by specifier only, without re-applying the cooldown ([`bootstrap_requirement_resolver.py#L118-L136`](https://github.com/python-wheel-build/fromager/blob/0883ce2/src/fromager/bootstrap_requirement_resolver.py#L118-L136), [`#L295-L309`](https://github.com/python-wheel-build/fromager/blob/0883ce2/src/fromager/bootstrap_requirement_resolver.py#L295-L309)). That sharing is intentional (#1187). So the first resolution of the unpinned rule returns 0.39.0, the pinned rule adds 0.39.1 to the shared cache, and the second resolution of the unpinned rule returns 0.39.1.
3. `Start.run` skips `add_to_graph` for `TOP_LEVEL` because the node was "already added in _resolve_and_add_top_level" ([`_start.py#L47-L55`](https://github.com/python-wheel-build/fromager/blob/0883ce2/src/fromager/bootstrapper/_start.py#L47-L55)), and the second `Start(0.39.1)` is dropped by `has_been_seen`. Nothing removes or corrects the stale 0.39.0 node from step 1.

## Expected behavior

graph.json should only contain top-level nodes that bootstrap actually processed. Either the top-level graph nodes should be derived from the versions the `Resolve` phase settles on (after the shared cache is warm), or each version added in pre-resolution should be bootstrapped.

## Impact

Any package that is listed unpinned and, further down, pinned to a release inside the cooldown window hits this. The failure only surfaces when the wheel for the stale version is not already on the cache server, so it stayed hidden until a cache index was recreated.

