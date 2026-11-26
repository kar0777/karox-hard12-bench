You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

v0.3 gRPC compat drops task status timestamp and three other fields

## What happens

Over the v0.3 gRPC compat endpoint, task statuses have no `timestamp`. The v0.3 JSON-RPC and REST compat endpoints include it.

Round trip through `compat/v0_3/proto_utils.py`:

```
timestamp after gRPC round trip: None      (sent 2026-03-15T10:30:00Z)
icon_url: None                              (sent http://x/icon.png)
skill security: None                        (sent [{'oauth': ['read']}])
```

`OAuth2SecurityScheme.oauth2_metadata_url` is dropped the same way.

## Why

`proto_utils.py` doesn't map these four fields in either direction. `conversions.py`, used by the JSON-RPC and REST compat paths, maps all four.

## Version

main @ f3ac824

