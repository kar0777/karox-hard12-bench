You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: ListTasks breaks the `includeArtifacts=false` spec "MUST omit" requirement

Specification [(3.1.4)](https://a2a-protocol.org/latest/specification/#314-list-tasks)

> When `includeArtifacts` is false (the default), the artifacts field MUST be omitted entirely from each Task object in the response. The field should not be present as an empty array or null value.

Actual behavior:
```python
from google.protobuf.json_format import MessageToDict

from a2a.types import ListTasksResponse, Task, TaskState, TaskStatus

task = Task(
    id="task-1",
    context_id="context-1",
    status=TaskStatus(state=TaskState.TASK_STATE_WORKING),
)
task.ClearField("artifacts")

response = ListTasksResponse(tasks=[task])
data = MessageToDict(
    response,
    preserving_proto_field_name=False,
    always_print_fields_with_no_presence=True,
)

print(data["tasks"][0]["artifacts"]) 
```

Returns `[]`.

### Code of Conduct

- [x] I agree to follow this project's Code of Conduct
