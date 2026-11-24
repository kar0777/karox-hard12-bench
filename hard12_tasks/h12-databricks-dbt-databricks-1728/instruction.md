You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Redact nested credential values in dbt debug connection details

<!-- port-from-v2:26068c1ea269ea8f0895ac765d921147ab872572 -->

## Describe the bug

`dbt debug` displays credential-like values nested inside `session_properties` without redaction. The top-level token remains hidden, but nested values appear in the connection details before the connection attempt.

The example below uses synthetic values and mocks the connection attempt. It does not require a warehouse or claim that the warehouse accepts these example session properties.

## Steps to reproduce

Save this as `test_debug_redaction.py` in a checkout with the adapter dependencies installed:

```python
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from dbt.adapters.databricks.credentials import DatabricksCredentials
from dbt.task.debug import DebugTask


class DebugRedactionTest(unittest.TestCase):
    def test_nested_credential_is_not_displayed(self):
        credentials = DatabricksCredentials.from_dict({
            "database": "main",
            "schema": "redaction_proof",
            "host": "example.invalid",
            "http_path": "/sql/1.0/warehouses/offline",
            "token": "SYNTHETIC_TOP_LEVEL_TOKEN",
            "session_properties": {"access_token": "SYNTHETIC_NESTED_TOKEN"},
        })
        task = DebugTask.__new__(DebugTask)
        task.profile = SimpleNamespace(credentials=credentials)
        with (
            patch("dbt.task.debug.fire_event") as events,
            patch.object(DebugTask, "attempt_connection", return_value=None),
        ):
            task.test_connection()
        display = "\n".join(call.args[0].msg for call in events.call_args_list)
        self.assertNotIn("SYNTHETIC_TOP_LEVEL_TOKEN", display)
        self.assertNotIn("SYNTHETIC_NESTED_TOKEN", display)
        self.assertEqual(
            credentials.session_properties["access_token"],
            "SYNTHETIC_NESTED_TOKEN",
        )
```

Run:

```sh
python -m unittest test_debug_redaction -v
```

## Expected behavior

Redact credential-like values recursively when displaying connection details, including nested mappings and sequences. Preserve benign settings and do not mutate the credentials used to connect.

## Actual behavior

The assertion fails because the connection display contains:

```text
session_properties: {'access_token': 'SYNTHETIC_NESTED_TOKEN'}
```

The broader unit reproduction has eight cases: six intended assertion failures and two passing controls. The controls verify that the top-level token stays hidden and a nonsecret setting stays visible; the checks also verify that the underlying profile is unchanged.

## Environment

- Python 3.10.20; dbt-core 1.12.5; dbt-adapters 1.24.5; dbt-common 1.38.0; dbt-spark 1.10.3; SQL connector 4.4.0.
- Adapter main source: `5dc7b22103a4fe04d2619bb0fc36db0c938ac2b5`.
- Next-release branch `1.13.latest`: `c1add903c70819b61b512027c33871a7857dadff`. Its complete credentials source is identical. The next check executes that source in the supported main runtime environment; it is not a full next-checkout integration run.

## Related work

Fusion adds recursive debug-display redaction in [26068c1ea269ea8f0895ac765d921147ab872572](https://github.com/dbt-labs/dbt/commit/26068c1ea269ea8f0895ac765d921147ab872572). Fusion does not itself display Databricks session properties; this report applies the same confidentiality requirement to the additional v1 display container.

[#1609](https://github.com/databricks/dbt-databricks/issues/1609), resolved by [#1610](https://github.com/databricks/dbt-databricks/pull/1610), concerns logged SQL credential/encryption clauses, not connection-profile display. Bounded open/closed issue and PR searches on October 14 found no matching report for this surface. No live credentials are needed for the reproduction.

