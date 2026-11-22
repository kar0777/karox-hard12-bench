"""Cases for the scope probe: does the wording of the prompt change the scope decision?

Takes saved KaroX trials, finds the first step whose reasoning quotes one of the prompt's
two scope rules ("smallest ... change", "broaden") within its first 35 steps, cuts the
conversation just before it
and writes the request twice: with the base prompt the trial ran (`old`) and with the
installed one (`new`). `scripts/replay_probe.py` then samples the model's next step for
each; `scripts/analysis/scope_probe_read.py` reads the samples.

    <KaroX venv python> scripts/build_scope_cases.py OUT_DIR OLD_PROMPT.py RUN_DIR [...]

OLD_PROMPT.py: the `core/prompt.py` of the version the trials ran (`git show
<commit>:src/karox6/core/prompt.py`). Needs karox6 importable (the new prompt is the
installed one). Only dev-pool trials belong here: the cases carry the task's text.
"""

import glob
import gzip
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

from karox6.core.messages import Message
from karox6.core.prompt import BASE_PROMPT, build_system_prompt
from karox6.providers.base import ModelRequest
from karox6.providers.openai_chat import OpenAIChatProvider
from karox6.tools.registry import build_tools, tool_specs
from karox6.tools.shell import ShellInfo

SCOPE = re.compile(r"broaden|smallest (?:general )?change", re.IGNORECASE)
MAX_STEP = 35  # later quotes are about tidying the diff, and their requests are the largest


def load(session):
    messages, workdir = [], None
    for line in open(session, encoding="utf-8").read().split("\n"):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if row.get("kind") == "meta":
            workdir = row.get("workspace")
        elif row.get("kind") == "reset":
            messages = [Message.from_dict(m) for m in row["messages"]]
        elif row.get("kind") == "message":
            messages.append(Message.from_dict(row["message"]))
    return messages, workdir or "/testbed"


def main():
    out, old_file, runs = sys.argv[1], sys.argv[2], sys.argv[3:]
    spec = importlib.util.spec_from_file_location("old_prompt", old_file)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    prompts = {"old": old.BASE_PROMPT, "new": BASE_PROMPT}
    shell = ShellInfo(kind="bash", executable="/bin/bash", flavor="bash")
    tools = tool_specs(build_tools(shell))
    provider = OpenAIChatProvider(base_url="http://unused", api_key="unused")
    os.makedirs(out, exist_ok=True)
    cases = []
    for run in runs:
        pattern = f"{run}/trial-*/jobs/*/*/agent/karox6/sessions/*/session.jsonl"
        for session in sorted(glob.glob(pattern)):
            trial = Path(session).parents[4]
            messages, workdir = load(session)
            steps = [i for i, m in enumerate(messages) if m.role == "assistant"]
            cut = next((i for i in steps if SCOPE.search(messages[i].reasoning or "")), None)
            if cut is None or steps.index(cut) + 1 > MAX_STEP:
                continue
            try:
                result = json.load(open(trial / "result.json", encoding="utf-8"))
                reward = result["verifier_result"]["rewards"]["reward"]
            except (OSError, ValueError, KeyError, TypeError):
                reward = None
            task = trial.name.split("__")[0]
            name = f"{task}--{Path(run).name}--{trial.name.split('__')[1]}"
            for variant, base in prompts.items():
                system = build_system_prompt(Path(workdir), shell, base=base)
                system = re.sub(r"- Platform: [^\n]*", "- Platform: Linux; shell tool: bash", system)
                system = re.sub(r"- Python: [^\n]*\n?", "", system)
                system = re.sub(r"- Working directory: [^\n]*", f"- Working directory: {workdir}",
                                system)
                system = re.sub(r"- Git: [^\n]*", "- Git: (see the conversation)", system)
                request = ModelRequest(model="m", system=system, messages=messages[:cut],
                                       tools=tools)
                case = f"{name}--{variant}"
                os.makedirs(os.path.join(out, case), exist_ok=True)
                path = os.path.join(out, case, "request.json.gz")
                with gzip.open(path, "wt", encoding="utf-8") as handle:
                    json.dump(provider.build_body(request), handle, ensure_ascii=False)
                cases.append({"case": case, "variant": variant, "task": task,
                              "step": steps.index(cut) + 1, "solved": reward,
                              "recorded": (messages[cut].reasoning or "")[:6000]})
    with open(os.path.join(out, "cases.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(cases, handle, indent=1, ensure_ascii=False)
    open(os.path.join(out, ".replay"), "w").close()
    print(len(cases), "cases ->", out)


if __name__ == "__main__":
    main()
