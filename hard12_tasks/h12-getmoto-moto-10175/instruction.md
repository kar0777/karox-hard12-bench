You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[DynamoDB] Query and Scan do not enforce Select semantics

Moto does not fully enforce DynamoDB's `Select` semantics for `Query` and `Scan`. This allows invalid requests to succeed and makes `Scan` with `Select="COUNT"` include `Items`.

This is present in the latest Moto release, `5.2.2`, and on the current `master` branch at 7dc0838503a3da50ac83980dc82c07572bb5212a.

The following code creates a table with a `KEYS_ONLY` GSI and demonstrates both behaviors:

```python
import boto3
from botocore.exceptions import ClientError
from moto import mock_aws


@mock_aws
def reproduce():
    client = boto3.client("dynamodb", region_name="us-east-1")

    client.create_table(
        TableName="select-repro",
        BillingMode="PAY_PER_REQUEST",
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "gsi_pk", "AttributeType": "S"},
        ],
        KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "test_gsi",
                "KeySchema": [{"AttributeName": "gsi_pk", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "KEYS_ONLY"},
            }
        ],
    )

    try:
        client.query(
            TableName="select-repro",
            IndexName="test_gsi",
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression="gsi_pk = :value",
            ExpressionAttributeValues={":value": {"S": "group-1"}},
        )
    except ClientError as exc:
        print(exc.response["Error"]["Code"])
    else:
        print("Query accepted")

    response = client.scan(
        TableName="select-repro",
        Select="COUNT",
    )
    print("Items" in response)


reproduce()
```

**Expected Result**

The query should raise a `ValidationException` because `ALL_ATTRIBUTES` is not supported on a GSI whose projection type is not `ALL`.

The scan response should contain `Count` and `ScannedCount`, but not `Items`.

**Actual**

Moto accepts the query and prints:

```text
Query accepted
```

Moto also includes `Items` in the scan response, so the second value printed is:

```text
True
```
