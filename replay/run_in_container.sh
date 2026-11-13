#!/usr/bin/env bash
# Runs inside a task image: install the KaroX wheel the same way the harbor
# agent does, start the scripted endpoint, run karox agent run, check results.
# usage: run_in_container.sh SCENARIO_NAME  (replay dir mounted at /replay)
set -uo pipefail
SCENARIO=/replay/scenarios/$1.json
OUT=/replay-out
VENV=/tmp/karo-venv
PY=$VENV/bin/python
TASK_DIR=${TASK_DIR:-/app}
mkdir -p "$OUT" 2>/dev/null || OUT=/tmp/replay-out && mkdir -p "$OUT"

t0=$(date +%s)
if python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  if ! python3 -m venv $VENV >/dev/null 2>&1; then
    rm -rf $VENV && python3 -m venv --without-pip $VENV &&
    $PY -c "import urllib.request; exec(urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py', timeout=120).read())" --quiet
  fi
else
  python3 -m venv /tmp/karo-uv && /tmp/karo-uv/bin/python -m pip install --quiet uv &&
  /tmp/karo-uv/bin/uv venv --quiet --seed --python 3.12 $VENV
fi
$PY -m pip install --quiet --force-reinstall /replay/karox_runtime-5.0.0-py3-none-any.whl || { echo "INSTALL FAILED"; exit 2; }
echo "install: $(( $(date +%s) - t0 ))s"

LOG=$OUT/requests.jsonl
: > "$LOG"
python3 /replay/mock_openai.py "$SCENARIO" "$LOG" 18555 >"$OUT/mock.log" 2>&1 &
MOCK=$!
for _ in $(seq 50); do python3 -c "import socket; socket.create_connection(('127.0.0.1', 18555), 1)" 2>/dev/null && break; sleep 0.2; done

export KAROX_PROVIDER_REPLAY_API_KEY=replay-not-a-secret
export KAROX_VNEXT_CONFIG_DIR=$OUT/karox-config KAROX_VNEXT_RUNTIME_DIR=$OUT/karox-runtime
TASK=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['task'])" "$SCENARIO")
cd "$TASK_DIR"
$PY -m karox.cli provider add replay --adapter openai_compatible_chat --base-url http://127.0.0.1:18555/v1 \
  --credential-ref env:KAROX_PROVIDER_REPLAY_API_KEY --timeout-seconds 60 --max-transport-retries 0 --json >/dev/null
$PY -m karox.cli model add replay replay --context-window 1048576 --max-output-tokens 32768 \
  --tools true --streaming true --structured-output unknown --vision unknown --provenance "offline replay" --json >/dev/null
t1=$(date +%s)
$PY -m karox.cli agent run --repository "$TASK_DIR" --route replay/replay --max-steps 40 --max-seconds 600 \
  --verification-command '["bash","-lc","*"]' --verification-command '["python3","*"]' \
  --task "$TASK" --stream --json > "$OUT/agent.log" 2>&1
RC=$?
echo "agent run: $(( $(date +%s) - t1 ))s exit=$RC"
kill $MOCK 2>/dev/null
tail -c 1500 "$OUT/agent.log"; echo
python3 /replay/check_replay.py "$SCENARIO" "$LOG" "$RC"
