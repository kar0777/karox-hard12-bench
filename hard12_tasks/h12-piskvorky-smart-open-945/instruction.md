You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[s3] Feature request: handle s3 url object versionId specifier

#### Feature description

- What are you trying to achieve?

interoperability w/ url-like file specifiers that have the object version encoded in the path as `?versionId=...`

- What is the expected result?

this would return the correct version: `smart_open('s3://buckety/pathy-like-path.txt?versionId=12345')`

s3fs does this nicely: https://s3fs.readthedocs.io/en/latest/api.html#s3fs.core.S3FileSystem.split_path

- What are you seeing instead?

`smart_open` doesn't know that `?` can not be in an s3 key (https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html), or that versionId is a valid url-parameter, so instead this type of open fails.


#### Checklist

Before you create the issue, please make sure you have:

- [x] Described the problem clearly
- [ ] Provided a minimal reproducible example, including any required data
- [ ] Provided the version numbers of the relevant software

