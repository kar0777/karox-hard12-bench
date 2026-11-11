You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: SBOM upstream entry uses the purl.name, purl.type, and purl.namespace values when purl.upstream is not set

**Related:** #1031, #1376, #1377

## Why this is a bug

If `purl.upstream` is not set, fromager derives the upstream entry (`SPDXRef-upstream`) from the
downstream purl settings. Three per-package settings that change the wheel entry (`SPDXRef-wheel`)
also change the upstream entry:

- `purl.name`
- `purl.type`
- `purl.namespace`

#1376 reported the same problem for `purl.version`, and #1377 fixes it. The other three fields still
have the problem.

- The upstream entry identifies the source that fromager used. Upstream, the project is
  `pkg:pypi/sqlparse`. Upstream has no `pkg:pypi/sqlparse-corp`, `pkg:generic/sqlparse`, or
  `pkg:pypi/acme/sqlparse` (the `pypi` purl type does not use a namespace).
- The `GENERATED_FROM` relationship points from the wheel to the upstream entry, so it points to a
  source that does not exist.
- If `sbom.repository_url` is not set, the two entries have the same purl. Then the SBOM does not
  show a difference between the wheel and its source.
- The `purl.upstream` setting prevents this problem, but fromager does not tell users that the
  setting is required when they override these fields.

## Original intent

This behavior was intentional. The design in #1031 says that `_build_upstream_purl` uses "the same
cascade" of overrides as `_build_downstream_purl`, but without the `repository_url` qualifier. The
`PurlConfig.upstream` docstring also says: "When absent, the upstream purl is auto-derived from the
downstream purl without the `repository_url` qualifier."

The design assumed that the purl overrides describe the package everywhere. In practice, they
describe the downstream build. #1376 showed this for `version`: a local version such as
`0.5.5+local.1` exists only downstream. The same logic applies to a renamed package, a different
purl type, or a namespace that is added for a downstream index.

## Steps to reproduce

1. Install fromager from the `main` branch.
2. Make the file `overrides/settings.yaml` with this content:

   ```yaml
   sbom:
     supplier: "Organization: ExampleCo"
     namespace: "https://sbom.example"
   ```

3. Make the file `overrides/settings/sqlparse.yaml`. Use one of these settings:

   ```yaml
   purl:
     name: "sqlparse-corp"
   ```

   ```yaml
   purl:
     type: "generic"
   ```

   ```yaml
   purl:
     namespace: "acme"
   ```

4. Do not set `purl.upstream` or `sbom.repository_url`.
5. Build the wheel:

   ```bash
   fromager bootstrap sqlparse==0.5.5
   ```

6. Show the purls of the wheel entry and the upstream entry:

   ```bash
   WHL=$(ls wheels-repo/downloads/sqlparse-*.whl)
   unzip -p "$WHL" '*.dist-info/sboms/fromager.spdx.json' \
     | jq '.packages[].externalRefs[0].referenceLocator'
   ```

7. Compare the values with the correct values.

   | Setting | Wheel purl | Actual upstream purl | Correct upstream purl |
   |---|---|---|---|
   | `name: sqlparse-corp` | `pkg:pypi/sqlparse-corp@0.5.5` | `pkg:pypi/sqlparse-corp@0.5.5` | `pkg:pypi/sqlparse@0.5.5` |
   | `type: generic` | `pkg:generic/sqlparse@0.5.5` | `pkg:generic/sqlparse@0.5.5` | `pkg:pypi/sqlparse@0.5.5` |
   | `namespace: acme` | `pkg:pypi/acme/sqlparse@0.5.5` | `pkg:pypi/acme/sqlparse@0.5.5` | `pkg:pypi/sqlparse@0.5.5` |

The global `sbom.purl_type` setting has the same effect. If it is set to a value other than `pypi`,
the upstream entry of every package gets that type.

## Proposed solution

If `purl.upstream` is not set, the upstream entry is always
`pkg:pypi/<package name>@<resolved version>`.

- Do not use the per-package `name`, `type`, `namespace`, or `version` values for the upstream entry.
- Do not use the global `sbom.purl_type` value for the upstream entry.
- The per-package `purl` fields describe only the wheel. `purl.upstream` is the only setting that
  changes the upstream entry.

This agrees with the fix for #1376. Packages that come from GitHub, GitLab, or a different upstream
name set `purl.upstream`, as they do now. For these packages, a change to the type only is not
sufficient, because the name, namespace, and version are usually different too (for example
`pkg:github/vllm-project/bart-plugin@v0.2.0`).

This change modifies the SBOM for users who set `type`, `namespace`, or `sbom.purl_type` to describe
a non-PyPI source and do not set `purl.upstream`. Update the `PurlConfig` docstrings, mention the
change in the release notes, and tell these users to set `purl.upstream`.

## Discussion point: do we need `type` overrides for the wheel?

Fromager builds Python wheels. The purl specification uses the `pypi` type for Python packages, and
uses the `repository_url` qualifier for packages that come from an index other than PyPI. Fromager
already supports `repository_url` globally and for each package.

The only use case for the `type` override that I found is the `pkg:generic/my-fork@1.0.0` example
in #1032. That example identifies a fork, and `purl.upstream` now covers it.

Bundled components with other purl types do not need this setting. For example, #1327 imports
`pkg:cargo/...` components from the SBOM that Maturin generates. These components keep their own
purls and do not use `PurlConfig`.

Is there a valid use case for a wheel purl type other than `pypi`? If not, we can deprecate
`PurlConfig.type` and `sbom.purl_type`. Removing them would break existing configuration files, so
this issue does not propose the removal.

