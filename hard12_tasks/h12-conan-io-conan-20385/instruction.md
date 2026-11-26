You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[feature] Pass original URL as a header when downloading sources from backup URLs

### What is your suggestion?

When conan downloads sources from the backup URL, I would like the original URL to be passed as a header. Maybe something like `X-Resource-Original-Url: https://example.com/libfoo.tar.gz`.

This can be done with a one line change right here: https://sourcegraph.com/github.com/conan-io/conan/-/blob/conans/client/downloaders/caching_file_downloader.py?L114-118

```
headers = {'X-Resource-Original-Url': urls}
self._file_downloader.download(backup_url + sha256, cached_path, sha256=sha256, headers=headers)
```

My use case is that my company prevents access to the public internet by default except for specifically permitted services. If we pass this header, then all downloads can go through a service that acts as a proxy.

I've created a service that acts as a source caching proxy. When a request is made to myservice.com/<somesha>, first I check if that sha has already been downloaded, and if it has return that file immediately. If it hasn't been downloaded yet, then it reads the headers for the original URL, downloads the file, verifies it with the passed in sha, and then returns it to the client. It's an extremely simple service and this proxy means that normal users don't need to access the rest of the internet.

### Have you read the CONTRIBUTING guide?

- [x] I've read the CONTRIBUTING guide
