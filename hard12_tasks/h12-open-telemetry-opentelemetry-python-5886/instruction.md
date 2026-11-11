You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Enhancement: Add forward compatible instrument creation APIs

As surfaced in #5444, adding advisory attributes to existing `Meter.create_*` signatures would break third party OTel implementations when callers pass the new arguments. Hence, we must decide on a way to introduce an extendable creation API while preserving existing methods.

Three alternatives to consider are:

1. **Per-instrument methods with options**

   ```python
   meter.create_counter_with_options(
       "http.client.requests",
       options=CounterOptions(attributes_advisory=("http.request.method",)),
   )
   ```

2. **Instrument builders**

   ```python
   meter.counter_builder("http.client.requests").with_attributes_advisory(
       ("http.request.method",)
   ).build()
   ```

3. **Generic creation method with typed specifications**

   ```python
   meter.create_instrument(
       CounterSpec(
           name="http.client.requests",
           attributes_advisory=("http.request.method",),
       )
   )
   ```

4. **Add forward compatible `**kwargs` arguments to existing methods**

    ```python
    def create_counter(self, name: str, unit: str = "", description: str = "", **kwargs) -> Counter: ...
    ```

The chosen interface should accommodate future creation parameters without repeatedly changing SDK method signatures.

A similar extensibility strategy could also apply to the span creation APIs in [#5819](https://github.com/open-telemetry/opentelemetry-python/pull/5819), which introduces separate concrete methods to preserve compatibility with existing `Tracer` implementations.

My personal opinion is that 1 the approach we should take if we want to ensure no potential API breakage. It is nearly identical to the existing API, so users will find it familiar.

While not relevant to instrument creation, option 2 is undesirable because of the overhead introduced by the builder abstraction. My own benchmarking showed that the overhead of builders are ~3x the overhead of a single function call with several arguments. I would personally prefer to align on a design that we can utilize across signals, approach 2 would likely introduce performance issues/bottlenecks for span/log creation.
