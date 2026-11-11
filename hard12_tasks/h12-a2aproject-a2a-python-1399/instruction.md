You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: TaskEventStream methods don't receive ServerCallContext

### What happened?

**Version:** a2a-sdk 1.2.1
 
 ### Problem
 
 `TaskEventStream` (`a2a/server/cluster/event_stream.py` L17–32) is keyed only by `task_id`:
 
 ```python
 async def publish(self, task_id: str, event: VersionedEvent) -> None: ...
 def subscribe(self, task_id: str, *, after: TaskVersion) -> AsyncGenerator[VersionedEvent, None]: ...
 async def destroy(self, task_id: str) -> None: ...
 ```
 
 `TaskStore`, `VersionedTaskStore` and `PushNotificationConfigStore.{set,get,delete}_info` all take `context: ServerCallContext`. `TaskEventStream` and `PushNotificationConfigStore.get_info_for_dispatch` don't.
 
 Context-derived identity is already central to the SDK — `OwnerResolver = Callable[[ServerCallContext], str]`, and `DatabaseTaskStore` scopes every query by `owner = self.owner_resolver(context)`. `TaskEventStream` can't participate.
 
 ### Impact
 
 `DefaultRequestHandlerV2` holds one `event_stream` from construction (L143) and calls `publish` (L304) / `subscribe` (L571) with no caller information, so an implementation is permanently bound to its startup resources. That rules out selecting a backing resource per caller, refreshing credentials at a request boundary, propagating auth downstream, or request-scoped tracing — all of which `TaskStore` supports today.
 
 Related: `DatabaseTaskEventStream` filters only on `task_id`/`seq`, never on the `owner` column it writes. Authorization is enforced upstream (`_versioned_store.get(task_id, context)` precedes subscribe), so the default composition is safe — but the stream can't check independently.
 
 ### Proposed change
 
 Add `context: ServerCallContext` to the three methods, optional for source compatibility:
 
 ```python
 async def publish(self, task_id: str, event: VersionedEvent, context: ServerCallContext | None = None) -> None: ...
 def subscribe(self, task_id: str, *, after: TaskVersion, context: ServerCallContext | None = None) -> ...: ...
 async def destroy(self, task_id: str, context: ServerCallContext | None = None) -> None: ...
 ```
 
 The handler already holds the context at both call sites.
 
 `get_info_for_dispatch` has the same gap — dispatch runs after the request completes, so it needs a stored context, not a live one.

### Relevant log output

```shell

```

### Code of Conduct

- [x] I agree to follow this project's Code of Conduct
