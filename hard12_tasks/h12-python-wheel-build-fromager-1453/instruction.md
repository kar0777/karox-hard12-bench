You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: SBOM shows the resolved version, not the wheel version, when the wheel has a local version

**Related:** #1370, #1371

## Why this is a bug

Fromager can build a wheel that has a local version, for example `0.5.5+local.1`.
A patch can add the local version.
The SBOM in the wheel does not show this version. The SBOM shows the resolved version `0.5.5`.

PR #1371 makes the document name and namespace use the `purl.version` value.
If `purl.version` is not set, the SBOM still uses the resolved version in all fields.

- The SBOM must identify the wheel that contains it. At this time, the SBOM identifies the upstream release.
- The wheel file name and the `METADATA` file show `0.5.5+local.1`. The SBOM shows `0.5.5`. The data in one wheel does not agree.
- Scanners use the SBOM version and purl to find vulnerabilities. A scanner can think that the wheel is the upstream release.
  Then the scanner can show vulnerabilities that a patch fixed. The scanner can also miss the local changes.
- You can set `purl.version` for each package to get the correct version.
  If you forget this setting, fromager does not show an error or a warning. The SBOM is incorrect, and nobody knows.

## Steps to reproduce

1. Install fromager from the `main` branch, at commit `45241aad` or a later commit.
   Fromager 0.101.0 also shows the problem.
2. Make the file `overrides/settings.yaml` with this content:

   ```yaml
   sbom:
     supplier: "Organization: ExampleCo"
     namespace: "https://sbom.example"
   ```

3. Make the directory `overrides/patches/sqlparse-0.5.5/`.
4. Put this patch in the directory. Use the name `0001-local-version.patch`.
   The patch changes the package version to `0.5.5+local.1`.

   ```diff
   --- a/sqlparse/__init__.py
   +++ b/sqlparse/__init__.py
   @@ -18,7 +18,7 @@
    from sqlparse import formatter


   -__version__ = "0.5.5"
   +__version__ = "0.5.5+local.1"
    __all__ = ["engine", "filters", "formatter", "sql", "tokens", "cli"]


   ```

5. Do not make a package settings file for `sqlparse`. Do not set `purl.version`.
6. Build the wheel:

   ```bash
   fromager bootstrap sqlparse==0.5.5
   ```

7. Find the wheel in `wheels-repo/downloads/`. Make sure that the file name contains `0.5.5+local.1`.
8. Show the SBOM values:

   ```bash
   WHL=$(ls wheels-repo/downloads/sqlparse-*.whl)
   unzip -p "$WHL" '*.dist-info/sboms/fromager.spdx.json' \
     | jq '.name, .packages[0].versionInfo, .packages[0].externalRefs[0].referenceLocator'
   ```

9. Compare the values with the correct values.

   Actual values:

   ```text
   "sqlparse-0.5.5"
   "0.5.5"
   "pkg:pypi/sqlparse@0.5.5"
   ```

   Correct values:

   ```text
   "sqlparse-0.5.5+local.1"
   "0.5.5+local.1"
   "pkg:pypi/sqlparse@0.5.5%2Blocal.1"
   ```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

