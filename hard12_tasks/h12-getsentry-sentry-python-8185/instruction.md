You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Continued traces propagate sample_rate=1.0 instead of upstream

### How do you use Sentry?

Sentry Saas (sentry.io)

### Version

2.73.0 (behavior present since 2.22.0)

### Steps to Reproduce

1. Init the SDK with only `traces_sample_rate` set (e.g. `0.5`, no `traces_sampler`).
2. Continue an incoming trace that was sampled upstream at 1%:
   ```python
   headers = {
       "sentry-trace": "771a43a4192642f0b136d5159a501700-1234567890abcdef-1",
       "baggage": "sentry-trace_id=771a43a4192642f0b136d5159a501700,sentry-sample_rate=0.01,sentry-sample_rand=0.005,sentry-sampled=true,sentry-public_key=abc",
   }
   transaction = sentry_sdk.continue_trace(headers, name="t", op="http.server")
   with sentry_sdk.start_transaction(transaction):
       print(sentry_sdk.get_baggage())
   ```
3. Inspect the outgoing baggage and the envelope `trace` header of the sent transaction.

Same result with `trace_lifecycle="stream"`.

### Expected Result

The incoming DSC is frozen, so `sample_rate=0.01` is propagated as is, in both the envelope `trace` header and outgoing baggage. The [DSC spec](https://develop.sentry.dev/sdk/foundations/trace-propagation/dynamic-sampling-context/) says the receiving SDK MUST consider the incoming DSC frozen and propagate its values "as is". Other SDKs propagate the incoming sample rate in this scenario.

### Actual Result

Both the envelope `trace` header and outgoing baggage carry `sample_rate=1.0`:

```
sentry-trace_id=771a43a4192642f0b136d5159a501700,sentry-sample_rate=1.0,sentry-sample_rand=0.005,sentry-sampled=true,sentry-public_key=abc
```

When inheriting the parent decision, the SDK sets the transaction's sample rate to `float(parent_sampled)`, i.e. `1.0`, and then writes it over `sample_rate` in the frozen incoming DSC (`Scope.start_transaction`, and `Scope._update_sample_rate` for span streaming). This was introduced in #4018 (released in 2.22.0), which changed `test_dsc_continuation_of_trace` to expect `1.0` instead of the incoming rate.

**Why this matters:** Relay derives `client_sample_rate` from the DSC `sample_rate`, and Sentry uses it to extrapolate counts in the product. Data from any Python service that continues a trace gets weighted as if it were sampled at 100%. In the example above, extrapolated counts for that service end up 100x too low. Because the overwritten baggage is also propagated, every downstream service inherits `1.0` as well.

<!-- junior-request-attribution:start -->
via @mjq.
<!-- junior-request-attribution:end -->

<!-- junior-session-footer:start -->
<!-- junior-conversation-id:slack%3AC0BSRCZ1F9T%3A1793740283.124799 -->

--

[View Session](https://junior-prod.sentry.dev/conversations/slack%3AC0BSRCZ1F9T%3A1793740283.124799) [[Sentry]](https://sentry.sentry.io/explore/conversations/slack%3AC0BSRCZ1F9T%3A1793740283.124799/?project=4510944073809921)

<!-- junior-session-footer:end -->
