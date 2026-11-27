You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ProcessResourceDetector collects CLI args by default

### Describe your environment

_No response_

### What happened?

`ProcessResourceDetector` sets `process.command_args` and `process.command_line` by default. This can be problematic from a security perspective because these attributes can contain secrets or other sensitive data from command-line arguments. Furthermore, the spec says they are both supposed to be opt-in and should not be collected by default unless sensitive data is sanitized:

https://opentelemetry.io/docs/specs/semconv/resource/process/

### Steps to Reproduce

```
python -c 'from opentelemetry.sdk.resources import ProcessResourceDetector; r = ProcessResourceDetector().detect(); print(r.attributes.get("process.command_args")); print(r.attributes.get("process.command_line"))' --api-key=secret-value
```

### Expected Result

`ProcessResourceDetector` should not collect or emit `process.command_args` or `process.command_line` by default.

### Actual Result

`ProcessResourceDetector` collects and emits `process.command_args` or `process.command_line` by default.

### Additional context

`ProcessResourceDetector` is not loaded by default. This issue is about the detector behavior once used.

### Would you like to implement a fix?

Yes

### Tip

<sub>[React](https://github.blog/news-insights/product-news/add-reactions-to-pull-requests-issues-and-comments/) with 👍 to help prioritize this issue. Please use comments to provide useful context, avoiding `+1` or `me too`, to help us triage it. Learn more [here](https://opentelemetry.io/community/end-user/issue-participation/).</sub>
