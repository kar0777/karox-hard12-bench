"""Render one page and keep what a human needs to judge it: screenshots and errors."""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], Path(sys.argv[2])
report = {"url": url, "console_errors": [], "page_errors": [], "failed_requests": [], "shots": []}
ok = False
with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    page = browser.new_page(viewport={"width": 1600, "height": 900})
    page.on("console", lambda m: m.type == "error" and report["console_errors"].append(m.text))
    page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
    page.on("requestfailed", lambda r: report["failed_requests"].append(f"{r.url} {r.failure}"))
    for attempt in range(20):  # the http server starts in the background
        try:
            page.goto(url, wait_until="load", timeout=60_000)
            break
        except Exception as exc:  # noqa: BLE001
            if attempt == 19:
                report["page_errors"].append(f"goto failed: {exc}")
            time.sleep(0.5)
    def shot(name):
        page.screenshot(path=str(out / f"{name}.png"))
        report["shots"].append(f"{name}.png")
    started = time.time()
    for t in (1, 4, 8):
        page.wait_for_timeout(max(0, int((started + t - time.time()) * 1000)))
        shot(f"t{t:02d}s")
    page.mouse.move(800, 450); page.mouse.down(); page.mouse.move(1150, 380, steps=25); page.mouse.up()
    page.wait_for_timeout(1500); shot("orbit")
    page.mouse.move(800, 450)
    for _ in range(6):
        page.mouse.wheel(0, -300); page.wait_for_timeout(120)
    page.wait_for_timeout(1500); shot("zoom")
    report["canvas_count"] = page.evaluate("document.querySelectorAll('canvas').length")
    ok = report["canvas_count"] > 0 and not report["page_errors"]
    browser.close()
report["ok"] = ok
(out / "report.json").write_text(json.dumps(report, indent=2))
sys.exit(0 if ok else 1)
