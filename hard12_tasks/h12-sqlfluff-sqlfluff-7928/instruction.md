You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

LT02 - DBT - BigQuery - Formatting Final state inconsistent

### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

When formatting an SQL file like this:

```sql
{%- set extraction_list = [
    ('Compound', 'Canonicalized', 'ival'),
    ('IUPAC Name', 'Allowed', 'sval'),
    ('IUPAC Name', 'CAS-like Style', 'sval'),
    ('IUPAC Name', 'Markup', 'sval'),
    ('IUPAC Name', 'Preferred', 'sval'),
    ('IUPAC Name', 'Systematic', 'sval'),
    ('IUPAC Name', 'Traditional', 'sval'),
    ('InChI', 'Standard', 'sval')
] %}

{{ config(cluster_by=['cid']) }}

SELECT
{%- for label, name, field in extraction_list %}
        (
            SELECT
                p.value.{{ field }}
            FROM UNNEST(props) AS p
            WHERE
                p.urn.label = '{{ label }}'
                AND p.urn.name = '{{ name }}'
            LIMIT 1
        )
            AS {{ (label ~ '_' ~ name) | lower | replace(' ', '_') | replace('-','_') }}
        {{- "," if not loop.last }}
{%- endfor %}
FROM {{ ref('pubchem_compound_raw') }}
```

the `{{- "," if not loop.last }}` will be toggled back and forth between 4 indent and 8 indent.



The output that I generated was in an empty directory with no .sqlfluff config file. 

### Expected Behaviour

SQLFluff will format consistently

### Observed Behaviour

run 1
```shell
$ sqlfluff  fix derp.sql --dialect bigquery
==== finding fixable violations ====
== [derp.sql] FAIL                                                                                                                                                                                                                                                                                                                                                                                                                                                           
L:  25 | P:  89 | LT02 | Expected indent of 4 spaces. [layout.indent]
== [derp.sql] FIXED
1 fixable linting violations found
  [2 unfixable linting violations found]
```
run 2
```shell
$ sqlfluff  fix derp.sql --dialect bigquery
==== finding fixable violations ====
== [derp.sql] FAIL                                                                                                                                                                                                                                                                                                                                                                                                                                                           
L:  25 | P:  89 | LT02 | Expected indent of 8 spaces. [layout.indent]
== [derp.sql] FIXED
1 fixable linting violations found
  [2 unfixable linting violations found]
```

### How to reproduce

1. empty directory
2. create derp.sql with contents above provided
3. run sqlfluff with the arguments above provided
4. repeat as many times as desired
5. observe that it swaps between two end states

### Dialect

BigQuery

### Version

$ uv pip freeze | egrep dbt\|sqlfluff
sqlfluff==4.2.1

### Configuration

Empty .sqlfluff and .sqlfluffignore

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

