You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: Logger not properly passed to Confluent Kafka Producer and AdminClient

**Describe the bug**

There are two related issues with logger configuration in the Confluent Kafka components:

1. Late Logger Setup in AsyncConfluentProducer

      In faststream/confluent/helpers/client.py at line 46, the Producer object is created before the _setup() method is called for loger_state. This results in the Producer receiving a NoSetLoggerObject instead of the intended logger passed during initialization.

2. Missing Logger in AdminClient
     The AdminClient in AdminService does not accept a logger parameter, even though it should. Currently, only the configuration is passed, leaving the AdminClient without proper logging.

**How to reproduce**
Include source code:

```python
import logging

import uvicorn
from fastapi import FastAPI
from faststream.confluent.fastapi import KafkaRouter

logger = logging.getLogger("faststream")

router = KafkaRouter(
    bootstrap_servers="kafka:9092",
    enable_idempotence=True,
    allow_auto_create_topics=False,
    schema_url="/asyncapi",
    include_in_schema=True,
    logger=logger,
)

app = FastAPI()
app.include_router(router)

uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Expected behavior**

1. The Producer in AsyncConfluentProducer should use the logger passed to KafkaRouter.
2. The AdminClient should inherit the same logger as other components.

**Observed behavior**

1. The Producer uses NoSetLoggerObject instead of the provided logger.
2. The AdminClient lacks logger configuration, leading to potential silent failures or inadequate logging.

**Environment**
Running FastStream 0.6.3 with CPython 3.13.1 on Linux

