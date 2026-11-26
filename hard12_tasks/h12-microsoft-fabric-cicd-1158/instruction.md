You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] key_value_replace still corrupts notebook .py files that parse as a YAML mapping (follow-up to #890)

### Library Version

1.2.0 (also reproduced on 1.4.0)

### Python Version

3.14.8

### Operating System

Linux

### Authentication Method

Service principal (secret)

### What is the problem?

#890 / #889 fixed `key_value_replace` corrupting notebook `.py` files by making `check_valid_yaml_content()` return True only when the content parses as a mapping or sequence. That covers notebooks whose uncommented code parses as a plain scalar, but not ones whose uncommented code happens to parse as a mapping.

Every notebook structural line (`# Fabric notebook source`, `# META`, `# CELL`, `# MAGIC`) is a YAML comment. If the remaining Python is something like:

```python
for p in ["a", "b"]:
    spark.conf.set(p, globals()[p])
```

YAML reads it as `{'for p in ["a", "b"]': 'spark.conf.set(p, globals()[p])'}`, a mapping. The file passes `check_valid_yaml_content()`, and `replace_key_value()` then returns `yaml.dump(data)` even though the `find_key` matched nothing. All comment lines are dropped, including the prologue and cell markers, and Fabric rejects the result.

We hit this with a notebook whose parameters cell was commented out and whose other cells were all `%%sql` (`# MAGIC` lines), so a single `for` loop was the only uncommented code. A `key_value_replace` entry filtered by `item_type: Notebook` (meant for `.schedules`) was enough to trigger it. Git Sync of the same commit works.

### Steps to reproduce

1. Add a `key_value_replace` entry to `parameter.yml` that applies to Notebook items without a `file_path` filter, for example:
   ```yaml
   key_value_replace:
     - find_key: $.schedules[*].enabled
       replace_value:
         dev: false
       item_type: Notebook
   ```
2. Add a notebook whose only uncommented code parses as a YAML mapping, for example the `for` loop above, with all other cells being `%%sql` or markdown.
3. Deploy.

Minimal repro without deploying (fabric-cicd 1.4.0):

```python
from fabric_cicd._common._check_utils import check_valid_yaml_content
from fabric_cicd._parameter._utils import replace_key_value

notebook = """# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# CELL ********************

for p in ["a", "b"]:
    spark.conf.set(p, globals()[p])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
"""

class Ws:
    environment = "dev"

print("check_valid_yaml_content:", check_valid_yaml_content(notebook))
param = {"find_key": "$.schedules[*].enabled", "replace_value": {"dev": False}}
print(replace_key_value(Ws(), param, notebook, "dev", is_yaml=True))
```

Output:

```
check_valid_yaml_content: True
for p in ["a", "b"]: spark.conf.set(p, globals()[p])
```

### Expected behavior

The notebook is published unchanged, since it is not a YAML file and the `find_key` does not match anything in it.

### Actual behavior

The notebook content is replaced with a YAML dump of its uncommented code, and publishing fails:

```
Failed to publish Notebook '<name>': Operation failed. Error Code: NB_CLR_NotebookServiceApiException. Error Message: "Convert data from py to ipynb failed. Detail: PyToIPynb: the py format is not correct - The py content is not supported - prologue is invalid. Expected prologue: # Fabric notebook source\r" (Crud) (HTTP 400) Operation: Import
```

### Is there an ideal solution?

Either of these would fix it, and together they would also cover other non-YAML files that happen to parse as YAML:

1. In `replace_key_value()`, return the original `content` unchanged when `jsonpath_expr.find(data)` finds no matches, instead of always re-serializing. Re-dumping also drops comments and reformats real YAML files that had no matches.
2. Decide JSON/YAML handling by file extension (`.json`, `.yml`, `.yaml`, `.schedules`, `.platform`, etc.) rather than by whether the content happens to parse, so `.py`, `.kql`, `.sql` and similar files are never treated as YAML.

### Additional context, screenshots, logs, error output, etc

- Previous report and fix: #890, #889. The test added in #889 uses `print("hello world")` as the only code, which parses as a scalar, so the mapping case isn't covered.
- Workaround: make sure the notebook has uncommented code that doesn't parse as a YAML mapping. Scoping the `key_value_replace` entry with a `file_path` filter so it never touches `.py` files should also avoid it.

