You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] install --update re-downloads a package revision already in the cache, then fails with "already exists"

### Describe the bug

**Environment:** conan 2.20.0 (Windows 11) and conan 2.32.0 (Ubuntu 22.04 / WSL2) — reproduced on both.

If the remote's latest package revision is already in the local cache but is **not** the cache's latest prev, `conan install --update` marks the package `Update`, re-downloads that prev, then fails storing it:

```
ERROR: Reference 'reprolib/1.0#<rrev>%<ts>:<pid>#<prev>%<ts>' already exists
```

Only one remote is needed.

This looks like a missing guard in `_evaluate_in_cache` (`conan/internal/graph/graph_binaries.py`):

```python
if cache_time < node.pref_timestamp and cache_latest_prev != node.pref:
    node.binary = BINARY_UPDATE
```

It compares only the cache's *latest* prev, and never checks whether the remote's prev is in the cache at all. The download then reaches the unguarded INSERT in `Cache.create_pkg_layout()` (`conan/internal/cache/cache.py:152`) -> `ConanReferenceAlreadyExistsInDB` (`packages_table.py:87`).

`Cache.exists_prev()` already performs exactly this check, and is used in `download.py:64` and in the locked-prev branch at `graph_binaries.py:334` — but not here.

**Workaround:** `conan remove "<full pref>" -c`, then re-run. Lockfiles do not help: normal lockfiles pin recipe revisions only, so the locked-prev branch is never entered.

### How to reproduce it

1. `conan create` with content X -> **prev_A**  (do *not* upload)
2. `conan create` with content Y -> **prev_B**  (cache latest is now prev_B)
3. Upload **only prev_B**
4. Upload **prev_A** explicitly -> prev_A becomes the server's newest
5. `conan install --requires=reprolib/1.0 --update` -> **ERROR ... already exists**
6. `conan remove "<pref of prev_A>" -c`, retry -> succeeds

The recipe declares no settings/options so `package_id` is constant; packaged content comes from an env var that is not part of `package_id`, so both builds share one `package_id` and differ only in `prev`.

Order matters — conan skips re-uploading an existing revision and does not refresh its timestamp, so uploading prev_A before prev_B makes the repro silently pass.

Actual output:

```
reprolib/1.0: Current package revision is older than the remote one
    reprolib/1.0#a1ceff85...:da39a3ee...#d9cc070c... - Update (reprosrv)
-------- Downloading 1 package --------
Retrieving package da39a3ee... from remote 'reprosrv'
ERROR: Reference '...#d9cc070c...%1789077750.0' already exists
```

Expected: the revision is already cached and byte-identical, so it should resolve to `BINARY_CACHE` without downloading.

<details>
<summary>Self-contained reproducer (throwaway CONAN_HOME + conan_server, ~30s)</summary>

`conanfile.py`:

```python
import os
from conan import ConanFile
from conan.tools.files import save


class ReproConan(ConanFile):
    """Minimal package for the conan --update / exists_prev repro.

    No settings and no options, so package_id is constant. The packaged content
    is driven by REPRO_MARKER, which is NOT part of package_id -- so changing it
    produces a NEW package revision (prev) for the SAME package_id. That is what
    lets the repro place two prevs of one package_id in the cache.
    """
    name = "reprolib"
    version = "1.0"

    def build(self):
        pass

    def package(self):
        marker = os.environ.get("REPRO_MARKER", "default")
        save(self, os.path.join(self.package_folder, "marker.txt"), marker)
```

`repro.sh`:

```bash
#!/usr/bin/env bash
# Repro: `conan install --update` re-downloads a package revision that is
# already in the local cache, then fails to store it.
#
#   ERROR: Reference '<pref>' already exists
#
# Requires: conan 2.x and conan_server on PATH. Uses a throwaway CONAN_HOME and
# a throwaway server; touches nothing else on the machine.
set -u

ROOT="${1:-$(pwd)/conan-repro-run}"
CONAN_SERVER_BIN="${CONAN_SERVER_BIN:-conan_server}"
PORT=9300

rm -rf "$ROOT"; mkdir -p "$ROOT/home" "$ROOT/server" "$ROOT/pkg"
cp "$(dirname "$0")/conanfile.py" "$ROOT/pkg/"
export CONAN_HOME="$ROOT/home"

echo "== 0. start a throwaway conan_server on :$PORT =="
"$CONAN_SERVER_BIN" -d "$ROOT/server" >"$ROOT/server-init.log" 2>&1 &
SRV=$!; sleep 4; kill "$SRV" 2>/dev/null; wait "$SRV" 2>/dev/null   # generate server.conf
sed -i 's|^\[write_permissions\]|[write_permissions]\n*/*@*/*: demo|' "$ROOT/server/server.conf"
"$CONAN_SERVER_BIN" -d "$ROOT/server" >"$ROOT/server.log" 2>&1 &
SRV=$!; sleep 4
trap 'kill "$SRV" 2>/dev/null' EXIT

conan profile detect --force >/dev/null 2>&1
conan remote add reprosrv "http://localhost:$PORT" >/dev/null 2>&1
conan remote login reprosrv demo -p demo >/dev/null 2>&1

cd "$ROOT/pkg"
echo "== 1. build prev_A (do NOT upload yet) =="
REPRO_MARKER=A conan create . >/dev/null 2>&1

echo "== 2. build prev_B (same package_id, different content) =="
REPRO_MARKER=B conan create . >/dev/null 2>&1
# Cache now holds prev_A (older) and prev_B (newer == cache-latest).

echo "== 3. upload ONLY prev_B (\`:*\` uploads the latest prev) =="
conan upload "reprolib/1.0:*" -r reprosrv -c >/dev/null 2>&1
# NOTE: prev_A must reach the server AFTER prev_B. Conan skips re-uploading a
# revision that already exists ("already in server") and does NOT refresh its
# timestamp, so uploading prev_A first would make this repro silently pass.

read RREV PID PREV_A PREV_B <<< "$(conan list 'reprolib/1.0:*#*' --format=json 2>/dev/null | python -c "
import sys,json
d=json.load(sys.stdin)['Local Cache']
for ref,v in d.items():
  for rrev,rv in v['revisions'].items():
    for pid,pv in rv['packages'].items():
      r=sorted(pv['revisions'].items(), key=lambda kv: kv[1]['timestamp'])
      print(rrev, pid, r[0][0], r[-1][0])")"

echo "== 4. re-upload prev_A so it becomes NEWEST on the server =="
conan upload "reprolib/1.0#${RREV}:${PID}#${PREV_A}" -r reprosrv -c >/dev/null 2>&1

echo
echo "PRECONDITION:"
echo "  cache latest prev  = $PREV_B   (cache also holds $PREV_A, older)"
echo "  server latest prev = $PREV_A   (already present in cache, but NOT cache-latest)"
echo
echo "== 5. conan install --update  -> EXPECT: ERROR ... already exists =="
conan install --requires=reprolib/1.0 --update -r reprosrv
RC=$?
echo "exit=$RC"
echo
if [ "$RC" -ne 0 ]; then
  echo "== 6. REMEDY: drop the colliding prev from cache, retry =="
  conan remove "reprolib/1.0#${RREV}:${PID}#${PREV_A}" -c
  conan install --requires=reprolib/1.0 --update -r reprosrv >/dev/null 2>&1
  echo "retry exit=$?  (0 == remedy works)"
fi
```

</details>

