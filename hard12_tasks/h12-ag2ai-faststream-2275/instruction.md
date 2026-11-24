You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Feature:Support MultiProcess Collector for PrometheusMiddleWare

I encountered a problem that if `MultiProcessCollector` from `prometheus_client` is used, then the metrics are simply not collected. Only `#TYPE` and `#HELP` appear. I learned from one of the contributers - Roman Frolov - of `FastStream` that this functionality is missing, he asked me to create a `Issue` to add this functionality. 

It would be cool if you add a flag for Middleware `multiprocess=True` or something like that.

```python
from typing import Final
from faststream import FastStream
from faststream.kafka import KafkaBroker
from app.settings import Settings, get_settings()

settings: Final[Settings] = get_settings()
registry: Final[CollectorRegistry] = CollectorRegistry()
multiprocess.MultiProcessCollector(registry, path=settings.project_dir / settings.server.multiprocess_dir)

broker: KafkaBroker = KafkaBroker(
            settings.broker.url,
            middlewares=[
                KafkaPrometheusMiddleware(
                    registry=registry,
                    app_name="faststream-some-service",
                    multiprocess=True
                ),
            ]
        )
```

Environment
Running FastStream 0.5.40 with CPython 3.12 on Windows
