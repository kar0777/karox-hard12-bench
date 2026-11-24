You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Compat REST client drops security from the v0.3 extended agent card

## What happens

`CompatRestTransport.get_extended_agent_card` against a v0.3 server turns an HTTP bearer scheme into an empty OpenIdConnect scheme, and card and skill `security` come back as `[{}]`.

## Why

It parses `GET /v1/card` as v0.3 proto JSON. v0.3 servers, including `REST03Handler`, send the pydantic card JSON. `CompatJsonRpcTransport` already parses it with `types_v03.AgentCard.model_validate`.

## Version

main @ 11f1116

