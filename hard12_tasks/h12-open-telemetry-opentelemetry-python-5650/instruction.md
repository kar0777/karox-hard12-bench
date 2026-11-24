You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] BatchSpanProcessor missing validation for export_timeout_millis <= 0

### Describe your environment

OS: macOS / Linux
Python version: 3.10+
SDK version: main

### What happened?

In `opentelemetry-sdk` (`opentelemetry.sdk.trace.export.BatchSpanProcessor` and `BatchLogRecordProcessor`), parameters like `max_queue_size`, `schedule_delay_millis`, and `max_export_batch_size` validate that values must be positive integers and raise a `ValueError` if `<= 0`.

However, `export_timeout_millis` is missing validation for values `<= 0`. Initializing `BatchSpanProcessor(ConsoleSpanExporter(), export_timeout_millis=-500)` or `export_timeout_millis=0` is accepted without raising a `ValueError`.

### Steps to Reproduce

from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# 1. schedule_delay_millis correctly validates <= 0:
try:
    BatchSpanProcessor(ConsoleSpanExporter(), schedule_delay_millis=0)
except ValueError as e:
    print("schedule_delay_millis validation working:", e)

# 2. export_timeout_millis is missing validation:
bsp = BatchSpanProcessor(ConsoleSpanExporter(), export_timeout_millis=-500)
print("Accepted without ValueError!")

### Expected Result

Initializing `BatchSpanProcessor` or `BatchLogRecordProcessor` with `export_timeout_millis <= 0` should raise a `ValueError("export_timeout_millis must be positive.")`.

### Actual Result

Accepted without raising a `ValueError`.

### Additional context

Location: opentelemetry-sdk/src/opentelemetry/sdk/trace/export/__init__.py in `BatchSpanProcessor._validate_arguments()`.

I am opening a PR for this fix now!

### Would you like to implement a fix?

Yes

### Tip

<sub>[React](https://github.blog/news-insights/product-news/add-reactions-to-pull-requests-issues-and-comments/) with 👍 to help prioritize this issue. Please use comments to provide useful context, avoiding `+1` or `me too`, to help us triage it. Learn more [here](https://opentelemetry.io/community/end-user/issue-participation/).</sub>
