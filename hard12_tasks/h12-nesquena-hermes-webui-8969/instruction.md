You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

POST /api/session/new accepts a profile that isn't a valid profile name

`POST /api/session/new` accepts a profile that isn't a valid profile name.

**Seen on:** master `f65960b46351` (exp-v0.52.641).

## What happens

`POST /api/session/new` passes `body.get("profile") or None` through unchecked (`api/routes.py` ~19394/19418/19424/19518 → `new_session(profile=...)`). The real client always sends a valid name, so this needs a crafted request. Results recorded on master, with the agent stubbed:

| `profile` sent | `/api/session/new` | cached session's `profile` | then `/api/chat/start` naming `default` |
|---|---|---|---|
| `123`, `true`, `["default"]`, `{"name": "default"}` | 200 | the raw value (int, bool, list, dict) | 200, a turn starts, and the profile stays the non-string value |
| `"../evil"`, `"No Such Profile"`, `"ghost"` | 200 | the raw string | 200, a turn starts, and the session is retagged to `default` |

- **Path traversal is already blocked downstream.** `get_hermes_home_for_profile` falls back to the default home for a name that doesn't match the profile-name format, so `"../evil"` reads no other directory. No file named after it was created in the run.
- **The real cost:** a session can exist, at least in memory, with an owner that no ownership check can read.
- **After #8853:** chat/start answers 404 for the non-string cases, because ownership is unverifiable. So the session `/api/session/new` just returned can't be used, and the request that created it got 200.

## Fix shape

Validate `profile` the way the other routes already do (chat/start, import and archive answer `400 "invalid profile"` via `_PROFILE_ID_RE`):
- **`None` or `""`:** unchanged; the active profile applies.
- **A non-string, or a string that fails `_PROFILE_ID_RE.fullmatch`:** `400 "invalid profile"` before anything is created.
- **Optional:** an unknown but well-formed name (`"ghost"`) could get the same 400, if creating a session under a profile that doesn't exist is never wanted. That's a product call; today the session is retagged on its first chat/start.

Add a test that posts each of the values above and asserts 400 with nothing cached.

Found by the senior review of #8853 (gate on `4116564cc867`), and reproduced here.

