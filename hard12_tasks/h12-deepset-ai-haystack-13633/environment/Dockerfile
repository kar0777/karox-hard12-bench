FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git init -q /testbed && cd /testbed \
 && git fetch -q --depth=1 https://github.com/deepset-ai/haystack.git 8872d2bfba932964638c26575b074184913a8074 \
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN cd /testbed && pip install -q hatch && pip install -q -e . && pip install -q pytest pytest-cov pytest-asyncio pandas numpy numba opentelemetry-sdk ddtrace structlog 'httpx[http2]' azure-identity pytest-bdd pytest-rerunfailures coverage mypy pylint ipython colorama anyio jsonref openapi3 openapi-llm nltk tiktoken rich pillow pypdfium2 pypdf 'pdfminer.six' markdown-it-py mdit_plain trafilatura python-pptx python-docx jq openpyxl tabulate python-oxmsg langdetect arrow azure-ai-formrecognizer && pip install --quiet pytest
WORKDIR /testbed
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all \
 && git gc --prune=now -q \
 && test "$(git rev-list --all | wc -l)" = "1" \
 && test "$(git rev-parse HEAD)" = "8872d2bfba932964638c26575b074184913a8074"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
