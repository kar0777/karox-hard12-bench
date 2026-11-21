"""Consecutive length-cut replies in karox6 event logs: how often the reply after a cut is cut again."""
import collections, glob, json, os, sys
runs = collections.Counter(); after = collections.Counter(); kinds = collections.Counter()
ended = 0; total_cut = 0; files = 0
for root in sys.argv[1:]:
    seen = set()
    for path in glob.glob(os.path.join(root, "**", "karox6.jsonl"), recursive=True):
        key = os.path.basename(os.path.dirname(os.path.dirname(path)))
        if key in seen:
            continue
        seen.add(key); files += 1
        seq = []
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "assistant_message":
                cut = e.get("finish_reason") == "length"
                empty = not (e.get("text") or "").strip() and not e.get("tool_calls")
                seq.append("T" if cut and empty else "C" if cut else ".")
            elif e.get("type") == "run_finished" and "cut off" in (e.get("reason") or ""):
                ended += 1
        s = "".join(seq)
        total_cut += s.count("T") + s.count("C")
        kinds["thinking-only"] += s.count("T"); kinds["with text/calls"] += s.count("C")
        i = 0
        while i < len(s):
            if s[i] in "TC":
                j = i
                while j < len(s) and s[j] in "TC":
                    j += 1
                runs[j - i] += 1
                i = j
            else:
                i += 1
        for a, b in zip(s, s[1:]):
            if a == "T":
                after["T->cut" if b in "TC" else "T->ok"] += 1
print(f"logs {files}; cut replies {total_cut} {dict(kinds)}; runs ended on repeated cuts {ended}")
print("lengths of consecutive cut streaks:", dict(sorted(runs.items())))
print("after a thinking-only cut:", dict(after), f"=> cut again {after['T->cut']/max(sum(after.values()),1):.0%}")
