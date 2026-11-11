FROM swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5858:latest

ENV _JAVA_OPTIONS=""

ARG UV_URL=https://astral.sh/uv/0.7.13/install.sh
RUN (curl -fsSL "$UV_URL" 2>/dev/null || wget -qO- "$UV_URL") | UV_INSTALL_DIR=/usr/local/bin sh
RUN mkdir -p /logs
RUN cd /testbed \
 && git config --global --add safe.directory /testbed \
 && (git remote | xargs -r -n1 git remote remove) \
 && git branch -f hard12-base HEAD 2>/dev/null; git checkout -q hard12-base 2>/dev/null; \
 (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \
 && git reflog expire --expire=now --all && git gc --prune=now -q
ENV PATH=/opt/conda/envs/nicegui/bin:/opt/miniconda3/envs/nicegui/bin:$PATH
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
