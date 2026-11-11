You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Error in post_publish_all() hides the PublishError of the same item type

### Library Version

1.4.0

### Python Version

3.11.15

### Operating System

macOS

### Authentication Method

Azure CLI (az login)

### What is the problem?

`ItemPublisher.publish_all()` publishes the items of one item type and collects each failure in `errors`. Then it calls `self.post_publish_all()`, and only after that it raises `PublishError(errors, logger)`:

```python
self.post_publish_all()

if errors:
    raise PublishError(errors, logger)
```

If `post_publish_all()` raises, the `raise PublishError(...)` line never runs. This means that the caller only gets the error from the post-publish step. The items that failed to publish are missing from the exception, although they are logged. Neither does the result name them (`deploy_with_config` sets `DeploymentResult.message` to `str(e)`).

This happens in 2 cases:

- For Lakehouses: `LakehousePublisher.post_publish_all()` publishing shortcuts. With `enable_shortcut_publish` set and `continue_on_shortcut_failure` not set, a failed shortcut raises `FailedPublishedItemStatusError`. 
- For Semantic Models: `SemanticModelPublisher.post_publish_all()` binding connections. With `enable_strict_semantic_model_binding` from #1171, a failed binding raises `FailedPublishedItemStatusError`.

In current situation, a failed run reports one and hides the other. See below for example. 

Note: This fortunately does not apply to bulk mode, since it does not use `publish_all()`

### Steps to reproduce

1. Set the `enable_shortcut_publish` feature flag.
2. Put two lakehouses in the repository. Make `LakehouseA` fail to publish and give `LakehouseB` a shortcut that fails to publish.
3. Run `publish_all_items()`.
--> `FailedPublishedItemStatusError: Failed to publish '<shortcut>' for lakehouse LakehouseB` and `LakehouseA` appears only in an earlier log line. 

I've reproduced this against `main` with a stub `LakehousePublisher` whose `publish_one()` raises for one item and whose `post_publish_all()` raises. The real `publish_all()` raised only `FailedPublishedItemStatusError`. The exception had no `.errors` attribute, showing that code that catches `PublishError` misses both failures.

### Expected behavior

The exception names both failures: The failing publish for `LakehouseA` and the failing shortcut for `LakehouseB`.

### Actual behavior

The exception names only the shortcut of `LakehouseB`. `LakehouseA` appears only in the log.

### Is there an ideal solution?

I suggest keeping the call order, since `post_publish_all()` must still run for the items that did publish (e.g. to bind connections). If both steps then fail, change only the exception that is raised:

In `ItemPublisher.publish_all()`:

```python
try:
    self.post_publish_all()
except BaseCustomError as e:
    if errors:
        raise PublishError(errors, logger, post_publish_error=e) from e
    raise

if errors:
    raise PublishError(errors, logger)
```

And, in `PublishError`, add an optional `post_publish_error` and name it in the message:

```python
def __init__(
    self, errors: list[tuple[str, Exception]], logger: Logger, post_publish_error: Optional[Exception] = None
) -> None:
    self.errors = errors
    self.post_publish_error = post_publish_error
    failed_names = [name for name, _ in errors]
    message = f"Failed to publish {len(errors)} item(s): {failed_names}"
    if post_publish_error is not None:
        message += f". The post-publish step also failed: {post_publish_error}"
    # additional_info and super().__init__() remain as is
```

Result:

- The message names both failures. `deploy_with_config` copies the message to `DeploymentResult.message`, so the result names both failures too.
- `errors` keeps only the items that failed, so the item count stays correct.
- The caller still gets a `PublishError`, as the `publish_all()` docstring states.
- N.b. New parameter remains optional. Current callers and tests do not change.
- If no item failed, the post-publish error is raised as it is now, with the same type and message.

### Additional context, screenshots, logs, error output, etc

Found during the review of #1171. Agreed to have a separate issue and PR. 
