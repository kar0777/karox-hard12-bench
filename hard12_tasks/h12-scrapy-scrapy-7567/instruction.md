You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Retry logs an error when giving up

# Description

When retry gives up, scrapy is logging an error, which increases `log_count/ERROR` stats.
This key is the standard way to check for errors in scrapy, but a retry giving shouldn't be considered an error.

### Steps to Reproduce

Run the a spider against an invalid URL so it gives up retrying

**Expected behavior:**

As per my understanding, failing to retry a request shouldn't be considered an error.
If the website is down, it is not an issue in our code, but the website.
So, a validation in the project, when the job finishes, checking if any retries gave up and then throw an exception should be the standard solution in a spider (as scrapy doesn't know if it is an error for the application).

It is also dangerous, as if I handle `errback`, it's still logged as an error, even if I'm "handling" errors on the spider side.
So, maybe a better solution would be to log it as a warning and have a setting to raise a `RetryGaveUpException` that could be handled on a spider basis.
And the user can handle it in `errback`, even if no new setting is added.

Finally, my case is that I'm dealing with a broad crawler and it keeps showing errors when retry gives up, even though I don't have the power to control if the website is down or not.
So, in a per website basis, the error can be helpful, but once we don't have explicit control over the websites we're visiting, various things can happen and they may not be errors.

So, a candidate solution, that should be a mix of old/new behavior is, logging a warning or similar and rising an exception.
If the exception is not handled, it will log the error, but gives the user a simple approach to handle it properly.
Also, if you're already handling exceptions, then it'll keep the old behavior (just logging that it gave up).

### Versions

It was introduced recently
* https://github.com/scrapy/scrapy/issues/3171
* "Possible fix": https://github.com/scrapy/scrapy/issues/4216

