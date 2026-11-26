You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GET /health returns 500 for the whole life of an image-gen or video-gen serve

`GET /health` returns **500** for the whole lifetime of an image-gen or video-gen serve, and every probe writes a full traceback to the log.

## Repro

Built `main` at `f3a39da2` (`apps/rapid-mac/scripts/build.sh`) and served an image alias from the bundled sidecar:

```
"Rapid-MLX Desktop.app/Contents/Resources/rapid-mlx/bin/rapid-mlx" serve flux2-klein-4b --port 8077
curl -i http://127.0.0.1:8077/health
```

```
INFO:     127.0.0.1:56756 - "GET /health HTTP/1.1" 500 Internal Server Error
ERROR:rapid_mlx.exception_handlers:Unhandled exception on GET /health:
    'ImageEngine' object has no attribute 'get_stats'
  File "vllm_mlx/routes/health.py", line 80, in health
AttributeError: 'ImageEngine' object has no attribute 'get_stats'
```

A poll loop at 1 Hz produced **36,578 log lines in 10 minutes** — the traceback is re-printed on every probe, so an ordinary monitoring cadence turns the serve log into a traceback firehose and buries anything else in it.

## Cause

`vllm_mlx/routes/health.py:80` calls the engine unconditionally:

```python
engine_stats = cfg.engine.get_stats() if cfg.engine else {}
```

The guard only covers `cfg.engine is None`. `ImageEngine` (`vllm_mlx/runtime/image_lane.py:49`) is duck-typed on `is_image_gen` / `_loaded` and defines no `get_stats`; neither does `VideoEngine` (`vllm_mlx/runtime/video_lane.py:133`). Only `BatchedEngine` has one. So both generative-media lanes fail here.

The next line has the same shape and would fail identically once line 80 is fixed:

```python
"model_type": "mllm" if (cfg.engine and cfg.engine.is_mllm) else "llm",
```

## Blast radius

* `/healthz` is **fine** — that is what `ServerManager.swift` polls, which is why the desktop Images tab still works and why this was invisible until now.
* `/health` is the documented human-readable view. Anything that health-checks the server that way — `curl`, a container `HEALTHCHECK`, a reverse proxy, Prometheus blackbox, a CI wait loop — sees an image serve as permanently broken.
* Found because a verification harness polled `/health` and hung for 10 minutes on a server that was in fact fully up and rendering images.

## Suggested fix

Make the call capability-checked rather than presence-checked, e.g. `getattr(cfg.engine, "get_stats", None)` with an `{}` fallback, and the same for `is_mllm`. A regression test that serves an `image-gen` alias and asserts `GET /health == 200` would pin both lanes; the current tests only exercise the text lane, so the lane that lacks the attribute is exactly the lane nothing checks.

