You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: v2.3.0b2 在受限环境(fnOS 应用沙箱)启动即崩:dependency_maintenance 锁根目录优先按 pwd home 推导,绕过了 $HOME,且覆盖变量 QWENPAW_DEPENDENCY_STATE_DIR 未在文档中说明

## QwenPaw Version

2.3.0b2(PyPI wheel)

## Description

在受限部署环境(飞牛 fnOS NAS 应用沙箱)中,`pip install qwenpaw==2.3.0b2` 后以专用应用用户运行 `python3 -m qwenpaw app`,**import 阶段即崩溃**,进程无法启动。

根因:`qwenpaw/plugins/dependency_maintenance.py` 的 `state_root()` 在解析依赖托管锁根目录时,**优先取 `pwd.getpwuid(os.getuid()).pw_dir`(passwd 数据库的 home),而不是 `os.environ["HOME"]`**。fnOS 这类托管环境会为应用创建专用用户(passwd 中 home 为 `/home/<appuser>`),但该目录实际不存在且 `/home` 对应用用户不可写,于是 `_open_lock()` 内的 `Path(...).mkdir(parents=True)` 抛出 `PermissionError: [Errno 13] Permission denied: '/home/qwenpaw'`,发生在 `qwenpaw/__init__.py` 的 import 期,进程必然退出。

代码中其实已提供覆盖变量 **`QWENPAW_DEPENDENCY_STATE_DIR`**(优先级最高),实测设置后可正常启动——但该变量未在任何文档中出现,受限环境的用户无从得知。

建议(任选或组合):
1. 解析顺序改为 `QWENPAW_DEPENDENCY_STATE_DIR` → `$HOME` → `pwd.pw_dir`(与多数工具一致,pw_dir 在托管环境往往是错的);
2. `state_root()` 失败时给出可操作的错误信息,指明可设置 `QWENPAW_DEPENDENCY_STATE_DIR`;
3. 在文档中说明该变量。

**Related PR(s):** 无

**Security considerations:** 无(仅涉及部署环境下的路径与权限)

## Component(s) Affected

- [x] Core / Backend (app, agents, config, providers, utils, local_models)
- [ ] Console (frontend web UI)
- [ ] Channels (DingTalk, Feishu, QQ, Discord, iMessage, etc.)
- [ ] Skills
- [x] CLI
- [ ] Documentation (website)
- [ ] Tests
- [ ] CI/CD
- [ ] Scripts / Deploy

## Environment

- **QwenPaw version:** 2.3.0b2
- **OS:** 飞牛 fnOS 1.x(Debian 系 NAS 系统)
- **Install method:** pip(从 PyPI 镜像安装到专用 venv)
- **Python version:** 3.12(fnOS python312 依赖应用)

## Steps to Reproduce

1. 创建专用用户且不创建其 home 目录,例如 `useradd -M qwenpaw`(`/home` 为 root 所有,应用用户不可写)
2. 以该用户运行 venv 中的内核:`python3 -m qwenpaw app --host 0.0.0.0 --port 18088`
3. import 阶段立即崩溃

注:同类环境的 b1(2.3.0b1)不受影响——b2 才在 `qwenpaw/__init__.py` 引入了 import 期的 `lease_environment` 调用。

## Actual vs Expected

- **Actual:** `PermissionError: [Errno 13] Permission denied: '/home/qwenpaw'`,启动即崩,且错误信息未指向任何可操作的解决方案
- **Expected:** 尊重 `$HOME`(或至少在 pw_dir 不可用时回退),或给出指向 `QWENPAW_DEPENDENCY_STATE_DIR` 的清晰错误

## Logs / Screenshots

```
Traceback (most recent call last):
  File "<frozen runpy>", line 189, in _run_module_as_main
  File "/vol2/@apphome/qwenpaw/venv/lib/python3.12/site-packages/qwenpaw/__init__.py", line 11, in <module>
    _environment_custody.lease_environment(_environment_custody.host_sites())
  File ".../qwenpaw/plugins/dependency_maintenance.py", line 386, in lease_environment
    _lease_environment(sites, parent_pid, timeout)
  File ".../qwenpaw/plugins/dependency_maintenance.py", line 421, in _lease_environment
    with admission():
  File ".../qwenpaw/plugins/dependency_maintenance.py", line 414, in admission
    with file_lock(
  File ".../qwenpaw/plugins/dependency_maintenance.py", line 323, in file_lock
    descriptor = open_coordination_lock(path)
  File ".../qwenpaw/plugins/dependency_maintenance.py", line 310, in _open_lock
PermissionError: [Errno 13] Permission denied: '/home/qwenpaw'
```

相关代码(`state_root()` 解析顺序,`dependency_maintenance.py` 约 205-230 行):`QWENPAW_DEPENDENCY_STATE_DIR` 覆盖 → `pwd.getpwuid(os.getuid()).pw_dir` → `$HOME` → 报错。问题在于 pw_dir 的优先级高于 `$HOME`,且失败信息未提示覆盖变量。

## Additional Notes

- 已验证的 workaround:`export QWENPAW_DEPENDENCY_STATE_DIR=<可写的绝对路径>`(我们指向应用数据区),设置后 b2 可正常启动并运行。建议将此变量写入文档。
- 部署背景:我们是 QwenPaw 的飞牛 fnOS 第三方打包维护方([QwenPaw for fnOS](https://github.com/yaozy2020/QwenPaw-for-fnOS)),b2 的依赖托管子进程机制我们在打包层已配合进程组保底;锁路径问题修复后我们会跟进升级测试。
