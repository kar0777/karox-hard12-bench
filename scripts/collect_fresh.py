"""Deterministic candidate collector for pool3 (fresh blind coding-agent tasks).

Usage:
    python scripts/collect_fresh.py [--since 2026-11-11] [--until 2026-11-23T00:00:00Z] [--out data/candidates3.json]

Reads the distinct repos and their SWE-rebench recipes from data/candidates2.json,
queries merged PRs via the `gh` CLI (GraphQL + REST diff/issue/compare endpoints),
caches raw responses under .cache_pool3/, applies purely objective filters, excludes
any PR/issue already present in data/candidates2.json, data/night_tasks.txt, or
hard12_tasks/, caps at 2 per repo by lowest order_key, and writes up to 120
records sorted by order_key.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES2_PATH = ROOT / "data" / "candidates2.json"
NIGHT_TASKS_PATH = ROOT / "data" / "night_tasks.txt"
HARD12_DIR = ROOT / "hard12_tasks"
CACHE_DIR = ROOT / ".cache_pool3"
DEFAULT_OUT = ROOT / "data" / "candidates3.json"
DEFAULT_SINCE = "2026-11-11"
DEFAULT_UNTIL = "2026-11-23T00:00:00Z"
ORDER_SALT = "pool3-20261123|"
MAX_PER_REPO = 2
MAX_TOTAL = 120

GQL_MERGED_PRS = """
query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: [MERGED]
      orderBy: {field: UPDATED_AT, direction: DESC}
      first: 100
      after: $after
    ) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        number
        url
        title
        body
        createdAt
        mergedAt
        updatedAt
        baseRefOid
        headRefOid
        closingIssuesReferences(first: 10) {
          nodes {
            number
            title
            body
            createdAt
            repository {
              nameWithOwner
            }
          }
        }
      }
    }
  }
}
""".strip()

CLOSING_KW_RE = re.compile(
    r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s*"
    r"(?:#(\d+)|https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/issues/(\d+))\b"
)


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def normalize_iso(ts: str) -> str:
    s = ts.strip()
    if "T" not in s:
        s = s + "T00:00:00Z"
    dt = parse_iso(s).astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_git_exclude() -> None:
    """Add .cache_pool3/ to git info/exclude (never .gitignore)."""
    res = subprocess.run(
        ["git", "rev-parse", "--git-path", "info/exclude"],
        cwd=ROOT,
        capture_output=True,
    )
    if res.returncode != 0:
        return
    exclude_path = Path(res.stdout.decode("utf-8", errors="replace").strip())
    if not exclude_path.is_absolute():
        exclude_path = ROOT / exclude_path
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
    lines = [ln.strip() for ln in existing.splitlines()]
    if ".cache_pool3/" not in lines:
        sep = "" if (not existing or existing.endswith("\n")) else "\n"
        with open(exclude_path, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(f"{sep}.cache_pool3/\n")


def load_recipes_and_exclusions(out_path: Path) -> tuple[dict[str, dict[str, Any]], set[tuple[str, int]], set[tuple[str, int]]]:
    cands2 = json.loads(CANDIDATES2_PATH.read_text(encoding="utf-8"))
    recipes: dict[str, dict[str, Any]] = {}
    excluded_prs: set[tuple[str, int]] = set()
    excluded_issues: set[tuple[str, int]] = set()

    for r in cands2:
        repo = r["repo"]
        if repo not in recipes:
            recipes[repo] = {
                "image": r["image"],
                "install_config": r["install_config"],
                "image_instance": r["image_instance"],
            }
        excluded_prs.add((repo.lower(), int(r["pr"])))
        if r.get("issue") is not None:
            excluded_issues.add((repo.lower(), int(r["issue"])))

    # Later pools also skip every earlier pool's candidates (valid or not).
    for extra in sorted((ROOT / "data").glob("candidates[3-9].json")):
        if extra.resolve() == out_path.resolve():
            continue
        for r in json.loads(extra.read_text(encoding="utf-8")):
            excluded_prs.add((r["repo"].lower(), int(r["pr"])))
            if r.get("issue") is not None:
                excluded_issues.add((r["repo"].lower(), int(r["issue"])))

    if NIGHT_TASKS_PATH.exists():
        for line in NIGHT_TASKS_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            token = line.split()[0]
            if "#" in token:
                repo_part, num_part = token.rsplit("#", 1)
                if num_part.isdigit():
                    excluded_prs.add((repo_part.lower(), int(num_part)))

    if HARD12_DIR.exists():
        for readme in sorted(HARD12_DIR.glob("h12-*/README.md")):
            txt = readme.read_text(encoding="utf-8", errors="replace")
            m_src = re.search(r"https://github\.com/([^/\s]+/[^/\s]+)/pull/(\d+)", txt)
            if m_src:
                repo_l = m_src.group(1).lower()
                excluded_prs.add((repo_l, int(m_src.group(2))))
                m_iss = re.search(r"\|\s*issue\s*\|\s*#(\d+)", txt)
                if m_iss:
                    excluded_issues.add((repo_l, int(m_iss.group(1))))

    return recipes, excluded_prs, excluded_issues


class GitHubClient:
    def __init__(self, cache_dir: Path, sleep_sec: float = 0.25) -> None:
        self.cache_dir = cache_dir
        self.sleep_sec = sleep_sec
        self.api_calls = 0
        self.cache_hits = 0
        (cache_dir / "prs").mkdir(parents=True, exist_ok=True)
        (cache_dir / "issues").mkdir(parents=True, exist_ok=True)
        (cache_dir / "diffs").mkdir(parents=True, exist_ok=True)
        (cache_dir / "compare").mkdir(parents=True, exist_ok=True)

    def _run_gh(self, args: list[str], accept_404: bool = False) -> tuple[int, str, str]:
        backoff = 15.0
        for attempt in range(6):
            if self.sleep_sec > 0:
                time.sleep(self.sleep_sec)
            self.api_calls += 1
            proc = subprocess.run(
                ["gh", *args],
                capture_output=True,
                timeout=120,
            )
            stdout = proc.stdout.decode("utf-8", errors="replace")
            stderr = proc.stderr.decode("utf-8", errors="replace")
            if proc.returncode == 0:
                return 0, stdout, stderr

            err_low = (stderr + "\n" + stdout).lower()
            if accept_404 and ("404" in err_low or "not found" in err_low):
                return 404, stdout, stderr
            if "406" in err_low or "422" in err_low or "too large" in err_low:
                return proc.returncode, stdout, stderr

            is_rate = any(
                k in err_low
                for k in (
                    "403",
                    "429",
                    "rate limit",
                    "secondary rate",
                    "abuse",
                    "too many requests",
                )
            )
            is_transient = any(
                k in err_low
                for k in ("502", "503", "504", "timeout", "eof", "connection", "500")
            )
            if (is_rate or is_transient) and attempt < 5:
                wait = backoff * (2**attempt) if is_rate else min(30.0, 3.0 * (2**attempt))
                wait = min(wait, 180.0)
                print(
                    f"[warn] gh transient/rate error (attempt {attempt + 1}/6), sleeping {wait:.0f}s...",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(wait)
                continue
            return proc.returncode, stdout, stderr
        return 1, "", "max retries exceeded"

    def list_merged_prs(self, repo: str, since_iso: str, until_iso: str) -> list[dict[str, Any]]:
        safe_repo = repo.replace("/", "__")
        since_tag = since_iso.replace(":", "-")
        until_tag = until_iso.replace(":", "-")
        cache_file = self.cache_dir / "prs" / f"{safe_repo}__since_{since_tag}__until_{until_tag}__v2.json"
        if cache_file.exists():
            self.cache_hits += 1
            return json.loads(cache_file.read_text(encoding="utf-8"))

        owner, name = repo.split("/", 1)
        since_dt = parse_iso(since_iso)
        until_dt = parse_iso(until_iso)
        all_nodes: list[dict[str, Any]] = []
        cursor: str | None = None
        max_pages = 30
        failed = False

        for _ in range(max_pages):
            args = [
                "api",
                "graphql",
                "-f",
                f"owner={owner}",
                "-f",
                f"name={name}",
                "-f",
                f"query={GQL_MERGED_PRS}",
            ]
            if cursor is not None:
                args.extend(["-f", f"after={cursor}"])

            rc, stdout, stderr = self._run_gh(args)
            if rc != 0:
                print(
                    f"[warn] GraphQL failed for {repo}: rc={rc} {stderr.strip()[:200]}",
                    file=sys.stderr,
                    flush=True,
                )
                failed = True
                break

            payload = json.loads(stdout)
            repo_obj = (payload.get("data") or {}).get("repository")
            if not repo_obj:
                if payload.get("errors"):
                    print(
                        f"[warn] GraphQL errors for {repo}: {str(payload['errors'])[:200]}",
                        file=sys.stderr,
                        flush=True,
                    )
                    failed = True
                break
            prs_conn = repo_obj.get("pullRequests") or {}
            nodes = prs_conn.get("nodes") or []
            if not nodes:
                break

            stop = False
            for node in nodes:
                if not node:
                    continue
                updated = node.get("updatedAt")
                merged = node.get("mergedAt")
                if merged:
                    merged_dt = parse_iso(merged)
                    if since_dt <= merged_dt < until_dt:
                        all_nodes.append(node)
                if updated and parse_iso(updated) < since_dt:
                    stop = True

            page_info = prs_conn.get("pageInfo") or {}
            if stop or not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")
            if not cursor:
                failed = True
                print(
                    f"[warn] Missing endCursor with hasNextPage=True for {repo}; not caching incomplete list",
                    file=sys.stderr,
                    flush=True,
                )
                break
        else:
            failed = True
            print(
                f"[warn] Hit max_pages={max_pages} for {repo} without reaching stop; not caching incomplete list",
                file=sys.stderr,
                flush=True,
            )

        # Deduplicate by PR number in case pagination shifted slightly
        by_num: dict[int, dict[str, Any]] = {}
        for n in all_nodes:
            by_num[int(n["number"])] = n
        result = [by_num[k] for k in sorted(by_num)]
        if not failed:
            cache_file.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        return result

    def get_issue(self, repo: str, issue_num: int) -> dict[str, Any] | None:
        safe_repo = repo.replace("/", "__")
        cache_file = self.cache_dir / "issues" / f"{safe_repo}__{issue_num}.json"
        if cache_file.exists():
            self.cache_hits += 1
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            return None if cached.get("_missing") else cached

        rc, stdout, _stderr = self._run_gh(
            ["api", f"repos/{repo}/issues/{issue_num}"],
            accept_404=True,
        )
        if rc != 0:
            cache_file.write_text(json.dumps({"_missing": True, "rc": rc}), encoding="utf-8")
            return None

        data = json.loads(stdout)
        if "pull_request" in data:
            cache_file.write_text(json.dumps({"_missing": True, "_is_pr": True}), encoding="utf-8")
            return None

        slim = {
            "number": int(data["number"]),
            "title": data.get("title") or "",
            "body": data.get("body") or "",
            "createdAt": data.get("created_at") or "",
        }
        cache_file.write_text(json.dumps(slim, ensure_ascii=False), encoding="utf-8")
        return slim

    def get_pr_diff(self, repo: str, pr_num: int) -> str | None:
        safe_repo = repo.replace("/", "__")
        cache_file = self.cache_dir / "diffs" / f"{safe_repo}__{pr_num}.diff"
        err_file = self.cache_dir / "diffs" / f"{safe_repo}__{pr_num}.err"
        if cache_file.exists():
            self.cache_hits += 1
            return cache_file.read_text(encoding="utf-8", errors="replace")
        if err_file.exists():
            self.cache_hits += 1
            return None

        rc, stdout, stderr = self._run_gh(
            ["api", "-H", "Accept: application/vnd.github.v3.diff", f"repos/{repo}/pulls/{pr_num}"]
        )
        if rc != 0 or not stdout.strip():
            err_file.write_text(f"rc={rc}\n{stderr[:300]}\n", encoding="utf-8")
            return None

        cache_file.write_text(stdout, encoding="utf-8", newline="\n")
        return stdout

    def get_merge_base(self, repo: str, base_oid: str, head_oid: str) -> str | None:
        if base_oid == head_oid:
            return base_oid
        safe_repo = repo.replace("/", "__")
        cache_file = self.cache_dir / "compare" / f"{safe_repo}__{base_oid}__{head_oid}.json"
        if cache_file.exists():
            self.cache_hits += 1
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            return None if cached.get("_missing") else cached.get("sha")

        rc, stdout, stderr = self._run_gh(
            [
                "api",
                f"repos/{repo}/compare/{base_oid}...{head_oid}",
                "--jq",
                ".merge_base_commit.sha",
            ],
            accept_404=True,
        )
        if rc == 0:
            sha = stdout.strip()
            if re.fullmatch(r"[0-9a-fA-F]{40}", sha):
                cache_file.write_text(json.dumps({"sha": sha}), encoding="utf-8")
                return sha
            print(
                f"[warn] Unexpected merge-base SHA for {repo} {base_oid}...{head_oid}: {sha!r}",
                file=sys.stderr,
                flush=True,
            )
            return None

        err_low = (stderr + "\n" + stdout).lower()
        if rc == 404 or "422" in err_low:
            cache_file.write_text(json.dumps({"_missing": True, "rc": rc}), encoding="utf-8")
        else:
            print(
                f"[warn] compare failed for {repo} {base_oid}...{head_oid}: rc={rc} {stderr.strip()[:200]}",
                file=sys.stderr,
                flush=True,
            )
        return None


def extract_body_issue_nums(repo: str, body: str) -> list[int]:
    repo_low = repo.lower()
    nums: set[int] = set()
    for m in CLOSING_KW_RE.finditer(body or ""):
        if m.group(1):
            nums.add(int(m.group(1)))
        elif m.group(2) and m.group(3):
            if m.group(2).lower() == repo_low:
                nums.add(int(m.group(3)))
    return sorted(nums)


def select_linked_issue(
    client: GitHubClient,
    repo: str,
    pr_node: dict[str, Any],
    excluded_issues: set[tuple[str, int]],
) -> tuple[dict[str, Any] | None, bool]:
    """Return (chosen_issue, has_any_valid_before_pr_issue).

    Checks GraphQL closingIssuesReferences first (same repo, sorted by number),
    then falls back to closing keywords in PR body ("fixes #N" etc.).
    Prefers the lowest-numbered qualifying issue with body length >= 400.
    """
    pr_created = parse_iso(pr_node["createdAt"])
    repo_low = repo.lower()

    gql_issues: list[dict[str, Any]] = []
    seen_nums: set[int] = set()
    closing_nodes = ((pr_node.get("closingIssuesReferences") or {}).get("nodes")) or []
    for node in closing_nodes:
        if not node:
            continue
        node_repo = ((node.get("repository") or {}).get("nameWithOwner") or "").lower()
        if node_repo != repo_low:
            continue
        num = int(node["number"])
        if num in seen_nums:
            continue
        seen_nums.add(num)
        gql_issues.append(
            {
                "number": num,
                "title": node.get("title") or "",
                "body": node.get("body") or "",
                "createdAt": node.get("createdAt") or "",
            }
        )
    gql_issues.sort(key=lambda x: x["number"])

    qualifying: list[dict[str, Any]] = []
    for iss in gql_issues:
        if (repo_low, iss["number"]) in excluded_issues:
            continue
        if iss["createdAt"] and parse_iso(iss["createdAt"]) < pr_created:
            qualifying.append(iss)

    for iss in qualifying:
        if len(iss["body"]) >= 400:
            return iss, True

    # Fallback to "fixes #N" / "closes #N" / "resolves #N" in PR body
    body_nums = [n for n in extract_body_issue_nums(repo, pr_node.get("body") or "") if n not in seen_nums]
    for num in body_nums:
        if (repo_low, num) in excluded_issues:
            continue
        iss = client.get_issue(repo, num)
        if not iss or not iss.get("createdAt"):
            continue
        if parse_iso(iss["createdAt"]) < pr_created:
            qualifying.append(iss)
            if len(iss["body"]) >= 400:
                return iss, True

    if qualifying:
        return qualifying[0], True
    return None, False


def parse_diff_path(header_line: str) -> str:
    m = re.match(r'^diff --git "?a/(.+?)"? "?b/(.+?)"?$', header_line)
    if m:
        return m.group(2)
    parts = header_line.split()
    if len(parts) >= 4 and parts[3].startswith("b/"):
        return parts[3][2:]
    return ""


def is_test_path(path: str) -> bool:
    parts = [p.lower() for p in path.replace("\\", "/").split("/") if p]
    if not parts:
        return False
    if any(seg in ("test", "tests") for seg in parts):
        return True
    name = parts[-1]
    return (
        name == "conftest.py"
        or (name.startswith("test_") and name.endswith(".py"))
        or name.endswith("_test.py")
    )


def split_and_measure_diff(raw_diff: str) -> dict[str, Any]:
    chunks = re.split(r"(?=^diff --git )", raw_diff, flags=re.M)
    chunks = [c for c in chunks if c.startswith("diff --git ")]

    test_chunks: list[str] = []
    gold_chunks: list[str] = []
    test_files_set: set[str] = set()
    src_files_set: set[str] = set()
    src_lines = 0

    for chunk in chunks:
        lines = chunk.splitlines()
        if not lines:
            continue
        path = parse_diff_path(lines[0])
        if not path:
            continue
        if not chunk.endswith("\n"):
            chunk = chunk + "\n"
        if is_test_path(path):
            test_chunks.append(chunk)
            test_files_set.add(path)
        else:
            gold_chunks.append(chunk)
            if path.endswith(".py"):
                src_files_set.add(path)
                in_hunk = False
                for ln in lines[1:]:
                    if not in_hunk:
                        if ln.startswith("@@"):
                            in_hunk = True
                        continue
                    if ln.startswith("@@"):
                        continue
                    if ln.startswith("+") or ln.startswith("-"):
                        src_lines += 1

    return {
        "test_patch": "".join(test_chunks),
        "gold_patch": "".join(gold_chunks),
        "test_files": sorted(test_files_set),
        "src_files": sorted(src_files_set),
        "src_lines": src_lines,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Collect fresh blind candidate PRs for pool3.")
    ap.add_argument("--since", default=DEFAULT_SINCE, help="Merged-at lower bound inclusive (YYYY-MM-DD or ISO-8601 UTC)")
    ap.add_argument("--until", default=DEFAULT_UNTIL, help="Merged-at upper bound exclusive (YYYY-MM-DD or ISO-8601 UTC)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="Output JSON path")
    ap.add_argument("--sleep", type=float, default=0.25, help="Sleep seconds before each live gh call")
    args = ap.parse_args()

    since_iso = normalize_iso(args.since)
    until_iso = normalize_iso(args.until)
    if parse_iso(since_iso) >= parse_iso(until_iso):
        print(f"[error] --since ({since_iso}) must be strictly before --until ({until_iso})", file=sys.stderr)
        return 2
    ensure_git_exclude()

    recipes, excluded_prs, excluded_issues = load_recipes_and_exclusions(Path(args.out))
    repos = sorted(recipes.keys(), key=lambda s: s.lower())

    client = GitHubClient(CACHE_DIR, sleep_sec=args.sleep)

    stats = Counter()
    stats["repos_scanned"] = len(repos)
    passed_all: list[dict[str, Any]] = []

    for idx, repo in enumerate(repos, 1):
        prs = client.list_merged_prs(repo, since_iso, until_iso)
        stats["prs_seen"] += len(prs)

        for pr in prs:
            pr_num = int(pr["number"])
            if (repo.lower(), pr_num) in excluded_prs:
                continue
            if not pr.get("baseRefOid") or not pr.get("headRefOid"):
                continue
            stats["after_not_excluded"] += 1

            issue, has_issue = select_linked_issue(client, repo, pr, excluded_issues)
            if not has_issue or issue is None:
                continue
            stats["after_linked_issue_before_pr"] += 1

            issue_body = issue["body"]
            issue_body_len = len(issue_body)
            if issue_body_len < 400:
                continue
            stats["after_issue_body_len"] += 1

            raw_diff = client.get_pr_diff(repo, pr_num)
            if not raw_diff:
                continue
            stats["after_diff_fetched"] += 1

            dm = split_and_measure_diff(raw_diff)
            if not any(p.endswith(".py") for p in dm["test_files"]):
                continue
            stats["after_test_files"] += 1

            if not (1 <= len(dm["src_files"]) <= 3):
                continue
            stats["after_src_files"] += 1

            if not (10 <= dm["src_lines"] <= 120):
                continue
            stats["after_src_lines"] += 1

            merge_base = client.get_merge_base(repo, pr["baseRefOid"], pr["headRefOid"])
            if not merge_base:
                continue
            stats["after_merge_base"] += 1

            url = pr["url"]
            order_key = hashlib.sha256((ORDER_SALT + url).encode("utf-8")).hexdigest()
            recipe = recipes[repo]

            record = {
                "repo": repo,
                "pr": pr_num,
                "url": url,
                "title": pr.get("title") or "",
                "created": pr["createdAt"],
                "merged": pr["mergedAt"],
                "base": merge_base,
                "issue": int(issue["number"]),
                "issue_created": issue["createdAt"],
                "issue_title": issue["title"],
                "issue_body_len": issue_body_len,
                "src_lines": dm["src_lines"],
                "test_files": dm["test_files"],
                "src_files": dm["src_files"],
                "image": recipe["image"],
                "install_config": recipe["install_config"],
                "image_instance": recipe["image_instance"],
                "gold_patch": dm["gold_patch"],
                "test_patch": dm["test_patch"],
                "order_key": order_key,
                "problem_statement": {
                    "title": issue["title"],
                    "body": issue_body,
                },
            }
            passed_all.append(record)

        if idx % 10 == 0 or idx == len(repos):
            print(
                f"[{idx}/{len(repos)}] seen={stats['prs_seen']} "
                f"linked={stats['after_linked_issue_before_pr']} "
                f"body>=400={stats['after_issue_body_len']} "
                f"pass={stats['after_merge_base']} "
                f"(api={client.api_calls} cache={client.cache_hits})",
                file=sys.stderr,
                flush=True,
            )

    # Cap at most MAX_PER_REPO per repo (lowest order_key), then sort globally and cap at MAX_TOTAL
    by_repo: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in passed_all:
        by_repo[rec["repo"]].append(rec)

    capped: list[dict[str, Any]] = []
    for repo_recs in by_repo.values():
        repo_recs.sort(key=lambda r: r["order_key"])
        capped.extend(repo_recs[:MAX_PER_REPO])
    stats["after_repo_cap"] = len(capped)

    capped.sort(key=lambda r: r["order_key"])
    final = capped[:MAX_TOTAL]
    stats["final_count"] = len(final)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(final, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    dist = Counter(r["repo"] for r in final)
    summary = {
        "since": since_iso,
        "until": until_iso,
        "stats": dict(stats),
        "api_calls": client.api_calls,
        "cache_hits": client.cache_hits,
        "repos_in_final": len(dist),
        "distribution": dict(sorted(dist.items(), key=lambda kv: (-kv[1], kv[0].lower()))),
        "examples": [{"url": r["url"], "title": r["title"]} for r in final[:3]],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
