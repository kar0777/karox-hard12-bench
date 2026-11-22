"""Read the scope probe: what the model does at a recorded scope decision under the old
and the new base prompt.

    python scope_probe_read.py <cases dir> <probe out dir> [--show N]

The cases come from `scripts/build_scope_cases.py` (a saved KaroX run cut just before the
first step that quoted "smallest ... change" or "broaden"), the samples from
`scripts/replay_probe.py`. Per variant: samples, how many quote the removed rules, how
many use the new ones, how many decide by "not asked / out of scope", reasoning length,
and the tools of the sampled step. --show N prints, per sample, N characters around each
scope word, next to the recorded step's own passage: the decision is read there by eye.
"""
import collections
import glob
import json
import os
import re
import sys

OLD = re.compile(r"smallest (?:general )?change|broaden|exact contract", re.I)
NEW = re.compile(r"samples?\b|spell(?:ed)? out|rules? (?:it|them) out|every affected input|"
                 r"other forms|neighbou?ring", re.I)
NARROW = re.compile(r"out of scope|scope creep|(?:not|n't|isn't) (?:asked|requested|required|"
                    r"mentioned)|more than asked|beyond (?:the )?(?:issue|task|scope)", re.I)
NOT_ASKED = "decides by 'not asked'"


def passages(text, width):
    for match in re.finditer(f"{OLD.pattern}|{NEW.pattern}|{NARROW.pattern}", text, re.I):
        a, b = max(0, match.start() - width), min(len(text), match.end() + width)
        yield text[a:b].replace("\n", " ")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cases_dir, out_dir = sys.argv[1], sys.argv[2]
    show = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 0
    cases = json.load(open(os.path.join(cases_dir, "cases.json"), encoding="utf-8"))
    stats = collections.defaultdict(collections.Counter)
    for case in cases:
        samples = []
        for path in sorted(glob.glob(os.path.join(out_dir, f"{case['case']}.*.json"))):
            sample = json.load(open(path, encoding="utf-8"))
            if not sample.get("error"):
                samples.append(sample)
        if show:
            print(f"\n== {case['task']} step {case['step']} ({case['variant']} prompt; the run "
                  f"{'solved' if case['solved'] else 'did not solve'} the task)")
            if case["variant"] == "old":
                for text in list(passages(case["recorded"], show))[:2]:
                    print(f"   recorded: ...{text}...")
        for sample in samples:
            text = (sample.get("reasoning") or "") + "\n" + (sample.get("content") or "")
            row = stats[case["variant"]]
            row["samples"] += 1
            row["old rule quoted"] += bool(OLD.search(text))
            row["new rule used"] += bool(NEW.search(text))
            row[NOT_ASKED] += bool(NARROW.search(text))
            row["reasoning chars"] += len(sample.get("reasoning") or "")
            for name in sample.get("tool_calls") or ["(no tool call)"]:
                row[f"tool {name}"] += 1
            if show:
                print(f"   sample {sample['sample']}: tools {sample.get('tool_calls')}")
                for text in list(passages(text, show))[:4]:
                    print(f"      ...{text}...")
    print("\nvariant | samples | old rule quoted | new rule used | decides by 'not asked' | "
          "reasoning chars per sample | tools of the step")
    for variant, row in stats.items():
        n = max(row["samples"], 1)
        tools = ", ".join(f"{k[5:]} {v}" for k, v in sorted(row.items()) if k.startswith("tool "))
        print(f"{variant} | {row['samples']} | {row['old rule quoted']} | {row['new rule used']} | "
              f"{row[NOT_ASKED]} | {row['reasoning chars'] / n:.0f} | {tools}")


if __name__ == "__main__":
    main()
