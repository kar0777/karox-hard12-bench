You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Restricting S3 Purge queue to once every 60 seconds is very restrictive

Related Issue #10233
Related PR #10234

IMO this implementation is problematic for a tool being used in local development and at least in my case CI! I call purge_queue 3 times in my integration tests but the whole suite run takes < 2 mins with those calls being very close together.  So it will never pass on Moto 5.2.4

A preferred implementation in my opinion would allow for opt-out behaviour via configuration.  There is prior art in the codebase [MOTO_ALLOW_NONEXISTENT_REGION](https://github.com/getmoto/moto/blob/b2e1636ac8a3093120eb3575659c902c57853a2b/moto/settings.py#L101) which defaults to false

or (MOTO_S3_ALLOW_CROSSACCOUNT_ACCESS)[https://github.com/getmoto/moto/blob/b2e1636ac8a3093120eb3575659c902c57853a2b/moto/settings.py#L83] which defaults to true.  You can see example usage of this at https://github.com/getmoto/moto/blob/b2e1636ac8a3093120eb3575659c902c57853a2b/moto/s3/models.py#L2024

The purge queue method wouldn't change much, perhaps

```
    def purge_queue(self, queue_name: str) -> None:
        queue = self.get_queue(queue_name)
        now = unix_time()
        if sqs_enforce_strict_queue_purge_behaviour() and queue.last_purged_at is not None and now - queue.last_purged_at < 60:
            raise PurgeQueueInProgress(queue.name)
        queue.last_purged_at = now
        queue._messages = []
        queue._pending_messages = set()
```

Would a PR to such effect be tolerated?
