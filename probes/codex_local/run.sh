#!/usr/bin/env bash
# Local plumbing check of the bench's `codex` arm, no model and no key: Codex CLI ->
# the bench gateway (litellm + race_audit.py, ReformBoss config) -> a mock chat upstream
# that logs what it is sent. usage: run.sh <bench repo copy> <work dir> [strict]
set -uo pipefail
BENCH=$1; WORK=$2; MODE=${3:-}
rm -rf "$WORK"; mkdir -p "$WORK/gateway" "$WORK/audit/context" "$WORK/home" "$WORK/ws"
cp "$BENCH/gateway/race_audit.py" "$WORK/gateway/"
# Same config as the ReformBoss lane, upstream swapped for the local mock.
sed -e 's#https://api.reformboss.com/v1#http://127.0.0.1:4391/v1#' \
    -e 's#os.environ/REFORMBOSS_API_KEY#mock-key#' \
    "$BENCH/gateway/litellm.hard12.reformboss.yaml" > "$WORK/gateway/litellm.yaml"
printf '{"run_id": "local-codex", "task_id": "local"}\n' > "$WORK/audit/context/codex.json"
python3 "$(dirname "$0")/mock_chat.py" "$WORK/upstream.jsonl" 4391 $MODE >"$WORK/mock.log" 2>&1 &
MOCK=$!
(
  cd "$WORK/gateway"
  env -i PATH="$PATH" HOME="$HOME" HARNESS_RACE_GATEWAY_KEY=local-gw-key \
    HARNESS_RACE_AUDIT_DIR="$WORK/audit" LITELLM_TELEMETRY=False \
    HARNESS_RACE_PROFILE="$BENCH/config/inference_profile_hard12_reformboss.json" \
    ~/.local/share/uv/tools/litellm/bin/litellm --config litellm.yaml --host 127.0.0.1 \
    --port 4390 --num_workers 1 >"$WORK/litellm.log" 2>&1 &
  echo $! > "$WORK/litellm.pid"
)
for _ in $(seq 1 90); do
  python3 -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:4390/health/liveliness',timeout=3)" 2>/dev/null && break
  sleep 1
done
export CODEX_HOME="$WORK/home/.codex-hard12"; mkdir -p "$CODEX_HOME"
cat > "$CODEX_HOME/config.toml" <<'TOML'
model = "hard12-codex"
model_provider = "hard12"
model_context_window = 1048576
model_reasoning_effort = "high"
approval_policy = "never"
sandbox_mode = "danger-full-access"
[model_providers.hard12]
name = "HARD12 gateway"
base_url = "http://127.0.0.1:4390/v1"
env_key = "RACE_GATEWAY_KEY"
wire_api = "responses"
TOML
cd "$WORK/ws" && git init -q . 2>/dev/null
RACE_GATEWAY_KEY=local-gw-key timeout 120 npx -y @openai/codex@0.171.0 exec \
  --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --json \
  -- "Run echo hello and tell me what it printed." </dev/null >"$WORK/codex.jsonl" 2>&1
echo "codex rc=$?"
kill "$MOCK" "$(cat "$WORK/litellm.pid")" 2>/dev/null
sleep 1
echo "--- codex events"; cut -c1-300 "$WORK/codex.jsonl" | tail -12
echo "--- upstream requests: $(wc -l < "$WORK/upstream.jsonl" 2>/dev/null)"
echo "--- audit rows: $(wc -l < "$WORK/audit/audit.jsonl" 2>/dev/null)"
