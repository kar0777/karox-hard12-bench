You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Avro schema is re-converted to an Iceberg schema on every manifest  read during scan planning

### Feature Request / Improvement

  `AvroFileHeader.get_schema()` (`pyiceberg/avro/file.py`) runs the full `avro_to_iceberg` conversion every time an
  Avro file is opened.

  **The inefficiency**

  - Every manifest under a spec embeds an *identical* Avro schema string.
  - So during scan planning, that same conversion is repeated **once per manifest**.
  - The cost grows with the manifest count, even though only a couple of distinct schemas are ever involved.

  **Proposed fix**

  - The conversion depends only on the schema string, so the result can be cached (keyed on that string).

  **Measured impact**

  - `scan().plan_files()` on an unpartitioned 150-manifest table: **~86 ms → ~48 ms (~1.8× faster)**.
  - The saving grows as the number of manifests increases.
  
  I am willing to contribute for this improvement.
