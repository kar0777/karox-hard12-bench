You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

s3control pagination returns no error code for an invalid NextToken

## Reporting a bug

Passing a NextToken that moto cannot decode to any of the three paginated s3control calls produces a response with no usable error code. Client code that wants to catch an expired or malformed token has nothing to match on.

```python
import boto3, botocore
from moto import mock_aws

@mock_aws
def run():
    client = boto3.client("s3control", region_name="us-east-1")
    try:
        client.list_access_points(AccountId="111111111111", NextToken="invalid")
    except botocore.exceptions.ClientError as e:
        err = e.response["Error"]
        print(e.response["ResponseMetadata"]["HTTPStatusCode"], err["Code"], err["Message"])

run()
```

Prints:

```
400 400 Bad Request
```

The code is the literal string `400` and the message is `Bad Request`. Same for `list_multi_region_access_points` and `list_storage_lens_configurations`.

The s3control service model defines `InvalidNextTokenException`, and that is what real AWS returns here. moto's paginator already supports this: `PAGINATION_MODEL` entries take a `fail_on_invalid_token` key naming the exception to raise, which route53resolver and s3tables both set. The three s3control entries in `moto/s3control/models.py` leave it at the default, so the paginator falls back to the generic `InvalidToken`, which s3control has no handler for.

Valid tokens are unaffected, pagination itself works.

moto 5.1.29.dev, on master at f940cfd.
