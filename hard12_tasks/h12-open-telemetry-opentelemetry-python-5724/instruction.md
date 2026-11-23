You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Logs Enabled: implement Development-status conditions (minimum_severity, trace_based)

## What

Implement the remaining, Development-status conditions of the Logs `Enabled` spec in the SDK: severity-based filtering (`minimum_severity`) and trace-based filtering (`trace_based`).

## Background

PR #5380 adds `Logger.enabled()` and implements the **stable** conditions of the spec's [`Enabled` section](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/sdk.md#enabled):

- there are no registered `LogRecordProcessors`
- `LoggerConfig.enabled` is `false` (handled in `Logger.enabled()`)
- all registered `LogRecordProcessors` implement `Enabled` and each returns `false`

The spec lists two further conditions under which `Enabled` MUST return `false`, both currently marked **[Development]**:

- the provided severity is specified (not `0`) and is less than the configured `minimum_severity`
- `trace_based` is `true` and the current context is associated with an unsampled trace

These were intentionally deferred out of #5380 (see https://github.com/open-telemetry/opentelemetry-python/pull/5380#discussion_r3715247579 and the issue discussion at https://github.com/open-telemetry/opentelemetry-python/issues/5360#issuecomment-5183215458).

## Why deferred

- Both conditions are still **Development** status in the spec and subject to change.
- `_LoggerConfig` currently only has `is_enabled`; these conditions require adding `minimum_severity` and `trace_based` fields to the config model first. The tracer analog `_TracerConfig` also only has `is_enabled`, so the config model should grow consistently across signals (related: #5524).

## Proposed scope

- Add `minimum_severity` and `trace_based` fields to `_LoggerConfig`.
- Have `Logger.enabled()` return `false` when the provided severity is below `minimum_severity`, and when `trace_based` is set and the current context is an unsampled trace.
- Track the spec closely, since these conditions are Development status.

cc @aabmass @herin049

