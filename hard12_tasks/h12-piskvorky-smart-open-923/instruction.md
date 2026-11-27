You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[http/azure/s3] Avoid unnecessary GET when seeking within current buffer

Hello,

As for me `smart_open` http module can improve buffering, please look on code sample:

```python
import smart_open
import pandas as pd
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1

fp = smart_open.open("https://github.com/airbytehq/airbyte/files/9280856/test.xlsx", mode="rb")
df = pd.read_excel(fp)
print(df)
```

```bash
$ ./test.py | grep airbytehq/airbyte/files/9280856/test.xlsx
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=0-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=8685-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=8665-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=8045-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=0-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=8685-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=8665-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=8045-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=0-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=6478-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=1724-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=6694-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=3832-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=2536-\r\n\r\n'
send: b'GET /airbytehq/airbyte/files/9280856/test.xlsx HTTP/1.1\r\nHost: github.com\r\nUser-Agent: python-requests/2.28.1\r\nAccept-Encoding: identity\r\nAccept: */*\r\nConnection: keep-alive\r\nrange: bytes=3099-\r\n\r\n'
```

`pandas.read_excel` read file in random access way, it does a lot of `seek` and `read` calls.
I suspected if on first HTTP request we read all file contents, subsequent `read` calls will be from some internal buffer,
but I still see that library under the hood continue to make HTTP requests inside small bytes range which already was read on 1-st HTTP request.

Can we improve it? Can we skip additional HTTP request if we already have all needed data from 1-st HTTP request?

#### Versions

```
print(platform.platform())
Linux-5.14.0-1047-oem-x86_64-with-glibc2.31
print("Python", sys.version)
Python 3.9.11 (main, Aug  9 2022, 09:22:28) 
[GCC 9.4.0]
print("smart_open", smart_open.__version__)
smart_open 6.0.0
```

#### Checklist

Before you create the issue, please make sure you have:

- [x] Described the problem clearly
- [x] Provided a minimal reproducible example, including any required data
- [x] Provided the version numbers of the relevant software

