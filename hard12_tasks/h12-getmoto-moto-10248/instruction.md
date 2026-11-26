You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Kafka: list_clusters and list_clusters_v2 ignore ClusterNameFilter and ClusterTypeFilter

`list_clusters` and `list_clusters_v2` both take the filter arguments and never read them, so every call comes back with every cluster in the account.

```python
import boto3
from moto import mock_aws

@mock_aws
def repro():
    client = boto3.client("kafka", region_name="eu-west-1")
    for name in ("analytics-batch", "billing"):
        client.create_cluster_v2(
            ClusterName=name,
            Provisioned={
                "BrokerNodeGroupInfo": {
                    "InstanceType": "kafka.m5.large",
                    "ClientSubnets": ["subnet-0123456789abcdef0"],
                    "SecurityGroups": ["sg-0123456789abcdef0"],
                },
                "KafkaVersion": "2.8.1",
                "NumberOfBrokerNodes": 3,
            },
        )
    got = client.list_clusters(ClusterNameFilter="analytics")
    print([c["ClusterName"] for c in got["ClusterInfoList"]])
    # ['analytics-batch', 'billing'], expected ['analytics-batch']

repro()
```

`ClusterTypeFilter` on `list_clusters_v2` goes the same way. Ask for `SERVERLESS` and the provisioned clusters come back with it.

In `moto/kafka/models.py` the parameters arrive and are not used:

```python
def list_clusters(
    self,
    cluster_name_filter: str | None,
    max_results: int | None,
    next_token: str | None,
) -> tuple[list[dict[str, Any]], str | None]:
    cluster_info_list = [ ... for cluster_arn, cluster in self.clusters.items() ]
    return cluster_info_list, None
```

Nothing marks this as unimplemented, so the call looks like it worked. Code under test that lists one cluster by name gets the whole account back and carries on as if that were the answer.

AWS matches `ClusterNameFilter` on the start of the name, and treats a `ClusterTypeFilter` of `ALL` as no filter at all.

I have a patch and tests ready.
