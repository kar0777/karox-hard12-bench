FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git init -q /testbed && cd /testbed \
 && git fetch -q --depth=1 https://github.com/apache/iceberg-python.git e9f7f6b43dcefa9ccbd02be47d71e630921e54dd \
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN cd /testbed && pip install -q -e ".[pyarrow,pandas,hive,s3fs,glue,adlfs,dynamodb,bigquery,datafusion]" pytest pytest-mock pytest-lazy-fixtures requests-mock moto fastavro coverage pytz sqlalchemy google-cloud-bigquery && pip install --quiet pytest
WORKDIR /testbed
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all \
 && git gc --prune=now -q \
 && test "$(git rev-list --all | wc -l)" = "1" \
 && test "$(git rev-parse HEAD)" = "e9f7f6b43dcefa9ccbd02be47d71e630921e54dd"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
