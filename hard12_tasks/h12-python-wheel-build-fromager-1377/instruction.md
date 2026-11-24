You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: SBOM upstream entry uses the `purl.version` value when `purl.upstream` is not set

**Related:** #1370, #1371

## Why this is a bug

The `purl.version` setting changes the version of the wheel entry (`SPDXRef-wheel`) in the SBOM.
If `purl.upstream` is not set, `purl.version` also changes the version of the upstream entry (`SPDXRef-upstream`).
PR #1371 did not change the upstream entry. The problem continues after PR #1371.

- The upstream entry identifies the source that fromager used. The upstream project released `0.5.5`.
  The upstream project did not release `0.5.5+local.1`.
- The `GENERATED_FROM` relationship points from the wheel to the upstream entry.
  As a result, the relationship points to a version that does not exist upstream.
- Tools that use this relationship cannot find the upstream release.
- If `sbom.repository_url` is not set, the two entries have the same purl.
  Then the SBOM does not show a difference between the wheel and its source.
- The `purl.upstream` setting prevents this problem. But fromager does not tell users that this setting is necessary.
- The tests that PR #1371 added set `purl.upstream`. Because of this, the tests do not find this problem.

## Steps to reproduce

1. Install fromager from the `main` branch, at commit `45241aad` or a later commit.
   Fromager 0.101.0 also shows the problem.
2. Make the file `overrides/settings.yaml` with this content:

   ```yaml
   sbom:
     supplier: "Organization: ExampleCo"
     namespace: "https://sbom.example"
   ```

3. Make the file `overrides/settings/sqlparse.yaml` with this content:

   ```yaml
   purl:
     version: "0.5.5+local.1"
   ```

4. Do not set `purl.upstream`.
5. Build the wheel:

   ```bash
   fromager bootstrap sqlparse==0.5.5
   ```

6. Show the SBOM values of the upstream entry:

   ```bash
   WHL=$(ls wheels-repo/downloads/sqlparse-*.whl)
   unzip -p "$WHL" '*.dist-info/sboms/fromager.spdx.json' \
     | jq '.packages[1] | .versionInfo, .externalRefs[0].referenceLocator'
   ```

7. Compare the values with the correct values.

   Actual values:

   ```text
   "0.5.5+local.1"
   "pkg:pypi/sqlparse@0.5.5%2Blocal.1"
   ```

   Correct values:

   ```text
   "0.5.5"
   "pkg:pypi/sqlparse@0.5.5"
   ```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

