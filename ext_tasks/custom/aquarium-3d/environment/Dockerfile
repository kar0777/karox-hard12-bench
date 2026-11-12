FROM python:3.12-slim
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh && mkdir -p /app && cd /app && python3 -c "print('ok')"
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
