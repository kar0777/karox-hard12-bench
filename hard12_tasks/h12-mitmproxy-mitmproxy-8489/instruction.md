You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`cookies._read_set_cookie_pairs` swallows subsequent attributes into `Expires` when `Expires` is short (e.g. `Expires=0; Secure`)

### Problem Description

`mitmproxy.net.http.cookies.parse_set_cookie_header` swallows subsequent attributes (such as `Secure` or `HttpOnly`) into the `Expires` attribute value when `Expires` contains three or fewer characters (such as `Expires=0; Secure`).

#### Reproduction

```python
from mitmproxy.net.http import cookies

# Set-Cookie with Expires=0 followed by Secure
parsed = cookies.parse_set_cookie_header("session=abc; Expires=0; Secure; HttpOnly")

# Actual result:
# [('session', 'abc', CookieAttrs[('Expires', '0, Secure'), ('HttpOnly', None)])]
# 'Secure' is missing from the cookie attributes and merged into 'Expires'.

# Expected result:
# [('session', 'abc', CookieAttrs[('Expires', '0'), ('Secure', None), ('HttpOnly', None)])]
# 'Secure' is parsed as a distinct attribute with value None.
```

#### Root Cause

In `mitmproxy/net/http/cookies.py`, `_read_set_cookie_pairs` parses attributes in Set-Cookie headers using delimiters `;,`. When handling `Expires`, the code attempts to handle commas in HTTP date formats (such as RFC 1123 `Wed, 09 Jun 2021...`):

```python
            if lhs.lower() == "expires":
                if len(rhs) <= 3:
                    trail, off = _read_value(s, off + 1, ";,")
                    rhs = rhs + "," + trail
```

1. The check `if len(rhs) <= 3:` does not verify whether the delimiter that terminated `rhs` was actually a comma. If the attribute terminates at a semicolon (`;`) with `len(rhs) <= 3` (e.g., `Expires=0; Secure`), `_read_value` is called with `off + 1`, skipping past the semicolon and consuming the next attribute (`Secure`) into `rhs`.
2. For comma-separated multiple cookies in a single header (e.g., `a=b; expires=0, c=d`), the second cookie `c=d` is consumed into `Expires`.
3. For RFC 850 dates with full weekday names (e.g., `Wednesday, 21-Oct-2026 07:28:00 GMT; path=/`), `len("Wednesday") > 3`, which fails `len(rhs) <= 3` and incorrectly splits the date across the comma into a phantom second cookie.

#### Affected Ranges (Scope)

- Affected inputs: Any `Set-Cookie` header where `Expires` has a short value (`Expires=0`, `Expires=-1`, etc.) followed by other attributes or subsequent cookies, as well as `Set-Cookie` headers using RFC 850 date strings with full weekday names.
- Scope: Narrow to `mitmproxy.net.http.cookies._read_set_cookie_pairs`.
- Severity: Moderate logic / parsing defect; causes silent loss of security attributes (`Secure`, `HttpOnly`) when inspecting or modifying session cookies that use `Expires=0` idioms.

#### Finding Method

Found during code audit of cookie parsing against RFC 6265 and RFC 850 specifications.

#### System Information

```
Mitmproxy: 13.0.0.dev
Commit: 7735597
Python: 3.14.6
Platform: macOS-27.0.1-arm64-arm-64bit-Mach-O
```

#### Checklist

- [x] This bug affects the latest mitmproxy release.

