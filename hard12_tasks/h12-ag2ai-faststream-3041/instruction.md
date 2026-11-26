You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: NATS subscribers declared with `filter_subjects` render an empty AsyncAPI address

**Describe the bug**

A NATS JetStream pull subscriber can be declared without a `subject`, addressing the stream through `filter_subjects` instead. Such a subscriber works at runtime — including Path parameters, since each filter subject is compiled as an address — but its address never reaches the AsyncAPI schema. The channel renders with an empty subject and a degenerate name.

**How to reproduce**

```python
import json

from nats.js.api import ConsumerConfig

from faststream.nats import JStream, NatsBroker, PullSub
from faststream.specification import AsyncAPI

broker = NatsBroker()


@broker.subscriber(
    stream=JStream("st"),
    pull_sub=PullSub(),
    durable="d",
    config=ConsumerConfig(filter_subjects=["logs.{level}"]),
)
async def handle() -> None: ...


schema = json.loads(AsyncAPI(broker, schema_version="3.0.0").to_specification().to_json())
print(json.dumps(schema["channels"], indent=1))
```

**Observed behavior**

```json
{
 ":Handle": {
  "address": ":Handle",
  "servers": [{"$ref": "#/servers/development"}],
  "messages": {"SubscribeMessage": {"$ref": "#/components/messages/:Handle:SubscribeMessage"}},
  "bindings": {"nats": {"subject": "", "bindingVersion": "custom"}}
 }
}
```

**Expected behavior**

The subject(s) the consumer actually filters on should appear in the channel — as the address and in the NATS channel binding — and the channel name should be derived from them rather than collapsing to `:Handle`.

**Root cause**

`NatsSubscriberSpecificationConfig` carries only `subject` and `queue` (`faststream/nats/subscriber/config.py`), so the specification layer has no knowledge of `filter_subjects` at all. `NatsSubscriberSpecification.subject` reads `self.config.subject`, which is empty here.

The usecase layer does know: `filter_addresses` builds one `Address` per filter subject (`faststream/nats/subscriber/usecases/basic.py`) and `subscription_addresses` yields them, which is why the subscriber works. `_resolved_subject_string` already joins them, but is used only for log context.

**Additional context**

This is not specific to address templates — `filter_subjects=["logs.info"]` renders an empty address too. It was found while scoping #2357 (AsyncAPI render for pattern cases), and is deliberately kept out of it: #2357 is about *which* string a template renders as, this is about an address not being rendered at all.

The two do interact, though, and whoever picks this up should read #2357 first. #2357 adds channel `parameters` derived from the address. Different filter subjects can carry different `{param}` sets, which cannot be described by a single channel — so the natural shape here is one channel per filter subject, the same shape `KafkaSubscriberSpecification` already uses for its topics.

