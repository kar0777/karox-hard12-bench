You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`SynchronousMultiSpanProcessor.force_flush` stops when a processor doesn't return `True`

This code in `SynchronousMultiSpanProcessor`:

https://github.com/open-telemetry/opentelemetry-python/blob/347bfaeeba2c31728d606e0ec02703dca2b652d6/opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py#L182-L203

means that if a processor doesn't return something truthy, then remaining processors are skipped. This doesn't really match the docstring, which only mentions skipping in case of exceeding the timeout. To be fair, `SpanProcessor.force_flush` does say `Returns: False if the timeout is exceeded, True otherwise.` But it would be safer to just check the timeout in `SynchronousMultiSpanProcessor`. Why skip the rest otherwise?

This is particularly bad when one of the processors doesn't implement `force_flush`, so it inherits the default implementation which just returns None, which is interpreted as exceeding the timeout. To demonstrate:

```python
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


class MySpanProcessor(SpanProcessor):
    def on_start(self, span, parent_context):
        print(f'Span started: {span.name}')

    # force_flush not implemented


exporter1 = InMemorySpanExporter()
exporter2 = InMemorySpanExporter()
batch_processor_1 = BatchSpanProcessor(exporter1)
batch_processor_2 = BatchSpanProcessor(exporter2)

tracer_provider = TracerProvider()
tracer_provider.add_span_processor(batch_processor_1)
tracer_provider.add_span_processor(MySpanProcessor())  # has default empty force_flush which returns None
tracer_provider.add_span_processor(batch_processor_2)  # this will get skipped because of the previous processor

tracer = tracer_provider.get_tracer('my_tracer')

tracer.start_span('my_span').end()

tracer_provider.force_flush()

assert len(exporter1.get_finished_spans()) == 1
assert len(exporter2.get_finished_spans()) == 0  # skipped!!!
```

If for some reason it's important to skip other processors after one returns False, then I still think that:

1. `SpanProcessor.force_flush` should return True by default
2. `SynchronousMultiSpanProcessor` should distinguish between False and None.
