You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ModuleNotFoundError: No module named 'cron.jobs'

Hello,

I need your help to figure out whether this is a bug in Hermes WebUI/Agent or an issue with my installation's configuration.

I'm getting an “Error: Internal server error” message in the “Task” tab.

When I look at the hermes-webui logs, the following error appears every time I click on the “Task” tab:
```
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]: [webui] ERROR GET /api/crons
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]: Traceback (most recent call last):
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]:   File "/app/server.py", line 354, in do_GET
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]:     result = handle_get(self, parsed)
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]:              ^^^^^^^^^^^^^^^^^^^^^^^^
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]:   File "/app/api/routes.py", line 10026, in handle_get
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]:     from cron.jobs import list_jobs
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]: ModuleNotFoundError: No module named 'cron.jobs'
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]: 
Jun 23 08:33:23 instance-20260622-1202 hermes-webui[2241]: [webui] {"ts": "2026-06-23T08:33:23Z", "remote": "10.90.90.129", "method": "GET", "path": "/api/crons", "status": 500, "ms": 6.2, "forwarded_for": "10.90.89>
```

I don't see any errors in the Hermes agent logs

I don't know if this is the same bug as that one, but the thread has been closed.
https://github.com/nesquena/hermes-webui/issues/4700

This is a fresh installation:
- Oracle VPS Free Tier / Ubuntu ARM
- Podman / Rootless
- Separate hermes-agent and hermes-webui containers
- WebUI: v0.51.601 Agent: 0.17.0
- Gateway Status is Running in webui > system

Here are the -shrinked- container's files :

```
cat ~/.config/containers/systemd/hermes-agent.container 
[Unit]
After=network-online.target

[Container]
Image=docker.io/nousresearch/hermes-agent:latest

Network=hermes.network:ip=10.89.11.130

Volume=%h/containers/hermes/data:/home/hermes/.hermes:z,U

Environment=TZ=Europe/Paris
Environment=HERMES_HOME=/home/hermes/.hermes
Environment=HERMES_DATA_DIR=/home/hermes/.hermes
Environment=HERMES_UID=1002
Environment=HERMES_GID=1002
Environment=HERMES_HOME_MODE=0750
# Environment=GATEWAY_ALLOW_ALL_USERS=true
Environment=GATEWAY_HOST=10.89.11.130
Environment=HERMES_AGENT_HOST=10.89.11.130
Environment=API_SERVER_ENABLED=true
Environment=API_SERVER_HOST=10.89.11.130
Environment=API_SERVER_PORT=8642

EnvironmentFile=%h/containers/hermes/.env
Exec=gateway run
(...)
```

```
cat ~/.config/containers/systemd/hermes-webui.container 
[Unit]
After=network-online.target hermes-agent.service traefik.service
Requires=traefik.service hermes-agent.service

[Container]
Image=ghcr.io/nesquena/hermes-webui:latest

Network=traefik.network
Network=hermes.network:ip=10.89.11.120

Volume=%h/containers/hermes/data:/home/hermeswebui/.hermes:z,U
Volume=%h/containers/hermes/data/workspace:/workspace:z,U
Volume=%h/containers/hermes/agent:/home/hermeswebui/.hermes/hermes-agent:ro,z

Environment=TZ=Europe/Paris
Environment=HERMES_WEBUI_HOST=0.0.0.0
Environment=HERMES_WEBUI_PORT=8787
Environment=HERMES_WEBUI_STATE_DIR=/home/hermeswebui/.hermes/webui
Environment=HERMES_WEBUI_CHAT_BACKEND=gateway
Environment=HERMES_WEBUI_GATEWAY_BASE_URL=http://10.89.11.130:8642
EnvironmentFile=%h/containers/hermes/.env

Environment=WANTED_UID=1002
Environment=WANTED_GID=1002
Environment=HERMES_WEBUI_ONBOARDING_OPEN=1
Environment=HERMES_WEBUI_TRUST_FORWARDED_FOR=1
Environment=HERMES_HOME_MODE=0777
(...)
```

```
cat containers/hermes/.env | awk -F '=' '{print $1}'
API_SERVER_KEY
HERMES_WEBUI_GATEWAY_API_KEY
```

Thank you in advance for your help

