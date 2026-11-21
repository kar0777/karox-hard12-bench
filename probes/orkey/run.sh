#!/usr/bin/env bash
# OpenRouter key limits (no secret printed): key info, credits, rate-limit headers of one
# 5-token request to a free model. Writes out/orkey.txt.
set -u
mkdir -p out
H="Authorization: Bearer $OPENROUTER_API_KEY"
{
  echo "== /key"; curl -s -m 20 -H "$H" https://openrouter.ai/api/v1/key | python3 -c "import json,sys; d=json.load(sys.stdin).get('data',{}); d.pop('label',None); print(json.dumps(d,indent=1))"
  echo "== /credits"; curl -s -m 20 -H "$H" https://openrouter.ai/api/v1/credits | python3 -c "import json,sys; print(json.load(sys.stdin).get('data'))"
  for m in nvidia/nemotron-3-ultra-550b-a55b:free z-ai/glm-5.3-flash; do
    echo "== headers $m"
    curl -s -m 60 -D - -o /tmp/body -H "$H" -H "Content-Type: application/json" https://openrouter.ai/api/v1/chat/completions \
      -d "{\"model\":\"$m\",\"max_tokens\":5,\"messages\":[{\"role\":\"user\",\"content\":\"say ok $RANDOM\"}]}" | grep -iE "^HTTP|ratelimit|retry-after"
    python3 -c "import json; d=json.load(open('/tmp/body')); print(d.get('usage') or d.get('error'))" 2>/dev/null
  done
} | tee out/orkey.txt
