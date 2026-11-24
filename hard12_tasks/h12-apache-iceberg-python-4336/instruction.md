You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SqlCatalog: accept an existing SQLAlchemy Engine

### Feature Request / Improvement

`SqlCatalog.__init__` always builds its own engine from the `uri` property (`create_engine(uri, echo=..., pool_pre_ping=...)`). Since 0.12.0 it also runs `_init_catalog()` in the constructor, which queries the database to choose between the v0 and v1 catalog schema.

An application that already owns a configured `Engine` can't hand it to the catalog. Today it has to construct the catalog from a URI and then replace `catalog.engine`. With 0.12 the constructor's probe has already run by then, on the engine PyIceberg built.

That engine lacks what the application set on its own: a pool class and size, `connect_args` (an `ssl.SSLContext` for `sslmode=verify-full`, `application_name`, `statement_timeout`), a psycopg2 wait callback, and event listeners. Two failure modes follow:

- If the URI carries no password, because the application keeps secrets out of `catalog.properties`, the probe fails to authenticate. PyIceberg then reads the tables as absent and picks v1, whatever the real schema is.
- If the database requires TLS settings that only exist in code (an SSL context), the probe's connection is refused.

The probe also opens a connection in the constructor. An asyncio application has to remember to build the catalog off its event loop.

### Proposal

Accept an engine, for example `SqlCatalog(name, engine=engine, **properties)`, or a `SqlCatalog.from_engine(name, engine, **properties)` classmethod. When an engine is given, `uri` becomes optional and `_init_catalog()` runs on that engine. The `uri` property can still be set for display.

Example:

```python
engine = create_engine(url, connect_args={"sslcontext": context}, poolclass=QueuePool, pool_size=1)
catalog = SqlCatalog("default", engine=engine, warehouse="s3://bucket/prefix")
```

### Workaround we use

We subclass `SqlCatalog` and override `_init_catalog` with a no-op during `super().__init__`. We then set `self.engine` to our engine and call `SqlCatalog._init_catalog(self)` ourselves. This depends on a private method, which is why we'd like a supported way.

I can open a pull request for this.

