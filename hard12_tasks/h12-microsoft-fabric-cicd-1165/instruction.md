You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] False circular DataPipeline dependencies from GUID-valued non-reference fields

### Library Version

1.4.0 (upstream source)

### Python Version

3.13.5 (isolated test harness)

### Operating System

Linux

### Authentication Method

Other

### What is the problem?

The DataPipeline dependency detector can incorrectly identify circular dependencies when a pipeline definition contains a GUID belonging to another pipeline (or itself) in a field that is not an actual pipeline reference.

`find_referenced_datapipelines()` recursively scans all string values in `pipeline-content.json`. Any complete GUID matching a known DataPipeline logical ID is treated as a dependency, regardless of the field containing it.

For example, a pipeline parameter's `defaultValue` can be mistaken for a pipeline invocation. This creates false dependency edges and can cause an otherwise valid deployment to fail with a circular-dependency error.

The problem is in `src/fabric_cicd/_items/_datapipeline.py`.

### Steps to reproduce

1. Create a DataPipeline named `A` with logical ID `11111111-1111-4111-8111-111111111111`.
2. Give it the following `pipeline-content.json`:

```json
{
  "properties": {
    "activities": [],
    "parameters": {
      "auditPipelineId": {
        "type": "String",
        "defaultValue": "11111111-1111-4111-8111-111111111111"
      }
    }
  }
}
```

3. Run `find_referenced_datapipelines(workspace, content, "Repository")` with a workspace mapping that resolves this logical ID to pipeline `A`.
4. The function incorrectly returns `["A"]`, despite the absence of any pipeline invocation activity.
5. Pass this result through `sort_items()` to determine the publish order.

The resulting graph contains an artificial self-dependency and the topological sort raises a circular-dependency error.

This was reproduced in an isolated source-level test harness. Full upstream CI and live Fabric integration testing remain pending.

### Expected behavior

Only genuine pipeline invocation references should influence dependency ordering, including references inside nested activities.

GUIDs in parameters, request bodies, or unrelated metadata should not create dependency edges.

Real pipeline dependencies, genuine circular references, and reverse unpublish ordering should continue to behave as before.

### Actual behavior

The detector treats any GUID-valued string that resolves to a known pipeline as a dependency.

In the reproduction, it creates a self-reference and raises:

`ParsingError: There is a cycle in the graph. Cannot determine a valid publish order.`

The pipeline itself has no circular invocation dependency.

### Is there an ideal solution?

Restrict dependency detection to actual pipeline invocation fields, including:

- `ExecutePipeline`: `typeProperties.pipeline.referenceName`
- `InvokePipeline`: `typeProperties.pipelineId`

Preserve nested activity traversal and genuine circular-dependency detection.

Add regression tests for unrelated GUID-valued fields, real parent-child dependencies, nested activities, and publish/unpublish ordering.

### Additional context, screenshots, logs, error output, etc

I independently identified the issue by inspecting the current source and prepared a focused candidate fix with 11 isolated regression tests.

Results:
- Original implementation: 7 passed, 4 failed
- Proposed implementation: 11 passed
- Python 3.9 syntax compatibility: passed

The tests exercise the upstream dependency functions with mocked Fabric collaborators; the offline harness substitutes a recursive walker for `dpath`. Full upstream CI and live Fabric workspace testing have not been performed.

Source:
https://github.com/microsoft/fabric-cicd/blob/main/src/fabric_cicd/_items/_datapipeline.py

This differs from #978, which concerns missing dependencies in disabled activities.

I have a patch and regression tests prepared and would be happy to contribute a PR if the maintainers agree with the approach.
