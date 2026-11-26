You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[sdk] Failed kube config load discards the cause and swallows KeyboardInterrupt

### Environment

* KFP version: master (reproduced against `2.15.2`)
* KFP SDK version: `kfp==2.15.2`
* All dependencies version:

```
kfp                      2.15.2
kfp-pipeline-spec        2.17.0
kfp-server-api           2.17.0
kubernetes               30.1.0
```

### Steps to reproduce

When `kfp.Client()` is constructed without a `host` and outside a cluster, it falls back to
loading the local kube config. That fallback is wrapped in a bare `except:` that discards the
cause and reports every failure with the same fixed string
([`client.py#L313-L318`](https://github.com/kubeflow/pipelines/blob/master/sdk/python/kfp/client/client.py#L313-L318)):

```python
try:
    k8s.config.load_kube_config(
        client_configuration=config, context=kube_context)
except:
    print('Failed to load kube config.')
    return config
```

Any of the following produce byte-identical output:

```python
import kfp

# 1. no kubeconfig on the machine
# 2. kubeconfig present but malformed
# 3. kubeconfig fine, but the requested context does not exist
kfp.Client(kube_context='does-not-exist')
```

```
Failed to load kube config.
```

The underlying `kubernetes.config.ConfigException` carries the actionable detail in each case
(`Invalid kube-config file. No configuration found.`, `Context does-not-exist not found in
kube-config file`, and so on), but it is discarded.

Because the method then returns the partially populated `Configuration` rather than raising,
the first symptom the user actually sees is a later connection error against the default host,
detached from the real cause.

There are two further consequences of the same block:

1. A bare `except:` catches `BaseException`, so `KeyboardInterrupt` and `SystemExit` are
   swallowed during config resolution.
2. The message is written to stdout with `print`, so it cannot be suppressed, captured, or
   leveled by callers that configure `logging`. It is the only `print` in `client.py` used for
   an error; the other four are deliberate user-facing links.

The in-cluster probe immediately above (`client.py#L303-L306`) uses a bare `except:` as well.

### Expected result

The failure should identify its cause, and should be routed through `logging` so callers can
control it — consistent with `_get_config_with_default_credentials` in the same class, which
already handles the analogous case this way:

```python
except Exception:
    logging.warning('Failed to set up default credentials. Proceeding'
                    ' without credentials...')
```

Concretely:

* `except:` → `except Exception:`, so `KeyboardInterrupt` propagates.
* `print(...)` → `logging.warning(...)`, including the underlying exception.
* The in-cluster probe should log at debug level rather than warn, since running outside a
  cluster is the expected case on that path and a warning there would be a false alarm.

Loading the kube config should remain best effort — it should keep returning the configuration
rather than raising, so existing callers that recover downstream are unaffected.

### Materials and Reference

* `sdk/python/kfp/client/client.py`, `Client._load_config`
* Existing precedent in the same class: `Client._get_config_with_default_credentials`

---

Impacted by this bug? Give it a 👍.

