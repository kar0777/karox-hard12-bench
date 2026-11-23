You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`SpanProcessor.on_end` exceptions escape cleanup and replace application exceptions

### Steps to Reproduce

```python
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider

class RaisingProcessor(SpanProcessor):
    def on_end(self, span):
        raise RuntimeError("processor failed")

provider = TracerProvider()
provider.add_span_processor(RaisingProcessor())
tracer = provider.get_tracer("reproduction")

with tracer.start_as_current_span("operation"):
    raise ValueError("application failed")
```

### Expected Result

[OnEnd(Span)](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan):

> This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception.

[Error handling](https://opentelemetry.io/docs/specs/otel/error-handling/):

> OpenTelemetry implementations MUST NOT throw unhandled exceptions at runtime.

> API methods that accept external callbacks MUST handle all errors.

[`SynchronousMultiSpanProcessor.on_end`](https://github.com/open-telemetry/opentelemetry-python/blob/53a5a40c9604583c501bcf13970a635f00e62df4/opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py#L187-L189) invokes processors without an exception guard. The exception escapes through [`Span.end`](https://github.com/open-telemetry/opentelemetry-python/blob/53a5a40c9604583c501bcf13970a635f00e62df4/opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py#L986-L1001) during context-manager cleanup.

### Actual Result

The caller receives `RuntimeError("processor failed")`, with the application’s `ValueError` in `__context__`. Replacing the application’s `raise` with `pass` also propagates `RuntimeError`.

### Would you like to implement a fix?

```diff
--- a/opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py
+++ b/opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py
@@ -187,3 +187,6 @@
     def on_end(self, span: "ReadableSpan") -> None:
         for sp in self._span_processors:
-            sp.on_end(span)
+            try:
+                sp.on_end(span)
+            except Exception:
+                logger.exception("Exception while calling SpanProcessor.on_end.")
```

### Tip

<sub>[React](https://github.blog/news-insights/product-news/add-reactions-to-pull-requests-issues-and-comments/) with 👍 to help prioritize this issue. Please use comments to provide useful context, avoiding `+1` or `me too`, to help us triage it. Learn more [here](https://opentelemetry.io/community/end-user/issue-participation/).</sub>
