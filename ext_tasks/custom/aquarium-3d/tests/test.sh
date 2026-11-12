#!/bin/bash
# No automatic grading: the owner judges the page visually. Keep every HTML the agent wrote.
mkdir -p /logs/verifier/out
cp /app/*.html /logs/verifier/out/ 2>/dev/null || true
if [ -s /app/aquarium-test.html ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 > /logs/verifier/reward.txt; fi
ls -la /logs/verifier/out
