You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SitemapSpider includes trailing robots.txt comment in sitemap request URL

### Description

`SitemapSpider` includes trailing `robots.txt` comments in the extracted sitemap URL. For a line like `Sitemap: http://host/sitemap.xml # generated sitemap`, the space before `#` is encoded as `%20` in the request path. The server receives `/sitemap.xml%20` and can return 404, so the spider never discovers the pages in the sitemap.

[Robots Exclusion Protocol syntax](https://www.rfc-editor.org/rfc/rfc9309#section-2.2) allows trailing comments in `robots.txt` lines; sitemap records are a commonly supported extension. The issue occurs in `sitemap_urls_from_robots`: the value is stripped but the comment is not removed.

### Steps to Reproduce

Save this script as `repro.py` and run `python repro.py plain`, then `python repro.py comment`. It starts a local HTTP server and runs an actual `SitemapSpider` against it; no external site is contacted.

```python
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import SitemapSpider

seen = []
comment = ' # generated sitemap' if sys.argv[1] == 'comment' else ''

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        seen.append(self.path)
        base = f'http://127.0.0.1:{self.server.server_port}'
        if self.path == '/robots.txt':
            data = f'Sitemap: {base}/sitemap.xml{comment}\n'.encode()
            content_type = 'text/plain'
        elif self.path == '/sitemap.xml':
            data = (
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                f'<url><loc>{base}/page</loc></url></urlset>'
            ).encode()
            content_type = 'application/xml'
        elif self.path == '/page':
            data, content_type = b'ok', 'text/plain'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
os.environ['no_proxy'] = '127.0.0.1'

class Demo(SitemapSpider):
    name = 'demo'
    sitemap_urls = [f'http://127.0.0.1:{server.server_port}/robots.txt']

    def parse(self, response):
        yield {'url': response.url}

process = CrawlerProcess(settings={'LOG_ENABLED': False, 'ROBOTSTXT_OBEY': False})
process.crawl(Demo)
process.start()
server.shutdown()
server.server_close()
print(sys.argv[1], seen)
```

Actual:

```text
$ python repro.py plain
plain ['/robots.txt', '/sitemap.xml', '/page']
$ python repro.py comment
comment ['/robots.txt', '/sitemap.xml%20']
```

**Expected behavior:** The trailing comment should not change the URL; both runs should request `/sitemap.xml` and `/page`. Encoded URL data such as `%23` should remain intact.

**Reproduces how often:** Every run in this local test.

### Versions

```text
Scrapy       : 2.19.0
lxml         : 6.1.3
libxml2      : 2.14.6
cssselect    : 1.6.0
parsel       : 1.12.1
w3lib        : 2.5.0
Twisted      : 26.4.0
Python       : 3.11.0
pyOpenSSL    : 26.4.0
cryptography : 50.0.2
Platform     : macOS-15.0-arm64-arm-64bit
```

Also reproduced from current `master` commit `5c7886a3f27dbf8b66f557cc9945dbc4a6aceaac`. Existing issues and PRs were searched for sitemap and robots comments. Codex assisted with investigation and drafting; both test runs were executed locally.

