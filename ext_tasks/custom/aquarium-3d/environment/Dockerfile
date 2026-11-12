# Web-task image: Microsoft's official Playwright image (Chromium + every system
# library it needs). The python package is pinned to the image's browser build so
# any agent's playwright, and the verifier, find the same Chromium. The symlink is
# the one browser every arm is pointed at (KaroX via its pinned playwright,
# OpenCode via Playwright MCP --executable-path). python3-venv: agents build venvs.
FROM mcr.microsoft.com/playwright/python:v1.55.0-noble
RUN apt-get update && apt-get install -y --no-install-recommends python3.12-venv \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir --break-system-packages playwright==1.55.0 \
 && ln -sf "$(ls -d /ms-playwright/chromium-*/chrome-linux/chrome | head -1)" /usr/local/bin/chromium-pw \
 && /usr/local/bin/chromium-pw --version \
 && echo 1.55.0 > /opt/playwright-version
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh && mkdir -p /app
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
