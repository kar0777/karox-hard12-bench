FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN git init -q /testbed && cd /testbed \
 && git fetch -q --depth=1 https://github.com/pipecat-ai/pipecat.git 833b382155713d69f13c5cd9227678e148c2b4e3 \
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN cd /testbed && pip install -e . --quiet && pip install pytest pytest-asyncio pytest-aiohttp --quiet && pip install websockets --quiet && pip install python-dotenv starlette fastapi anthropic google-genai langchain-core langchain-openai piper-tts --quiet && pip install google-api-core deepgram-sdk livekit aioboto3 uvicorn --quiet && pip install aws-sdk-sagemaker-runtime-http2 --quiet && pip install --quiet pytest
WORKDIR /testbed
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all \
 && git gc --prune=now -q \
 && test "$(git rev-list --all | wc -l)" = "1" \
 && test "$(git rev-parse HEAD)" = "833b382155713d69f13c5cd9227678e148c2b4e3"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
