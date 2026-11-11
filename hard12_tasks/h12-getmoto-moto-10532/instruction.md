You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

EC2 DeleteLaunchTemplateVersions is not implemented

`boto3`'s EC2 `delete_launch_template_versions` operation is not implemented on current master (`c6cd1556f18b0969c014608a541e7d0e47f42386`). Creating and describing launch-template versions works, but deleting an individual non-default version raises `NotImplementedError`.

Minimal reproduction with Python 3.12 and `mock_aws`:

```python
import boto3
from moto import mock_aws

with mock_aws():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    template_id = ec2.create_launch_template(
        LaunchTemplateName="delete-version-repro",
        LaunchTemplateData={"ImageId": "ami-00000001"},
    )["LaunchTemplate"]["LaunchTemplateId"]
    ec2.create_launch_template_version(
        LaunchTemplateId=template_id,
        LaunchTemplateData={"ImageId": "ami-00000002"},
    )
    ec2.delete_launch_template_versions(
        LaunchTemplateId=template_id,
        Versions=["2"],
    )
```

Actual result:

```text
NotImplementedError: The delete_launch_template_versions action has not been implemented
```

Expected: version 2 is deleted and reported in `SuccessfullyDeletedLaunchTemplateVersions`; version 1 remains the default. Surviving version numbers must stay unchanged, and a later version creation must not reuse an already allocated number. Attempts to delete the default version should be refused, and mixed requests should return per-version success/error results.

AWS API reference: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteLaunchTemplateVersions.html

