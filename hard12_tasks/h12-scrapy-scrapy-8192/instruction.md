You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Improving headers values decoding (utf-8 vs latin1)

This raises from https://github.com/scrapy/scrapy/issues/2589 where a server returns a non-UTF-8 header value. According to [this RFC](https://tools.ietf.org/html/rfc7230#section-3.2.4):

>    Historically, HTTP has allowed field content with text in the
   ISO-8859-1 charset [ISO-8859-1], supporting other charsets only
   through use of [RFC2047] encoding.  In practice, most HTTP header
   field values use only a subset of the US-ASCII charset [USASCII].
   Newly defined header fields SHOULD limit their field values to
   US-ASCII octets.  A recipient SHOULD treat other octets in field
   content (obs-text) as opaque data.

So the `latin1` encoding may be preferred over `utf-8` which is the Scrapy's default.  At the other hand, `requests` in some places uses `utf-8` with a fallback to `latin1`: https://github.com/kennethreitz/requests/blob/d6f4818c0b40bc6c00433c013b7daaea83b2cd51/requests/models.py#L908

Following @kmike's [suggestion](https://github.com/scrapy/scrapy/pull/2588#issuecomment-282112022), it seems that decoding headers with `utf-8` having `iso-8859-1` as fallback is the best option.
