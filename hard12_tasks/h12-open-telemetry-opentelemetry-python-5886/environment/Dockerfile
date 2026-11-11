FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git init -q /testbed && cd /testbed \
 && git fetch -q --depth=1 https://github.com/open-telemetry/opentelemetry-python.git 2b1246ed8dc4d409751b75b685db3b2cf064b2b7 \
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN cd /testbed && pip install uv -q && uv pip install -e ./opentelemetry-api --no-deps --system -q && uv pip install -e ./opentelemetry-semantic-conventions --no-deps --system -q && uv pip install -e ./opentelemetry-sdk --no-deps --system -q && uv pip install -e ./tests/opentelemetry-test-utils --no-deps --system -q && uv pip install pytest pytest-cov pluggy packaging --system -q && uv pip install typing-extensions importlib-metadata --system -q && pip install --quiet pytest
WORKDIR /testbed
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all \
 && git gc --prune=now -q \
 && test "$(git rev-list --all | wc -l)" = "1" \
 && test "$(git rev-parse HEAD)" = "2b1246ed8dc4d409751b75b685db3b2cf064b2b7"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
