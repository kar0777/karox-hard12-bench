You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] Out-of-bounds IndexError in extract_description when parsing crafted component YAML

Environment

How do you deploy Kubeflow Pipelines (KFP)?
Not specified (affects all environments where KFP SDK loads component YAML from untrusted sources)

KFP version:
Not specified (vulnerable in versions using ComponentSpec.from_yaml_documents())

KFP SDK version:
Not specified (any version containing structures.py implementation of extract_description)

------------------------------------------------------------

Steps to reproduce

1. Install KFP SDK:
pip install kfp

2. Run the script:

from kfp.components import structures

malicious_yaml = """line0
line1
 Description: some text
              continued text"""

try:
    spec = structures.ComponentSpec.from_yaml_documents(malicious_yaml)
except IndexError as e:
    print("Crash triggered:", e)

3. Or load via:
load_component_from_text()

4. Observe:
IndexError: list index out of range

------------------------------------------------------------

Expected result

- No crash or unhandled exception
- Invalid YAML should fail gracefully with a validation error
- Parser should not crash on malformed input

------------------------------------------------------------

Materials and reference

Issue in extract_description() inside ComponentSpec.from_yaml_documents()

Problems:
- No bounds check for comments[index]
- Loop can increment index beyond list length
- Assumes fixed line position (index_of_heading = 2)

Vulnerable code:

while comments[index][:len(multi_line_description_prefix)] == multi_line_description_prefix:

Fix:

while index < len(comments) and comments[index][:len(multi_line_description_prefix)] == multi_line_description_prefix:

Also recommended:
- Validate index_of_heading before access
- Avoid hardcoded line assumptions in YAML parsing logic

------------------------------------------------------------

Impact

Type: Denial of Service (DoS)
CWE: CWE-125 (Out-of-bounds access / unvalidated index)
Severity: Medium

Impact:
Any system using KFP SDK to parse untrusted YAML may crash, including:
- CI/CD pipelines
- Shared component repositories
- Multi-tenant pipeline services

------------------------------------------------------------

Labels
/area sdk
/area components
/area backend
/area security
