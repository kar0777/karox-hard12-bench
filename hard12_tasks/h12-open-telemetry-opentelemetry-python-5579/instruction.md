You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Samplers never receive the parent's tracestate, and the composite sampler erases it

### Describe your environment

**Labels:** bug, sdk, trace, sampling, spec-compliance
**Affected packages:** `opentelemetry-sdk`
**Found on:** `main` @ `0a5d76b6`
**Environment:** CPython 3.12

### What happened?


Two independent omissions on the same path.

`Tracer.start_span` calls `should_sample(context, trace_id, name, kind, attributes, links)` and never passes the seventh parameter, `trace_state`. Separately, `ParentBased.should_sample` accepts `trace_state` but does not forward it to its delegate. Between them, **no sampler ever receives a tracestate**, even though the `Sampler` ABC declares the parameter and the comment at the call site says the sampler may modify it.

A third, related bug: `_update_trace_state` returns early when the incoming tracestate is empty, so `SamplingIntent.update_trace_state` is silently skipped for every root span.


### Steps to Reproduce


```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace._sampling_experimental import (
    composable_always_on, composable_parent_threshold, composite_sampler,
)
from opentelemetry.trace import set_span_in_context
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

carrier = {
    "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01",
    "tracestate": "vendora=alpha,ot=th:8",
}
remote = TraceContextTextMapPropagator().extract(carrier)

provider = TracerProvider(
    sampler=composite_sampler(composable_parent_threshold(composable_always_on()))
)
span = provider.get_tracer("t").start_span("child", context=remote)

out = {}
TraceContextTextMapPropagator().inject(out, context=set_span_in_context(span))
print("incoming:", carrier["tracestate"])
print("outgoing:", out.get("tracestate"))
```

### Expected Result


The sampler receives the parent's tracestate, and vendor entries survive into the child span's tracestate.


### Actual Result


```
# what the sampler actually receives
bare sampler               trace_state = None
ParentBased(sampler)       trace_state = None

# end-to-end propagation through a composite sampler
incoming tracestate : vendora=alpha,ot=th:8
outgoing tracestate : None
vendora preserved   : False

# control - the default sampler
outgoing tracestate : vendora=alpha,ot=th:8
vendora preserved   : True
```

### Additional context


Two distinct consequences.

First, the W3C consistent probability sampling implementation in `_sampling_experimental` is inert. `_ComposableParentThreshold` reads the parent threshold from tracestate and always sees `None`, so it falls back to the sampled flag with `threshold_reliable=False`. The `rv` random value is never honoured either, so consistent sampling across a trace cannot work and span-to-metrics estimation loses its adjusted counts.

Second, and worse for anyone not using that module: `_CompositeSampler` rebuilds the outgoing tracestate from the parameter it was handed. Given `None`, it emits a fresh tracestate containing only `ot` - silently discarding every vendor entry from the incoming request. Tracestate is how other tracing systems carry their own context through a trace, so this breaks interoperability for third parties that have nothing to do with sampling.

Any custom sampler that relies on the documented `trace_state` parameter is also affected, including one wrapped in `ParentBased` - which is the default composition.


### Would you like to implement a fix?

Yes

### Tip

<sub>[React](https://github.blog/news-insights/product-news/add-reactions-to-pull-requests-issues-and-comments/) with 👍 to help prioritize this issue. Please use comments to provide useful context, avoiding `+1` or `me too`, to help us triage it. Learn more [here](https://opentelemetry.io/community/end-user/issue-participation/).</sub>
