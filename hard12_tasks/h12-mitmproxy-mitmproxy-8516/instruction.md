You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Block CRL and OCSP when using the `--emudhra` option

#### Problem Description

When `--emudhra` is enabled, the operating system or client software sends out CRL and OCSP requests to check revocation status. Those lookups are unnecessary and counterproductive — they should be blocked.

```
ocsp-a.emsign.com
ocsp-b.emsign.com
ocsp-c.emsign.com
crl.emsign.com
ocsp.comodoca.com
crl.comodoca.com
```

The last two cover the Sectigo cross-signed copy of the same intermediates, which can get picked up during chain building.

