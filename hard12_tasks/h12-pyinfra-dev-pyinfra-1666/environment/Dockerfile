FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git init -q /testbed && cd /testbed \
 && git fetch -q --depth=1 https://github.com/pyinfra-dev/pyinfra.git e85107be0675073e0af3f0df05b5ebee16b5dda0 \
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN cd /testbed && pip install -e . --quiet && pip install "pytest>=8.3.5,<9" "coverage>=7.7.1,<8" "pytest-cov>=7.0.0,<8" "pytest-testinfra>=10.2.2,<11" "pyyaml>=6.0.2,<7" --quiet && pip install freezegun --quiet && pip install pyinfra-testgen==0.1.1 --quiet && pip install --quiet pytest
WORKDIR /testbed
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all \
 && git gc --prune=now -q \
 && test "$(git rev-list --all | wc -l)" = "1" \
 && test "$(git rev-parse HEAD)" = "e85107be0675073e0af3f0df05b5ebee16b5dda0"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
