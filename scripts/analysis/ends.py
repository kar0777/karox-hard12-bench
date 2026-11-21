import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = sys.argv[1]
pat = sys.argv[2] if len(sys.argv) > 2 else ""
for path in sorted(glob.glob(os.path.join(root, "**", "karox6.jsonl"), recursive=True)):
    if pat and pat not in path:
        continue
    task = path.replace("\\", "/").split("/jobs/")[-1].split("/")[0] if "/jobs/" in path.replace("\\", "/") else path
    fin = None; n_usage = 0; notices = []; errs = []; cut = 0; steps = 0
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("type")
        if t == "run_finished":
            fin = e
        elif t == "usage":
            n_usage += 1
        elif t == "notice":
            notices.append(e.get("kind"))
        elif t == "error":
            errs.append((e.get("code"), (e.get("message") or "")[:100]))
        elif t == "assistant_message":
            steps += 1
            if e.get("finish_reason") == "length":
                cut += 1
    rdir = os.path.dirname(os.path.dirname(path))
    reward = "?"
    try:
        reward = open(os.path.join(rdir, "verifier", "reward.txt")).read().strip()
    except OSError:
        pass
    if fin:
        print(f"{task[-48:]:48} reward {reward} {fin['status']:9} steps {fin['steps']:3} {fin['elapsed_s']:6.0f}s cut {cut} notices {dict((k, notices.count(k)) for k in set(notices))} reason: {(fin.get('reason') or '')[:90]}")
    else:
        print(f"{task[-48:]:48} reward {reward} NO run_finished; usage events {n_usage}")
