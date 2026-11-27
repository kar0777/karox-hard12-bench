You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

CERT_EXPIRY too long

### Problem Description

Per #8142 CERT_EXPIRY has been reduced to 199 days. But as notBefore is backdated by 2 days, total cert length is 201 days which is still not accepted as max length is 200 days per 
https://chromium.googlesource.com/chromium/src/+/961e21793515436af0f02a7fe4889c79249909cf/net/cert/cert_verify_proc.cc#827

Example :
openssl s_client -proxy X.X.X.X:Y -connect www.google.com:443 -servername www.google.com </dev/null 2>/dev/null | openssl x509 -noout -dates -issuer -subject

notBefore=Apr 28 17:11:26 2026 GMT
notAfter=Nov 15 17:11:26 2026 GMT
issuer=CN = mitmproxy, O = mitmproxy
subject=CN = www.google.com

Length = 201 days

You should fix and set CERT_EXPIRY to 180 days to let some margin.

### System Information

```raw

```

### Checklist

- [x] This bug affects the [latest mitmproxy release](https://github.com/mitmproxy/mitmproxy/releases).
