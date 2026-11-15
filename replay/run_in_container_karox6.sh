#!/usr/bin/env bash
# KaroX 6 variant of run_in_container.sh: install the karox6 wheel the way
# harbor_agents/karox6_agent.py does, run `karox6 run` against the scripted
# endpoint, then check the requests, the event stream and the finish snapshot.
# usage: run_in_container_karox6.sh SCENARIO_NAME  (replay dir mounted at /replay)
set -uo pipefail
SCENARIO=/replay/scenarios/$1.json
OUT=/replay-out
VENV=/tmp/karox6-venv
PY=$VENV/bin/python
TASK_DIR=${TASK_DIR:-/app}
mkdir -p "$OUT" 2>/dev/null || OUT=/tmp/replay-out && mkdir -p "$OUT"

t0=$(date +%s)
mkvenv() {
  python3 -m venv "$1" >/dev/null 2>&1 || {
    rm -rf "$1" && python3 -m venv --without-pip "$1" &&
    "$1/bin/python" -c "import urllib.request; exec(urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py', timeout=120).read())" --quiet
  }
}
if python3 -c 'import sys; sys.exit(sys.version_info < (3, 12))'; then
  mkvenv $VENV
else
  mkvenv /tmp/karox6-uv && /tmp/karox6-uv/bin/python -m pip install --quiet uv &&
  /tmp/karox6-uv/bin/uv venv --quiet --seed --python 3.12 $VENV
fi
WHEEL=$(ls /replay/karox6-*.whl | tail -1)
$PY -m pip install --quiet --force-reinstall "$WHEEL" || { echo "INSTALL FAILED"; exit 2; }
echo "install: $(( $(date +%s) - t0 ))s ($($PY -m karox6 --version))"

LOG=$OUT/requests.jsonl
: > "$LOG"
python3 /replay/mock_openai.py "$SCENARIO" "$LOG" 18555 >"$OUT/mock.log" 2>&1 &
MOCK=$!
for _ in $(seq 50); do python3 -c "import socket; socket.create_connection(('127.0.0.1', 18555), 1)" 2>/dev/null && break; sleep 0.2; done

export REPLAY_GATEWAY_KEY=replay-not-a-secret
TASK=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['task'])" "$SCENARIO")
EXTRA=$(python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1])).get('karox6_flags', [])))" "$SCENARIO")
cd "$TASK_DIR"
t1=$(date +%s)
$PY -m karox6 run --json --provider openai-chat --base-url http://127.0.0.1:18555/v1 \
  --api-key-env REPLAY_GATEWAY_KEY --model replay --context-window 1048576 --max-output-tokens 32768 \
  --max-steps 40 --max-seconds 600 --home "$OUT/karox6" --cwd "$TASK_DIR" --approve-dangerous deny \
  $EXTRA -- "$TASK" </dev/null >"$OUT/events.jsonl" 2>"$OUT/stderr.txt"
RC=$?
echo "agent run: $(( $(date +%s) - t1 ))s exit=$RC"
kill $MOCK 2>/dev/null
tail -c 1500 "$OUT/events.jsonl"; echo
tail -c 1500 "$OUT/stderr.txt"
python3 /replay/check_replay.py "$SCENARIO" "$LOG" "$RC"; A=$?
python3 /replay/check_karox6.py "$SCENARIO" "$OUT"; B=$?
[ "$A" = 0 ] && [ "$B" = 0 ]
