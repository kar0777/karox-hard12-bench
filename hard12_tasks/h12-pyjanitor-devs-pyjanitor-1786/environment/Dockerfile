FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git init -q /testbed && cd /testbed \
 && git fetch -q --depth=1 https://github.com/pyjanitor-devs/pyjanitor.git 25c59554867e7040aa3b443ef6fb7ce36e5937cb \
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN cd /testbed && pip install -e . --quiet && pip install pytest pytest-xdist pytest-cov hypothesis --quiet && pip install polars --quiet && pip install unyt tqdm biopython pyspark rdkit --quiet && pip install requests tidyxl openpyxl --quiet && pip install --quiet pytest
WORKDIR /testbed
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all \
 && git gc --prune=now -q \
 && test "$(git rev-list --all | wc -l)" = "1" \
 && test "$(git rev-parse HEAD)" = "25c59554867e7040aa3b443ef6fb7ce36e5937cb"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
