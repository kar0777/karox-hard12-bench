# HARD12 task `h12-beeware-briefcase-2890`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/2890 |
| issue | #2888 (created 2026-06-18) |
| PR created / merged | 2026-06-19 / 2026-06-19 |
| base | `bef0b2251e346a2485905fab55bb118d4fa200c0` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 14 / 71 |
| test files | tests/platforms/macOS/app/package/test_notarize.py, tests/platforms/macOS/app/package/test_package.py, tests/platforms/macOS/app/package/test_package_dmg.py, tests/platforms/macOS/app/package/test_package_pkg.py, tests/platforms/macOS/app/package/test_package_zip.py, tests/platforms/macOS/app/package/test_resume_notarization.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
