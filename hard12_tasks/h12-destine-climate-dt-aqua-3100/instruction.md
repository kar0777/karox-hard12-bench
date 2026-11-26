You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

z3fdb troubles

### machine

Lumi

### catalog

ci

### version

main

### What happened?

There are a couple of issues with using the z3fdb engine.

1) The backend filters unknown kwargs and considers `config_fdb` unknown. As a result, this code 

````
from aqua import Reader
reader = Reader(catalog='ci', model='IFS', exp='test-fdb', source="fdb", engine="z3fdb", config_fdb="/users/jvonhar/config.yaml")
data = reader.retrieve()
````

leads to 

````
2026-09-18 14:27:06 :: BackendIntakeFDB :: WARNING  -> kwarg config_fdb is not in the intake parameters of the source, removing it
````

2) In the latest z3fdb v 5.23.2.27 ECMWF has changed the API of `SimpleStoreBuilder.add_part()` which now accepts a dictionary and not a string for the request (!!)
So z3fdb breaks in newer environments

See https://sites.ecmwf.int/docs/fdb/5.23.5/z3fdb/api.html#z3fdb-simplestorebuilder

