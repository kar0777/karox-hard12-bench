You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add max_spans limit to InMemorySpanExporter to prevent unbounded memory growth

### Is your feature request related to a problem?

While building a local observability dashboard on top of the OpenTelemetry Python SDK, I noticed that InMemorySpanExporter stores all exported spans in an unbounded list with no way to cap the size.
InMemorySpanExporter stores all exported spans in an unbounded list (self._finished_spans). In a short-lived test this is fine, but in any long-running process — a dev server, a background worker, or a monitoring loop these spans accumulate indefinitely and memory grows without bound until the process crashes or gets killed.

### Describe the solution you'd like

 Add an optional max_spans: int parameter to __init__ (defaulting to None for current unbounded behavior). When the limit is reached, either discard incoming spans or evict the oldest ones using a circular buffer (collections.deque(maxlen=max_spans)). The deque approach would be a one-line change to the existing implementation and would preserve the most recent spans automatically.

### Describe alternatives you've considered

Manually calling clear() periodically — but this loses all span history rather than keeping the most recent ones.

### Additional Context

This is particularly useful for developers using InMemorySpanExporter outside of pure unit tests, such as local observability dashboards or dev servers.

### Would you like to implement a fix?

Yes

### Tip

<sub>[React](https://github.blog/news-insights/product-news/add-reactions-to-pull-requests-issues-and-comments/) with 👍 to help prioritize this issue. Please use comments to provide useful context, avoiding `+1` or `me too`, to help us triage it. Learn more [here](https://opentelemetry.io/community/end-user/issue-participation/).</sub>
