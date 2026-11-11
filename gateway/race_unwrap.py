"""Host-side unwrap listener for the in-container race relays.

    python race_unwrap.py <listen-port>:<target-host:port> [...]

Accepts connections from task containers, requires the fixed preamble sent by
harbor_tasks/*/environment/karo_relay.py, strips it and pipes the rest of the
byte stream unchanged to the target (litellm :4000 or translator :4001).
Connections without the preamble are closed. See karo_relay.py for why the
preamble exists (Harbor egress sidecar cuts sniffed HTTP after ~15 s).
"""
from __future__ import annotations

import asyncio
import sys

PREAMBLE = b"\x00KRLY1\r\n"
PREAMBLE_TIMEOUT_S = 30.0


async def _pump(reader, writer):
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
            writer.write_eof()
        except (OSError, NotImplementedError, RuntimeError):
            try:
                writer.close()
            except OSError:
                pass


def make_handler(target_host: str, target_port: int):
    async def handle(reader, writer):
        try:
            head = await asyncio.wait_for(reader.readexactly(len(PREAMBLE)), PREAMBLE_TIMEOUT_S)
        except (asyncio.IncompleteReadError, asyncio.TimeoutError, OSError):
            writer.close()
            return
        if head != PREAMBLE:
            writer.close()
            return
        try:
            ur, uw = await asyncio.open_connection(target_host, target_port)
        except OSError:
            writer.close()
            return
        try:
            await asyncio.gather(_pump(reader, uw), _pump(ur, writer))
        finally:
            for w in (writer, uw):
                try:
                    w.close()
                except OSError:
                    pass

    return handle


def parse_spec(spec: str) -> tuple[int, str, int]:
    listen, target = spec.split(":", 1)
    host, port = target.rsplit(":", 1)
    return int(listen), host, int(port)


async def main(specs: list[str], listen_host: str = "0.0.0.0") -> None:
    servers = []
    for spec in specs:
        lp, th, tp = parse_spec(spec)
        servers.append(await asyncio.start_server(make_handler(th, tp), listen_host, lp))
    await asyncio.gather(*(s.serve_forever() for s in servers))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
