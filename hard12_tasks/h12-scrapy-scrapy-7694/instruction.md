You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Have scrapy.Item.fields return fields in definition order

The [current implementation](https://github.com/scrapy/scrapy/blob/ed63fa94d698ba09875d45c20253b98e05cca5e5/scrapy/item.py#L43) uses [`dir()`](https://docs.python.org/3/library/functions.html#dir), which sorts alphabetically by default.

It would be nice if the fields were returned in definition order. Maybe we can use `__dict__`, although for fields defined in base classes [it may not be that straightforward](https://stackoverflow.com/a/69268131). Also, I am not sure how we should order inherited fields, specially when overridden; maybe we can copy the behavior of dataclass, attrs or pydantic.
