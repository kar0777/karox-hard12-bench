You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

IPV6 Host malformation in TLS connect request when in upstream mode

### Problem Description

I was attempting to chain mitmproxy with burp and a mobile application in this order. 
mobile app->mitmproxy->burp->internet. 

Without burp in the loop, mitmproxy works perfectly in intercepting all https traffic so this rules out any mobile certificate or ssl pinning issues. When I route it though burp though, I get an error on burp:
Invalid client request received: Failed to parse target host and port from CONNECT request.

Upon setting up a netcat listener for the tls connection on the port burp's listener was on, I got this as the result

CONNECT IPV6_ADDRESS:443 HTTP/1.1
Host: IPV6_ADDRESS:443

(I've redacted the actual Ipv6 addresses)
As per the HTTP/URI spec, the host portion of the ipv6 address should be wrapped in square bracket which is not the case here and its my suspicion as to why burp interprets it as malformed. Considering that it is only an issue when dealing with --mode upstream and not regular connections, I'd recommend checking from there.

### System Information

```raw
Mitmproxy: 12.2.3
Python:    3.14.5
OpenSSL:   OpenSSL 3.6.2 7 Apr 2026
Platform:  Linux-6.18.32-2-lts-x86_64-with-glibc2.43
```

### Checklist

- [x] This bug affects the [latest mitmproxy release](https://github.com/mitmproxy/mitmproxy/releases).
