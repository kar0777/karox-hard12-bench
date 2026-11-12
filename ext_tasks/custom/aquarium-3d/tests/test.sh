#!/bin/bash
# Visual verifier: serve /app over http, render the page in the image's Chromium
# (software WebGL), save screenshots over time and after orbit/zoom, and record
# every console/page error. The owner judges the pictures; reward only says the
# page exists, loaded and drew a canvas without page errors.
mkdir -p /logs/verifier/out
cp /app/*.html /logs/verifier/out/ 2>/dev/null || true
cd /app && (python3 -m http.server 8765 --bind 127.0.0.1 >/tmp/http.log 2>&1 &)
python3 /tests/shoot.py http://127.0.0.1:8765/aquarium-test.html /logs/verifier/out
rc=$?
if [ $rc -eq 0 ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 > /logs/verifier/reward.txt; fi
cat /logs/verifier/out/report.json 2>/dev/null
ls -la /logs/verifier/out
