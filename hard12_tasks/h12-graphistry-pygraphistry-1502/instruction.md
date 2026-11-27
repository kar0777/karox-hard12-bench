You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL/Cypher IC4 direct-Cypher returns wrong aggregation results after CASE blocker fix

## Summary

Direct-Cypher execution of the official LDBC SNB Interactive IC4 (`new-topics`,
`interactive-complex-4`) query now lowers and runs end-to-end, but returns a
**semantically wrong result**. This is a new residual that surfaced after the
return-side `CASE` lowering blocker was fixed.

Measured on `pygraphistry` `origin/master`
`0efa2d0a1754e9b71ff17a7ea09ff9d7427fa6fc` (`Fix scalar projection alias match
planning (#1482)`).

## Detail

- The IC4 lowering blockers are **closed**: #1038 (return-side `CASE`
  expression) and #981 (multi-binding projection). The official IC4 Cypher no
  longer fails at lowering — it lowers and executes (~781 ms).
- The **GFQL** path for IC4 is correct (`ok`, matches the reference fixture).
- The **direct-Cypher** path now executes but fails `result_mismatch`: it
  returns the wrong set of tags.

At SF0.1, IC4 direct-Cypher returns 9 rows, 6 correct:

```
ACTUAL   : George_Harrison, Highway_61_Revisited, Islamabad/Rawalpindi,Lahore,
           Joan_Crawford, Salvador, Scream_Childhood, Stevie_Wonder, Taraz,
           Ulysses_S._Grant
EXPECTED : George_Frideric_Handel, George_Harrison, Highway_61_Revisited,
           Jean-Paul_Sartre, Joan_Crawford, Michelangelo, Scream_Childhood,
           Stevie_Wonder, Ulysses_S._Grant
```

3 tags wrongly included (`Islamabad/Rawalpindi,Lahore`, `Salvador`, `Taraz`),
3 wrongly dropped (`George_Frideric_Handel`, `Jean-Paul_Sartre`,
`Michelangelo`).

## Suspected shape

The official IC4 query ends with two `CASE`-based `WITH` stages, an aggregating
`WITH`, and a post-aggregation `WHERE`:

```cypher
WITH tag,
     CASE WHEN $startDate <= post.creationDate < $endDate THEN 1 ELSE 0 END AS valid,
     CASE WHEN post.creationDate < $startDate            THEN 1 ELSE 0 END AS inValid
WITH tag, sum(valid) AS postCount, sum(inValid) AS inValidPostCount
WHERE postCount>0 AND inValidPostCount=0
RETURN tag.name AS tagName, postCount
ORDER BY postCount DESC, tagName ASC
LIMIT 10
```

The wrong tag set is consistent with the post-aggregation
`WHERE postCount>0 AND inValidPostCount=0` filter (a `HAVING`-style filter over
aggregated columns) and/or the `inValid` `CASE` branch being mis-evaluated, so
tags with pre-`$startDate` posts are not excluded correctly.

## Evidence

- Benchmark tracker (evidence source): graphistry/pyg-bench#4
- Benchmark metadata reconciliation: graphistry/pyg-bench#29 (merged as
  `ef006f4`) — updates the pyg-bench runner classifier, translation YAML, and
  docs to record this lane as a result-correctness residual rather than the
  resolved `CASE` lowering blocker.

## Done when

- Direct-Cypher IC4 (`new-topics`) reports `ok` in pyg-bench conformance
  (result matches the reference fixture), allowing graphistry/pyg-bench#4 to
  close.

