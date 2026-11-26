You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Gauge read at startup then disapears

### Describe your environment

OS: debian
Python version: 3.11.2
SDK version: 1.31 & 1.24
API version: 1.31 & 1.24


### What happened?

I expect the following code to show both gauge & counter every 1s in the console (or when scrapped by prometheus client) but it does not. counter is always there. gauge is there when launching the script (very first seconds) then disapears.

```

import random
import time

from prometheus_client import start_http_server

from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

# Start Prometheus client
start_http_server(port=8000, addr="0.0.0.0")
# Exporter to export metrics to Prometheus
prefix = "MyAppPrefix"
reader = PrometheusMetricReader(prefix)
reader2 = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=1_000)
# Meter is responsible for creating and recording metrics
set_meter_provider(MeterProvider(metric_readers=[reader, reader2]))
meter = get_meter_provider().get_meter("view-name-change", "0.1.2")

my_counter = meter.create_counter("my.counter")
my_gauge = meter.create_gauge("my.gauge")

while 1:
    my_gauge.set(random.randint(1, 10))
    my_counter.add(random.randint(1, 10))
    time.sleep(61)
```


### Steps to Reproduce

run the script above

### Expected Result

gauge to be exported properly

### Actual Result

gauge is not exported properly

### Additional context

_No response_

### Would you like to implement a fix?

No
