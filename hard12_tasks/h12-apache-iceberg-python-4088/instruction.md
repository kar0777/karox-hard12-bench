You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

View does not expose metadata_location: RestCatalog.load_view discards it from the server's response

### Apache Iceberg version

0.12.0 (latest release)

### Please describe the bug 🐞

`RestCatalog.load_view` (and `create_view`) parse the server's `metadata-location` but drop it when building the `View`, so callers cannot learn where a view's current metadata file is. Tables keep it as `Table.metadata_location`; views have no equivalent. The behaviour is unchanged on `main`.

**The spec** (`open-api/rest-catalog-open-api.yaml`) requires the field in every view load result:

```yaml
LoadViewResult:
  required:
    - metadata-location
    - metadata
```

with the description: "The corresponding file location of view metadata is returned in the `metadata-location` field. Clients can check whether metadata has changed by comparing metadata locations after the view has been created."

**pyiceberg parses it, then discards it** (`pyiceberg/catalog/rest/__init__.py` on `main`):

```python
class ViewResponse(IcebergBaseModel):
    metadata_location: str | None = Field(alias="metadata-location", default=None)
    metadata: ViewMetadata
    config: Properties = Field(default_factory=dict)

def _response_to_view(self, identifier_tuple, view_response: ViewResponse) -> View:
    return View(
        identifier=identifier_tuple,
        metadata=view_response.metadata,
        config=view_response.config,
    )   # view_response.metadata_location is never passed on
```

`_response_to_table`, by contrast, passes `metadata_location=table_response.metadata_location` to `Table`.

**Why it matters:** without it, a client cannot detect changes to a view the way the spec suggests (comparing metadata locations), record where a view's metadata lives, or re-register a view from that file later with `register_view`.

**Expected:** `View` exposes `metadata_location`, set from the REST response, like `Table.metadata_location`.

PR #3390 ("REST: Add metadata_location to View, and register_view integration test") addressed this but was closed unmerged. Related umbrella issue: #818.


### Willingness to contribute

- [ ] I can contribute a fix for this bug independently
- [ ] I would be willing to contribute a fix for this bug with guidance from the Iceberg community
- [x] I cannot contribute a fix for this bug at this time
