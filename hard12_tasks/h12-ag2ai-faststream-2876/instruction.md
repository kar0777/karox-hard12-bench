You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: `POST /asyncapi/try` is not generated for FastAPI's plug-in

**Describe the bug**
FastAPI plug-in's `KafkaBroker` doesn't seem to generate `POST /try` endpoint. It results in 404 (Not Found) when trying out publishing an event with Kafka-like broker.


**How to reproduce**
```python
from fastapi import Depends, FastAPI
from typing_extensions import Annotated

from faststream.kafka import KafkaBroker, fastapi
from loguru import logger

router = fastapi.KafkaRouter("localhost:19092")

app = FastAPI()


def broker():
    return router.broker


@router.get("/")
async def hello_http(broker: Annotated[KafkaBroker, Depends(broker)]):
    """Works just fine..."""

    await broker.publish("Hello, Kafka!", "test")
    logger.info(ss)
    return "Hello, HTTP!"


@router.publisher("/test")
async def hello_kafka(message: str, broker: Annotated[KafkaBroker, Depends(broker)]):
    """404..."""

    await broker.publish("ss from test!", "test")
    return message

app.include_router(router)
```

0. Deploy Kafka-like broker.
1. Run FastAPI application.
2. Go to `localhost:8000/asyncapi`.
3. Click on "TRY IT OUT" and "Send Message".
4. Get 404: `INFO:     127.0.0.1:41906 - "POST /asyncapi/try HTTP/1.1" 404 Not Found`

**Expected behavior**
`/asyncapi/try` endpoint is correctly generated and executed, event is emitted.


**Observed behavior**
`POST /asyncapi/try` is not generated.


**Environment**
```python
> uv run faststream -v

Running FastStream 0.6.7 with CPython 3.14.3 on Linux
```

