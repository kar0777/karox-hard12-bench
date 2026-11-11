"""Loopback relay for harness-race task containers (plumbing, identical for all arms).

    python karo_relay.py <listen-port> <target-host:port>

Byte pump from 127.0.0.1:<listen-port> to the race gateway's *unwrap* listener.
Every upstream connection starts with a fixed 8-byte non-HTTP preamble
(PREAMBLE below); gateway/race_unwrap.py on the host checks and strips it and
forwards the untouched byte stream to litellm / the Responses translator.

Why: Harbor's egress-control sidecar (gost, "red" handler with sniffing) parses
EVERY HTTP/1.x request it sees and aborts it when the response head does not
arrive within ~15 s ("read response: i/o timeout"). Streaming responses send
bytes early and survived, but non-streaming model calls (Claude Code falls back
to them) routinely take 40-110 s and were cut -> ECONNRESET, 17 retries, run
lost (swe1-1x4-r4-claude). Reproduced with a slow HTTP server behind the real
sidecar image: plain HTTP >15 s fails on every request of a keep-alive
connection; with this preamble the sniffer falls back to raw TCP
(sniffing.fallback) and 40/120/250 s responses pass. The allowlist still
applies by destination IP (172.16.0.0/12), and public hosts stay blocked.

Previous versions rewrote the Host header of the first request; that only
fixed the allowlist match and left the 15 s cut in place.
"""
import asyncio
import sys

PREAMBLE = b"\x00KRLY1\r\n"  # 8 bytes; NUL first -> never parsed as HTTP/TLS


async def pump(reader, writer):
    try:
        while True:
            chunk = await reader.read(65536)
            if not chunk:
                break
            writer.write(chunk)
            await writer.drain()
    except OSError:
        pass
    finally:
        try:
            # propagate a half-close only: the response must keep flowing
            # after the request side EOFs
            writer.write_eof()
        except (OSError, NotImplementedError, RuntimeError):
            try:
                writer.close()
            except OSError:
                pass


def make_handler(target_host: str, target_port: int):
    async def handle(reader, writer):
        try:
            # HARD12: send the preamble in the SAME segment as the first client
            # bytes. Harbor's egress sidecar (gost) classifies a connection by
            # its first segment; a bare 8-byte preamble was reset (diag 2026-11-10).
            first = await reader.read(65536)
            if not first:
                writer.close()
                return
            ur, uw = await asyncio.open_connection(target_host, target_port)
            uw.write(PREAMBLE + first)
            await uw.drain()
        except OSError:
            writer.close()
            return
        try:
            await asyncio.gather(pump(reader, uw), pump(ur, writer))
        finally:
            for w in (writer, uw):
                try:
                    w.close()
                except OSError:
                    pass

    return handle


async def serve(listen_port: int, target: str, listen_host: str = "127.0.0.1"):
    host, port = target.rsplit(":", 1)
    server = await asyncio.start_server(make_handler(host, int(port)), listen_host, listen_port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(serve(int(sys.argv[1]), sys.argv[2]))
