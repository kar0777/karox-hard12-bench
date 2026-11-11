You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

update_webhook / hf webhooks update fail with 400 unless watched and domains are passed again

### Describe the bug

`HfApi.update_webhook()` says `watched` and `domains` are optional, and `hf webhooks update` says "Only provided options are changed". But updating just one field always fails with a 400.

The reason: `update_webhook` always sends `"watched": []` when `watched` is not passed, and leaves out `domains` when it is not passed. The Hub endpoint (`POST /api/settings/webhooks/{id}`) needs both, with at least one watched item. So the documented CLI example `hf webhooks update abc123 --url https://new-url.com/hook` can't work, and same for `--secret newsecret` alone. You have to pass the full watched list and domains again every time.

Tested on 2.4.0 and the code is the same on `main`.

Expected: fields that are not passed keep their current value (for example by reading the webhook first and filling in the missing `watched` / `domains`), or at least the docs say both are required.

I'm happy to send a PR for this if the fix direction sounds ok.

### Reproduction

Run against the CI hub with the test token from `tests/testing_constants.py`:

```python
from huggingface_hub import HfApi

api = HfApi(endpoint="https://hub-ci.huggingface.co", token="hf_HubCITokenXXXXXXXXXXXXXXXXXXXXX")
me = api.whoami()["name"]
w = api.create_webhook(url="https://webhook.site/test", watched=[{"type": "user", "name": me}], domains=["repo"])
try:
    api.update_webhook(w.id, url="https://webhook.site/new")  # 400
finally:
    api.delete_webhook(w.id)
```

Results for different calls:

| call | result |
|---|---|
| `update_webhook(id, url=...)` | 400: `watched` too small, `domains` undefined |
| `update_webhook(id, url=..., domains=["repo"])` | 400: `watched` too small |
| `update_webhook(id, secret="s2", watched=[...])` | 400: `domains` undefined |

### Logs

```shell
huggingface_hub.errors.BadRequestError: (Request ID: Root=1-6ae7af3b-301d4ebe24bef79a32f1e74d;c86a502f-0124-447b-a57e-54766439dd0d)

Bad request:
* Too small: expected array to have >=1 items * at watched * Invalid input: expected array, received undefined * at domains
```

### System info

```shell
- huggingface_hub version: 2.4.0
- Platform: Linux-6.12.94+-x86_64-with-glibc2.41
- Python version: 3.13.5
```

