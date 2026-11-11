You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: Kafka batch nack() rewinds only the first partition, allowing unprocessed messages from other partitions to be committed

**Describe the bug**

With the aiokafka backend, `batch=True`, and `AckPolicy.NACK_ON_ERROR`, a batch can contain messages from multiple partitions.

If the handler raises an exception, `KafkaAckableMessage.nack()` rewinds only the partition of `raw_message[0]`. Messages from the other partitions are not redelivered. A subsequent successful batch calls `consumer.commit()`, which can commit offsets for those unprocessed messages.

This was reproduced against a real Kafka broker with one consumer and three partitions.

**How to reproduce**

Subscriber configuration:

```python
from faststream import AckPolicy, FastStream
from faststream.kafka import KafkaBroker
from faststream.kafka.annotations import KafkaMessage

broker = KafkaBroker("localhost:9092")
app = FastStream(broker)
failed_once = False


@broker.subscriber(
    "batch-nack-repro",
    group_id="batch-nack-repro",
    batch=True,
    max_records=100,
    batch_timeout_ms=100,
    auto_offset_reset="earliest",
    ack_policy=AckPolicy.NACK_ON_ERROR,
)
async def handle(body: list[str], message: KafkaMessage) -> None:
    global failed_once

    records = [
        (record.partition, record.offset)
        for record in message.raw_message
    ]
    print("Received:", records)

    if not failed_once and len({p for p, _ in records}) > 1:
        failed_once = True
        raise RuntimeError("Fail before processing this batch")

    print("Successfully processed:", records)
```

Steps used in the integration test:

1. Create a fresh topic with three partitions and replication factor 1.
2. Start one FastStream batch subscriber with the configuration above.
3. Ensure messages from all three partitions are buffered before the next poll. For deterministic reproduction, the test blocks an initial warmup handler while publishing two messages to each partition and waiting for aiokafka’s background fetcher to buffer all three partitions.
4. Release the warmup handler. The next handler invocation receives a batch spanning all three partitions.
5. Raise an exception before processing that batch.
6. Allow subsequent handler invocations to succeed.
7. Compare successfully processed records with the consumer group’s committed offsets.

The test uses real Kafka connections and does not mock `getmany()`, `seek()`, or `commit()`.

**Expected behavior**

All messages from the failed batch should be eligible for redelivery.

For a batch spanning multiple partitions, `nack()` should rewind each affected partition to its earliest offset in that batch. Offsets for unprocessed messages should not be committed.

**Observed behavior**

The failed batch contained the following `(partition, offset)` pairs:

```text
[(0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)]
```

Only partition 0 was redelivered:

```text
[(0, 1), (0, 2)]
```

After that retry succeeded, the committed offsets were:

```text
{0: 3, 1: 2, 2: 2}
```

These four records were never successfully processed:

```text
[(1, 0), (1, 1), (2, 0), (2, 1)]
```

Their offsets were nevertheless committed, so the consumer group would skip them on restart.

Integration test result:

```text
success: PASSED
retry:   FAILED — offsets committed for unprocessed messages
```

**Screenshots**

Not applicable. The record and offset output above demonstrates the issue.

**Environment**

Output of `faststream -v`:

```text
Running FastStream 0.7.7 with CPython 3.13.0 on Darwin
```

Additional dependency versions:

```text
aiokafka:     0.14.0
pydantic:     2.14.1
fast-depends: 3.0.9
```

Kafka setup:

- Real Kafka broker (apache/kafka:latest) running locally in Docker.
- Topic with three partitions and replication factor 1.
- One consumer subscribed to the topic.

**Additional context**

`BatchSubscriber.get_msg()` merges records returned by `getmany()` across partitions:

```python
return tuple(chain(*messages.values()))
```

However, `KafkaAckableMessage.nack()` selects only the first record and performs a single `seek()`:

```python
raw_message = (
    self.raw_message[0]
    if isinstance(self.raw_message, tuple)
    else self.raw_message
)
```

There is also a documentation discrepancy: the [batch subscriber guide](https://faststream.ag2.ai/latest/kafka/Subscriber/batch_subscriber/) states that a batch comes from a single partition, while both the implementation and this integration test demonstrate batches spanning multiple partitions.
