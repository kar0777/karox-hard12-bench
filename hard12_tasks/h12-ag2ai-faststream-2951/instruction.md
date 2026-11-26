You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: batch per-message keys desync from `batch_bodies` when a publish middleware reorders/filters the batch

# Batch per-message keys desync from `batch_bodies` when it is reordered/filtered

## Summary

`KafkaPublishCommand` captures per-message keys **positionally** at construction (`self._per_message_keys`), and the producer later re-reads them **by index** while enumerating the *current* `cmd.batch_bodies` (`key = cmd.key_for(message_position)`, `faststream/kafka/publisher/producer.py:138-150`).

`BatchPublishCommand.batch_bodies` has a public setter, and a publish middleware runs against the command *after* construction and *before* the producer loop. If anything reorders or filters `cmd.batch_bodies` in between, keys no longer line up with bodies and messages are published with the **wrong key** (wrong partition / broken per-key ordering). No error is raised.

## Environment

- faststream `0.7.0rc1`, Python `3.13.12`

## Root cause

The command freezes keys by position at construction:

```python
# faststream/kafka/response.py
keys, normalized = extract_per_message_keys_and_bodies(self.batch_bodies)
if normalized is not None:
    self.batch_bodies = normalized
self._per_message_keys = keys        # <-- frozen at construction, indexed by position
```

The producer re-reads them by index over the *current* bodies:

```python
# faststream/kafka/publisher/producer.py
for message_position, body in enumerate(cmd.batch_bodies):   # <-- current bodies
    ...
    key=cmd.key_for(message_position),                       # <-- old index -> old key
```

`BatchPublishCommand.batch_bodies` has a public setter, and publish middleware runs between those two points, so reassigning `cmd.batch_bodies` desyncs `_per_message_keys`.

## Reproduction (command-level, deterministic)

Mirrors the producer loop exactly.

```python
from faststream.kafka import KafkaPublishMessage
from faststream.kafka.response import KafkaPublishCommand
from faststream.response.publish_type import PublishType

cmd = KafkaPublishCommand(
    KafkaPublishMessage("body-A", key=b"key-A"),
    KafkaPublishMessage("body-B", key=b"key-B"),
    topic="topic",
    _publish_type=PublishType.PUBLISH,
)

def delivered(cmd):  # exactly what the producer does
    return [(body, cmd.key_for(i)) for i, body in enumerate(cmd.batch_bodies)]

print("before:", delivered(cmd))

cmd.batch_bodies = tuple(reversed(cmd.batch_bodies))  # e.g. a publish middleware

print("after :", delivered(cmd))
```

Output:

```python
before: [('body-A', b'key-A'), ('body-B', b'key-B')]
after : [('body-B', b'key-A'), ('body-A', b'key-B')]
```

`body-B` is published with `key-A` and `body-A` with `key-B`. Filtering is worse: dropping the first body shifts every remaining key by one.

## Affected code

- `faststream/kafka/response.py:100-104,129-130` — `_per_message_keys` captured by index; `key_for(index)`.
- `faststream/kafka/publisher/producer.py:138-150` and `faststream/kafka/testing.py:205` — index-based read over current `batch_bodies`.
- `faststream/response/response.py` — shared `extract_per_message_keys_and_bodies` / `key_for_index` and the `batch_bodies` setter.
- `faststream/confluent/response.py:100-104` — same pattern.

## Expected

Per-message keys stay attached to their body across any mutation of `batch_bodies`.

## Suggested fix

Store bodies and keys together (one sequence of `(body, key)` pairs as the source of truth) so reordering/filtering one reorders/filters the other atomically; alternatively, make the `batch_bodies` setter rebuild `_per_message_keys`. The same fix should cover Confluent.

