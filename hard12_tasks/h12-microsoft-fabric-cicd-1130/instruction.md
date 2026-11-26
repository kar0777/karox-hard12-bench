You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Binding of a Semantic Model connection fails because of missing "/" in the OneLake path

### Library Version

1.3.0

### Python Version

3.14.3

### Operating System

Linux

### Authentication Method

Azure CLI (az login)

### What is the problem?

There is a problem when rebinding a semantic model using "semantic_model_binding:" in parameter.yml

In the workspace with the Semantic Model that we want to rebind, we have the following snippet in the parameter.yml file:
```
semantic_model_binding:
  models:
    - semantic_model_name: "sm_sandbox_platinum_prod_lh"
      connection_id:
        TEST: "b70bd193-bcb2-4823-b3c2-fa687a756aaa"
        PROD: "6312e53f-f205-4523-a641-f5080c06daaa"
```

When we run the Azure DevOps pipeline we see the following error message in the deploy step.

```
[error]  15:52:57 - Failed to bind 'sm_sandbox_platinum_prod_lh' to connection '6312e53f-f205-4523-a641-f5080c06daaa': Unhandled error occurred calling POST on 'https://api.fabric.microsoft.com/v1/workspaces/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/semanticModels/772e5a33-6fe0-41f7-9863-9a82daee4aaa/bindConnection'.
 Message: We cannot bind the semantic model to the specified data connection because the semantic model does not use the data source specified in the connection details (Type: AzureDataLakeStorage, Path:

https://onelake.dfs.fabric.microsoft.com/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/4386df3a-f0a3-485a-8b7e-86010800baaa). Please update the connection details to reference a valid data source, then try again. Learn more:

https://go.microsoft.com/fwlink/?linkid=2329807..
```

We analyzed the problem by issuing the API calls from the terminal and found that a missing `/` at the end of the lakehouse path produces this error message.
Here are the API calls from the terminal. The first call with missing `/` at the end of the lakehouse path:

```
$ curl -X POST   "https://api.fabric.microsoft.com/v1/workspaces/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/semanticModels/772e5a33-6fe0-41f7-9863-9a82daee4aaa/bindConnection"   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -d '{
    "connectionBinding": {
      "id": "6312e53f-f205-4523-a641-f5080c06daaa",
      "connectivityType": "ShareableCloud",
      "connectionDetails": {
        "type": "AzureDataLakeStorage",
        "path": "https://onelake.dfs.fabric.microsoft.com/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/4386df3a-f0a3-485a-8b7e-86010800baaa"
      }
    }
  }'
{"requestId":"c6ce818e-8368-4640-beaf-3d0f433c9607","errorCode":"BindConnectionDetailNotFound","message":"We cannot bind the semantic model to the specified data connection because the semantic model does not use the data source specified in the connection details (Type: AzureDataLakeStorage, Path: https://onelake.dfs.fabric.microsoft.com/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/4386df3a-f0a3-485a-8b7e-86010800baaa). Please update the connection details to reference a valid data source, then try again. Learn more: [https://go.microsoft.com/fwlink/?linkid=2329807.","isRetriable":false}](https://go.microsoft.com/fwlink/?linkid=2329807.%22,%22isRetriable%22:false%7D)
```

Successful binding API call with `/` at the end of the lakehouse path:

```
$ curl -X POST   "https://api.fabric.microsoft.com/v1/workspaces/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/semanticModels/772e5a33-6fe0-41f7-9863-9a82daee4aaa/bindConnection"   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -d '{
    "connectionBinding": {
      "id": "6312e53f-f205-4523-a641-f5080c06daaa",
      "connectivityType": "ShareableCloud",
      "connectionDetails": {
        "type": "AzureDataLakeStorage",
        "path": "https://onelake.dfs.fabric.microsoft.com/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/4386df3a-f0a3-485a-8b7e-86010800baaa/"
      }
    }
  }'
```

We further analyzed the problem and found that the API call that returns Fabric Connections returns path strings without `/` at the end. The `connectionDetails` of the response are used for the binding call above.

```
$ curl -X GET \
  "https://api.fabric.microsoft.com/v1/connections/6312e53f-f205-4523-a641-f5080c06daaa" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
{"allowConnectionUsageInGateway":false,"allowUsageInUserControlledCode":false,"id":"6312e53f-f205-4523-a641-f5080c06daaa","displayName":"conn_sandbox_platinum_prod","gatewayId":"6450ecfa-3b56-4b78-a4a3-64257fc7d0cc","connectivityType":"ShareableCloud","connectionDetails":{"path":"https://onelake.dfs.fabric.microsoft.com/2adfc75d-b4f3-4d0c-8278-6f66e28c4aaa/4386df3a-f0a3-485a-8b7e-86010800baaa","type":"AzureDataLakeStorage"},"privacyLevel":"Organizational","credentialDetails":{"credentialType":"WorkspaceIdentity","singleSignOnType":"None","connectionEncryption":"NotEncrypted","skipTestConnection":false},"connectionRecency":{"createdDateTime":"2026-09-08T10:28:44Z","lastBoundDateTime":"2026-09-14T15:55:06Z","lastCredentialUsedDateTime":"2026-09-14T15:56:00Z","myLastBoundDateTime":"2026-09-14T15:55:06Z","myLastCredentialUsedDateTime":"2026-09-14T15:56:00Z"},"myRole":"User"}
```

Suggested bugfix: Add a `/` chat when the connection type is `"AzureDataLakeStorage"` in the `build_request_body` method in the `\_semanticmodel.py` file.

```
connection_type = connection_details.get("type") if "type" in connection_details else None
    path = connection_details.get("path") if "path" in connection_details else None

    # The Fabric Connections API returns AzureDataLakeStorage paths without a trailing
    # slash, but bindConnection rejects them without one, so append it here.
    if connection_type == "AzureDataLakeStorage" and path and not path.endswith("/"):
        path = f"{path}/"

    return {
        "connectionBinding": {
            "id": connection_binding.get("id"),
            "connectivityType": connection_binding.get("connectivityType"),
            "connectionDetails": {
                "type": connection_type,
                "path": path,
            },
        }
    }
```


### Steps to reproduce

1. Create a Fabric workspace (with git connection and workspace identity enabled)
2. Create a Lakehouse in the workspace
3. Create a Semantic Model in the workspace
4. Commit the changes
5. Create a connection that uses the workspace identity to authenticate
6. Check out the git repository in VS Code
7. In the workspace folder create a parameter.yml file that defines a `semantic_model_binding`
8. commit your change
9. use a deployment pipeline to deploy the workspace

### Expected behavior

The Semantic Model binding is replaces as defined in parameter.yml `semantic_model_binding^

### Actual behavior

Error message:
```
[error]  15:52:57 - Failed to bind 'sm_sandbox_platinum_prod_lh' to connection '6312e53f-f205-4523-a641-f5080c06d5f5': Unhandled error occurred calling POST on 'https://api.fabric.microsoft.com/v1/workspaces/2adfc75d-b4f3-4d0c-8278-6f66e28c405f/semanticModels/772e5a33-6fe0-41f7-9863-9a82daee460a/bindConnection'.
 Message: We cannot bind the semantic model to the specified data connection because the semantic model does not use the data source specified in the connection details (Type: AzureDataLakeStorage, Path:

https://onelake.dfs.fabric.microsoft.com/2adfc75d-b4f3-4d0c-8278-6f66e28c405f/4386df3a-f0a3-485a-8b7e-86010800b910). Please update the connection details to reference a valid data source, then try again. Learn more:

https://go.microsoft.com/fwlink/?linkid=2329807..
```

### Is there an ideal solution?

See bug description.

### Additional context, screenshots, logs, error output, etc

_No response_
