You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Feature: `StreamSub(declare=False)` to opt out of Redis Stream creation

**Is your feature request related to a problem? Please describe.**

FastStream creates the Redis Stream for you whenever a subscriber uses a consumer group — `mkstream=True` is hardcoded and there is no way to turn it off:

https://github.com/ag2ai/faststream/blob/2e36197300841f4cf1fc66537655ae2d0bb1bf10/faststream/redis/subscriber/usecases/stream_subscriber.py#L133-L138

That is a fine default, but it means a typo in a stream name silently provisions a new empty stream instead of failing, and a service that is only supposed to *consume* a stream provisioned elsewhere has no way to say so. Every other broker in FastStream already has this opt-out — `RabbitQueue(declare=False)`, `RabbitExchange(declare=False)`, `JStream(declare=False)`, `KvWatch(declare=False)`, `ObjWatch(declare=False)`. Redis is the only one missing it. The same knob is being added to Kafka in #1827.

**Describe the solution you'd like**

A `declare: bool = True` argument on `StreamSub`, passed through as `mkstream=not declare`. Default behaviour does not change.

**Feature code example**

```python
from faststream import FastStream
from faststream.redis import RedisBroker, StreamSub

broker = RedisBroker()
app = FastStream(broker)


# unchanged default — stream is created if missing
@broker.subscriber(stream=StreamSub("orders", group="g", consumer="c"))
async def owned(msg: str) -> None: ...


# provisioned elsewhere — fail fast instead of creating an empty stream
@broker.subscriber(
    stream=StreamSub("external-events", group="g", consumer="c", declare=False)
)
async def consumed(msg: str) -> None: ...
```

**Semantics**

Redis only offers the "check, do not create" form, so `declare=False` fails when the stream is absent — the same as RabbitMQ's `declare=False` (AMQP `passive=True`), and unlike NATS' variant which just skips creation. Verified against `redis:alpine`:

```python
mkstream=False -> ResponseError: The XGROUP subcommand requires the key to exist.
                  Note that for CREATE you may want to use the MKSTREAM option to
                  create an empty stream automatically.
exists after mkstream=False: 0
mkstream=True  -> exists after: 1
```

The existing `except ResponseError` only swallows `"already exists"`, so this error propagates as-is today — which is the wanted behaviour. Wrapping it in a FastStream error with a message pointing at `declare=False` would be a nice touch, not a requirement.

**Implementation notes**

1. Add `declare: bool = True` to `StreamSub.__init__` and to `__slots__` — https://github.com/ag2ai/faststream/blob/2e36197300841f4cf1fc66537655ae2d0bb1bf10/faststream/redis/schemas/stream_sub.py#L44-L69 — plus an `Args:` entry in the class docstring.
2. Pass `mkstream=not stream.declare` at the `xgroup_create` call linked above.
3. `declare` only has an effect on the consumer-group path — that `xgroup_create` runs only when `group` **and** `consumer` are both set. Without a group the subscriber uses `XREAD`, which never creates anything. `StreamSub` already emits `RuntimeWarning` for argument combinations that have no effect (`no_ack` with a group, `polling_interval` with `last_id != ">"`); `declare=False` without a group deserves the same treatment.
4. Tests go in `tests/brokers/redis/` — one real-broker case asserting the stream is not created and the error surfaces, one asserting the default still creates it.

**Out of scope:** publishing. `XADD` always creates the stream and Redis exposes no flag to prevent it, so there is no publisher-side equivalent.

**Additional context**

Prior art to copy the naming and docstring style from: [`RabbitQueue.declare`](https://github.com/ag2ai/faststream/blob/2e36197300841f4cf1fc66537655ae2d0bb1bf10/faststream/rabbit/schemas/queue.py#L108) and [`JStream.declare`](https://github.com/ag2ai/faststream/blob/2e36197300841f4cf1fc66537655ae2d0bb1bf10/faststream/nats/schemas/js_stream.py#L60).

