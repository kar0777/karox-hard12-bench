You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: v0.3 REST client raises NotImplementedError for list_task_push_notification_configs

### What happened?

`Client.list_task_push_notification_configs()` raises `NotImplementedError` when the client talks to a v0.3 agent over HTTP+JSON:

```
NotImplementedError: list_task_push_notification_configs not supported in v0.3 REST
```

The v0.3 REST binding defines this call as `GET /v1/tasks/{id}/pushNotificationConfigs`, and v0.3 REST servers serve it. That includes this SDK's own compat server: `REST03Adapter` mounts the route and `REST03Handler.list_push_notifications` handles it. The v0.3 JSON-RPC and gRPC client transports (`CompatJsonRpcTransport`, `CompatGrpcTransport`) both implement the call, so only REST users hit the error.

### Steps to reproduce

1. Start a server with `create_rest_routes(handler, enable_v0_3_compat=True)` and a push config store.
2. Create a task and two push notification configs through `CompatRestTransport`.
3. Call `CompatRestTransport.list_task_push_notification_configs(ListTaskPushNotificationConfigsRequest(task_id=...))`.

Expected: the response lists both configs. Actual: `NotImplementedError`, and no request is sent.

### Environment

a2a-sdk `main` (1.3.x), Python 3.13.
