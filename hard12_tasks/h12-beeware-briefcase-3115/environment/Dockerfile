FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git init -q /testbed && cd /testbed \
 && git fetch -q --depth=1 https://github.com/beeware/briefcase.git ae0eca3d3282fe74c05d966e346c6e1395f435dc \
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN cd /testbed && pip install -q pytest==9.0.2 coverage[toml]==7.13.2 coverage-conditional-plugin==0.9.0 httpx-retries==0.4.5 pytest-xdist==3.8.0 && pip install -q -e . && pip install --quiet pytest
WORKDIR /testbed
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all \
 && git gc --prune=now -q \
 && test "$(git rev-list --all | wc -l)" = "1" \
 && test "$(git rev-parse HEAD)" = "ae0eca3d3282fe74c05d966e346c6e1395f435dc"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
