You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

v0.3 gRPC client raises A2AClientError for every error from a2a-go's v0.3 server

Against a2a-go's v0.3 gRPC server, every error comes back as a plain `A2AClientError`. Task not found, invalid params, unsupported operation and sending to a finished task all look the same. The v0.3 JSON-RPC client maps them correctly against the same server.

`_map_grpc_error` in `compat/v0_3/grpc_transport.py` only recognizes a status message shaped like `"TaskNotFoundError: ..."`, which is the format a2a-python's own v0.3 server writes. a2a-go sends a plain message and names the error in `ErrorInfo.reason` (`TASK_NOT_FOUND`), the same way the v1 gRPC client already reads it.

```
get_task(missing) -> A2AClientError: gRPC Error NOT_FOUND: failed to get task: task not found
```

main @ 09c9347

