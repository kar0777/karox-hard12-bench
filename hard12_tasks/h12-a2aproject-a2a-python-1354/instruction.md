You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: Client transports reject responses with unrecognized fields (spec 5.7)

### What happened?

The 1.0 client transports reject any response that carries a field they don't know. A `SendMessage` result with one extra key fails with `ParseError` and the caller gets no answer, even though the `message` in it is valid.

Spec [5.7](https://a2a-protocol.org/latest/specification/#57-field-presence-and-optionality) says: "Implementations **SHOULD** ignore unrecognized fields in messages, allowing for forward compatibility as the protocol evolves."

#1273 applied this to the server (`jsonrpc_dispatcher.py`, `rest_dispatcher.py`). The client side is still strict:

- `client/transports/jsonrpc.py`: every `json_format.ParseDict(json_rpc_response.result, ...)` (`send_message`, `get_task`, `list_tasks`, `cancel_task`, the push-notification config methods, `get_extended_agent_card`) and the streaming `ParseDict(..., StreamResponse())`.
- `client/transports/rest.py`: the same set of `ParseDict(response_data, ...)` calls.

The rest of the client is already lenient: `client/card_resolver.py` (`parse_agent_card`) and the v0.3 compat transport (`compat/v0_3/rest_transport.py`) both pass `ignore_unknown_fields=True`. So a client talking to a 1.0 agent is stricter than the same client talking to a 0.3 agent.

**Expected:** unknown fields in a response are ignored and the valid payload is returned, as on the server since #1273.

**Why it matters:** a server one minor version ahead (or one that adds a vendor field) breaks every client on an older SDK. Gateways built on this client inherit it: LiteLLM's A2A proxy calls `client.send_message`, so an agent whose `SendMessage` result has an extra key cannot be called through LiteLLM at all. We hit exactly this with a third-party agent that returns `{"message": {...}, "status": "COMPLETED"}`.

**Reproduction** (a2a-sdk 1.2.2, also present on `main`; no network needed):

```python
import asyncio
import json
import uuid

import httpx
from a2a.client import ClientConfig, ClientFactory
from a2a.client.card_resolver import parse_agent_card
from a2a.types import a2a_pb2

CARD = {
    "name": "demo",
    "description": "demo",
    "version": "1.0.0",
    "capabilities": {},
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [{"id": "s", "name": "s", "description": "s", "tags": []}],
    "supportedInterfaces": [
        {"url": "https://agent.example", "protocolBinding": "JSONRPC", "protocolVersion": "1.0"}
    ],
}


def agent(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={
        "jsonrpc": "2.0",
        "id": json.loads(request.content)["id"],
        "result": {
            "message": {"messageId": "r1", "role": "ROLE_AGENT", "parts": [{"text": "hello"}]},
            # A field this SDK version does not know (e.g. added by a newer spec minor version).
            "someNewField": "x",
        },
    })


async def main() -> None:
    async with httpx.AsyncClient(transport=httpx.MockTransport(agent)) as http:
        client = ClientFactory(ClientConfig(httpx_client=http, streaming=False)).create(parse_agent_card(CARD))
        request = a2a_pb2.SendMessageRequest(message=a2a_pb2.Message(
            role=a2a_pb2.Role.ROLE_USER, message_id=uuid.uuid4().hex, parts=[a2a_pb2.Part(text="hi")]))
        async for event in client.send_message(request):
            print(event)


asyncio.run(main())
```

Removing `someNewField` makes it print the message.

**Suggested fix:** pass `ignore_unknown_fields=True` at the response-parsing call sites in `client/transports/jsonrpc.py` and `client/transports/rest.py`, mirroring #1273. The enum caveat discussed there (an unknown enum value becomes `0`) applies here too.

### Relevant log output

```shell
google.protobuf.json_format.ParseError: Message type "lf.a2a.v1.SendMessageResponse" has no field named "someNewField" at "SendMessageResponse".
 Available Fields(except extensions): "['task', 'message']"
```

### Code of Conduct

- [x] I agree to follow this project's Code of Conduct

