You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Hook-spawned mine --mode convos prints "Done." and then never exits — spun ~1 core for 38 h, holding its PID slot

A transcript mine detached by the Claude Code Stop hook finished its work (printed the full Done. summary, Drawers filed: 156) and then never exited. The process stayed alive for 38 hours, burning 45–95% of one core the whole time (~17 h of accumulated CPU), until I killed it manually. While it was alive it kept its hook_state/mine_pids/ slot, so later hook fires for that transcript were skipped.

This is related to #2172 (a live wedged hook miner is never reclaimed), but a different shape: there the orphan was idle (~0.1 s CPU) mid-mine; here the mine had completed and the hang is in process shutdown, with a busy CPU.

Environment
MemPalace 3.11.0 (pipx), Python 3.12.2 (Homebrew), chromadb 1.5.9
backend chroma, embedding model minilm, hooks.daemon off (hook spawns the miner directly via _spawn_mine)
macOS 26.3, Apple M3 Pro, 18 GB RAM
Claude Code hooks: Stop / PreCompact python -m mempalace hook run --hook … --harness claude-code
What happened
hook.log:

[13:44:58] Transcript ingest started: 6c19a8c9-….jsonl -> claudepersonal
  ...
  + [   1/1] 6c19a8c9-….jsonl         +156
=======================================================
  Done.
  Files processed: 1
  Files skipped (already filed): 0
  Drawers filed: 156
  ...
=======================================================
The file was 2.1 MB; the mine itself took about two minutes. 38 hours later the process was still running:

PID    ELAPSED      %CPU  RSS   COMMAND
32228  01-14:30:32  68.5  8896  Python -m mempalace mine …/6c19a8c9-….jsonl --mode convos --wing claudepersonal
sample 32228 showed a large number of threads, all equally hot. I did not capture a symbolicated stack before killing it, sorry. Everything after the Done. banner (hallway computation, FTS5 validation) had already printed, so the hang appears to be in interpreter shutdown: joining a non-daemon thread or an atexit handler, probably from chromadb/onnxruntime.

A plain SIGTERM stopped it immediately.

Impact
One core pegged for 38 h. Together with the re-mine cost in [#2336](https://github.com/MemPalace/mempalace/issues/2336)/#2403, the machine ran at load average 13 with fans on.
The PID slot stayed claimed, so _spawn_mine logged Skipping mine: target already running for that transcript until the process was killed.
_ingest_transcript's convos path never calls _cleanup_mine_pid_file() (only miner.mine()'s finally does), so even clean convo mines leave their slot for the stale check to reclaim. I had 10 leftover files in mine_pids/.
Suggested fix
The "bounded hook mine" item from #2172, at least for the post-completion phase. What I'm running locally, in mempalace/cli/parser.py:

    try:
        dispatch[args.command](args)
    finally:
        if args.command == "mine":
            _arm_hook_mine_exit_watchdog()


# Grace period a hook-spawned mine gets to shut down after its work is done.
_HOOK_MINE_EXIT_GRACE_SECONDS = 60


def _arm_hook_mine_exit_watchdog():
    """Force-exit a hook-spawned mine whose interpreter shutdown hangs."""
    if not os.environ.get("MEMPALACE_MINE_PID_FILE"):
        return  # manual `mempalace mine` is never force-exited
    import threading

    from ..miner import _cleanup_mine_pid_file

    def _force_exit():
        _cleanup_mine_pid_file()
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:  # noqa: BLE001 - exiting is the point
            pass
        os._exit(0)

    timer = threading.Timer(_HOOK_MINE_EXIT_GRACE_SECONDS, _force_exit)
    timer.daemon = True
    timer.start()
A daemon timer keeps running while threading._shutdown() blocks on a non-daemon thread and while atexit handlers run, so it covers both hang points. Normal exits are not delayed. I verified it with a script that leaves a non-daemon sleep(3600) thread behind: it exits after the grace period and removes its PID slot. A normal hook-style mine --dry-run still exits in about 2 s.

Open questions for a proper fix:

Should os._exit exit with a non-zero code when the mine raised?
The root cause (which thread or handler keeps the process alive) is still unknown. A faulthandler.dump_traceback_later(...) in hook-spawned mines would capture it next time.

