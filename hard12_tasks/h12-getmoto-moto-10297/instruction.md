You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

DynamoDB: Incorrect item size calculation for Number attributes

*(Posted by Claude Code)*

## Description

Moto's DynamoDB `DynamoType.size()` method computes the size of a Number attribute as `len(str(value))` — the length of the decimal string representation. Real DynamoDB uses a more compact encoding where the size is approximately `ceil(significant_digits / 2) + 1` bytes, as [documented by AWS](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/CapacityUnitCalculations.html).

For example, a Unix timestamp like `1786461547` (10 digits):
- Moto computes: `len("1786461547")` = **10 bytes**
- Real DynamoDB uses: `ceil(10 / 2) + 1` = **6 bytes**

This means moto's 400 KB item size check is more restrictive than real DynamoDB's. Items that DynamoDB accepts can be rejected by moto with `ValidationException: Item size has exceeded the maximum allowed size`.

## Steps to reproduce

```python
import boto3
from moto import mock_aws

@mock_aws
def test():
    client = boto3.client("dynamodb", region_name="us-east-1")
    client.create_table(
        TableName="test",
        KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # This is accepted by real DynamoDB but rejected by moto
    client.put_item(
        TableName="test",
        Item={
            "pk": {"S": "x" * 40},
            "data": {"B": b"x" * 409530},
            "ttl": {"N": "1786461547"},
        },
    )

test()
```

## Root cause

In `moto/dynamodb/models/dynamo_type.py`, `DynamoType.size()`:

```python
def size(self) -> int:
    if self.is_number():
        value_size = len(str(self.value))  # <-- should be ceil(digits / 2) + 1
```

## Expected behavior

Number attribute size should be computed as `ceil(significant_digits / 2) + 1` to match DynamoDB's actual encoding, per the AWS documentation on [item size calculations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/CapacityUnitCalculations.html).
