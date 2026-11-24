You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Log a different error when Docker is unavailable on WSL2

### Describe the bug

Below what you currently see when Docker is unavailable on WSL2.
```
(venv) user@vm-win11:~/tmp/beeware/helloworld$ briefcase run --target ubuntu

*************************************************************************
** WARNING: Unable to determine if Docker is installed                 **
*************************************************************************

    Briefcase will proceed, assuming everything is OK. If you
    experience problems, this is almost certainly the cause of those
    problems.

    Please report this as a bug at:

      https://github.com/beeware/briefcase/issues/new

    In your report, please including the output from running:

      $ docker --version

    from the command prompt.

*************************************************************************

Briefcase was unable to use Docker commands. Check your Docker
installation, and try again.

Log saved to /home/user/tmp/beeware/helloworld/logs/briefcase.2024_02_04-17_57_53.run.log
```

Unfortunately, the current logic assumes that an unavailable Docker will raise an `OSError`.

But in WSL2, it returns a `CalledProcessError` with some useful text:
```
>>> exp = None
>>> try:
...     subprocess.check_output(["docker", "--version"])
... except Exception as e:
...     exp = e
...
>>> exp
CalledProcessError(1, ['docker', '--version'])
>>> exp.stdout
b"\nThe command 'docker' could not be found in this WSL 2 distro.\nWe recommend to activate the WSL integration in Docker Desktop settings.\n\nFor details about using Docker Desktop with WSL 2, visit:\n\nhttps://docs.docker.com/go/wsl2/\n\n"
```

Same thing happens at the bash prompt:
```
(venv) user@vm-win11:~/tmp/beeware/helloworld$ docker --version

The command 'docker' could not be found in this WSL 2 distro.
We recommend to activate the WSL integration in Docker Desktop settings.

For details about using Docker Desktop with WSL 2, visit:

https://docs.docker.com/go/wsl2/
```

### Steps to reproduce

1. Ensure Docker Desktop is not running
2. Run `briefcase build --target fedora`

### Expected behavior

Error handling provides a more useful message to the user.

### Screenshots

_No response_

### Environment

- Operating System: Windows 11, WSL 2.0.14.0
- Python version: 3.8
- Software versions:
  - Briefcase: `0.3.17.dev283+g23daa64e`

### Logs

<details>
<summary>Log</summary>

```
Date/Time:       2024-02-04 18:11:52
Command line:    /home/user/tmp/beeware/venv/bin/briefcase build --target fedora

OS Release:      Linux 5.15.133.1-microsoft-standard-WSL2
OS Version:      #1 SMP Thu Oct 5 21:02:42 UTC 2023
Architecture:    x86_64
Platform:        Linux-5.15.133.1-microsoft-standard-WSL2-x86_64-with-glibc2.29

Python exe:      /home/user/tmp/beeware/venv/bin/python
Python version:  3.8.10 (default, Nov 22 2023, 10:22:35)  [GCC 9.4.0]
Virtual env:     True
Conda env:       False

Briefcase:       0.3.17.dev283+g23daa64e
Target platform: linux
Target format:   system

Environment Variables:
        DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
        DISPLAY=:0
        HOME=/home/user
        HOSTTYPE=x86_64
        LANG=C.UTF-8
        LESSCLOSE=/usr/bin/lesspipe %s %s
        LESSOPEN=| /usr/bin/lesspipe %s
        LOGNAME=user
        LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:
        NAME=vm-win11
        OLDPWD=/home/user/tmp/beeware
        PATH=/home/user/tmp/beeware/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Users/user/.pyenv/pyenv-win/shims:/mnt/c/Users/user/.pyenv/pyenv-win/versions/3.9.13:/mnt/c/Users/user/.pyenv/pyenv-win/versions/3.8.10:/mnt/c/Users/user/.pyenv/pyenv-win/versions/3.10.11:/mnt/c/Users/user/.pyenv/pyenv-win/versions/3.11.3:/mnt/c/Windows/system32:/mnt/c/Windows:/mnt/c/Windows/System32/Wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0/:/mnt/c/Windows/System32/OpenSSH/:/mnt/c/Program Files/Git/cmd:/mnt/c/Program Files/dotnet/:/mnt/c/Program Files/starship/bin/:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/c/Program Files/PowerShell/7/:/mnt/c/Users/user/.pyenv/pyenv-win/bin:/mnt/c/Users/user/.pyenv/pyenv-win/shims:/mnt/c/Users/user/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/user/.dotnet/tools:/mnt/c/Users/user/.dotnet/tools:/mnt/c/Users/user/AppData/Local/Programs/Microsoft VS Code/bin:/snap/bin
        PS1=(venv) \[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$
        PULSE_SERVER=unix:/mnt/wslg/PulseServer
        PWD=/home/user/tmp/beeware/helloworld
        SHELL=/bin/bash
        SHLVL=1
        TERM=xterm-256color
        USER=user
        VIRTUAL_ENV=/home/user/tmp/beeware/venv
        WAYLAND_DISPLAY=wayland-0
        WSL2_GUI_APPS_ENABLED=1
        WSLENV=WT_SESSION:WT_PROFILE_ID:
        WSL_DISTRO_NAME=Ubuntu-20.04
        WSL_INTEROP=/run/WSL/530_interop
        WT_PROFILE_ID={4dd1e689-b517-5f39-947d-78e8a8bdf958}
        WT_SESSION=ddc343a5-cbe6-4254-9e07-19f61b67b25a
        XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop
        XDG_RUNTIME_DIR=/run/user/1000/
        _=/home/user/tmp/beeware/venv/bin/briefcase

Briefcase Log:
[18:11:52]                                                                                                                                                         subprocess.py:720
           >>> Running Command:                                                                                                                                    subprocess.py:720
           >>>     docker --version                                                                                                                                subprocess.py:720
           >>> Working Directory:                                                                                                                                  subprocess.py:720
           >>>     /home/user/tmp/beeware/helloworld                                                                                                               subprocess.py:720
           >>> Command Output:                                                                                                                                     subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>>     The command 'docker' could not be found in this WSL 2 distro.                                                                                   subprocess.py:720
           >>>     We recommend to activate the WSL integration in Docker Desktop settings.                                                                        subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>>     For details about using Docker Desktop with WSL 2, visit:                                                                                       subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>>     https://docs.docker.com/go/wsl2/                                                                                                                subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>> Return code: 1                                                                                                                                      subprocess.py:720
                                                                                                                                                                       docker.py:183
           *************************************************************************                                                                                   docker.py:183
           ** WARNING: Unable to determine if Docker is installed                 **                                                                                   docker.py:183
           *************************************************************************                                                                                   docker.py:183
                                                                                                                                                                       docker.py:183
               Briefcase will proceed, assuming everything is OK. If you                                                                                               docker.py:183
               experience problems, this is almost certainly the cause of those                                                                                        docker.py:183
               problems.                                                                                                                                               docker.py:183
                                                                                                                                                                       docker.py:183
               Please report this as a bug at:                                                                                                                         docker.py:183
                                                                                                                                                                       docker.py:183
                 https://github.com/beeware/briefcase/issues/new                                                                                                       docker.py:183
                                                                                                                                                                       docker.py:183
               In your report, please including the output from running:                                                                                               docker.py:183
                                                                                                                                                                       docker.py:183
                 $ docker --version                                                                                                                                    docker.py:183
                                                                                                                                                                       docker.py:183
               from the command prompt.                                                                                                                                docker.py:183
                                                                                                                                                                       docker.py:183
           *************************************************************************                                                                                   docker.py:183
                                                                                                                                                                   subprocess.py:720
           >>> Running Command:                                                                                                                                    subprocess.py:720
           >>>     docker info                                                                                                                                     subprocess.py:720
           >>> Working Directory:                                                                                                                                  subprocess.py:720
           >>>     /home/user/tmp/beeware/helloworld                                                                                                               subprocess.py:720
           >>> Command Output:                                                                                                                                     subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>>     The command 'docker' could not be found in this WSL 2 distro.                                                                                   subprocess.py:720
           >>>     We recommend to activate the WSL integration in Docker Desktop settings.                                                                        subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>>     For details about using Docker Desktop with WSL 2, visit:                                                                                       subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>>     https://docs.docker.com/go/wsl2/                                                                                                                subprocess.py:720
           >>>                                                                                                                                                     subprocess.py:720
           >>> Return code: 1                                                                                                                                      subprocess.py:720
                                                                                                                                                                      __main__.py:44
           Briefcase was unable to use Docker commands. Check your Docker                                                                                             __main__.py:45
           installation, and try again.                                                                                                                               __main__.py:45

Main thread traceback:
╭─────────────────────────────────────────────────────────────────────── Traceback (most recent call last) ────────────────────────────────────────────────────────────────────────╮
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/integrations/docker.py:199 in _user_access                                                                     │
│                                                                                                                                                                                  │
│   196 │   │   │   # Invoke a docker command to check if the daemon is running,                                                                                                   │
│   197 │   │   │   # and the user has sufficient permissions.                                                                                                                     │
│   198 │   │   │   # We don't care about the output, just that it succeeds.                                                                                                       │
│ ❱ 199 │   │   │   tools.subprocess.check_output(["docker", "info"])                                                                                                              │
│   200 │   │   except subprocess.CalledProcessError as e:                                                                                                                         │
│   201 │   │   │   failure_output = e.output                                                                                                                                      │
│   202 │   │   │   if "permission denied while trying to connect" in failure_output:                                                                                              │
│                                                                                                                                                                                  │
│ ╭───────────────────────────────────────────────── locals ──────────────────────────────────────────────────╮                                                                    │
│ │            cls = <class 'briefcase.integrations.docker.Docker'>                                           │                                                                    │
│ │ failure_output = "\nThe command 'docker' could not be found in this WSL 2 distro.\nWe recommend to a"+150 │                                                                    │
│ │          tools = <briefcase.integrations.base.ToolCache object at 0x7f2092f98d00>                         │                                                                    │
│ ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯                                                                    │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/integrations/subprocess.py:123 in inner                                                                        │
│                                                                                                                                                                                  │
│   120 │   │   """                                                                                                                                                                │
│   121 │   │   # Just run the command if no dynamic elements are active                                                                                                           │
│   122 │   │   if not sub.tools.input.is_console_controlled:                                                                                                                      │
│ ❱ 123 │   │   │   return sub_method(sub, args, *wrapped_args, **wrapped_kwargs)                                                                                                  │
│   124 │   │                                                                                                                                                                      │
│   125 │   │   remove_dynamic_elements = False                                                                                                                                    │
│   126                                                                                                                                                                            │
│                                                                                                                                                                                  │
│ ╭───────────────────────────────────────── locals ─────────────────────────────────────────╮                                                                                     │
│ │           args = ['docker', 'info']                                                      │                                                                                     │
│ │            sub = <briefcase.integrations.subprocess.Subprocess object at 0x7f2092f98a90> │                                                                                     │
│ │     sub_method = <function Subprocess.check_output at 0x7f2093019280>                    │                                                                                     │
│ │   wrapped_args = ()                                                                      │                                                                                     │
│ │ wrapped_kwargs = {}                                                                      │                                                                                     │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────╯                                                                                     │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/integrations/subprocess.py:530 in check_output                                                                 │
│                                                                                                                                                                                  │
│   527 │   │   │   self._log_environment(kwargs.get("env"))                                                                                                                       │
│   528 │   │                                                                                                                                                                      │
│   529 │   │   try:                                                                                                                                                               │
│ ❱ 530 │   │   │   cmd_output = self._subprocess.check_output(                                                                                                                    │
│   531 │   │   │   │   [str(arg) for arg in args], **self.final_kwargs(**kwargs)                                                                                                  │
│   532 │   │   │   )                                                                                                                                                              │
│   533 │   │   except subprocess.CalledProcessError as e:                                                                                                                         │
│                                                                                                                                                                                  │
│ ╭───────────────────────────────────── locals ─────────────────────────────────────╮                                                                                             │
│ │   args = ['docker', 'info']                                                      │                                                                                             │
│ │ kwargs = {'stderr': -2}                                                          │                                                                                             │
│ │  quiet = False                                                                   │                                                                                             │
│ │   self = <briefcase.integrations.subprocess.Subprocess object at 0x7f2092f98a90> │                                                                                             │
│ ╰──────────────────────────────────────────────────────────────────────────────────╯                                                                                             │
│                                                                                                                                                                                  │
│ /usr/lib/python3.8/subprocess.py:415 in check_output                                                                                                                             │
│                                                                                                                                                                                  │
│    412 │   │   │   empty = b''                                                                                                                                                   │
│    413 │   │   kwargs['input'] = empty                                                                                                                                           │
│    414 │                                                                                                                                                                         │
│ ❱  415 │   return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,                                                                                                      │
│    416 │   │   │      **kwargs).stdout                                                                                                                                           │
│    417                                                                                                                                                                           │
│    418                                                                                                                                                                           │
│                                                                                                                                                                                  │
│ ╭────────────────────────────────────────── locals ───────────────────────────────────────────╮                                                                                  │
│ │    kwargs = {'stderr': -2, 'text': True, 'encoding': 'UTF-8', 'errors': 'backslashreplace'} │                                                                                  │
│ │ popenargs = (['docker', 'info'],)                                                           │                                                                                  │
│ │   timeout = None                                                                            │                                                                                  │
│ ╰─────────────────────────────────────────────────────────────────────────────────────────────╯                                                                                  │
│                                                                                                                                                                                  │
│ /usr/lib/python3.8/subprocess.py:516 in run                                                                                                                                      │
│                                                                                                                                                                                  │
│    513 │   │   │   raise                                                                                                                                                         │
│    514 │   │   retcode = process.poll()                                                                                                                                          │
│    515 │   │   if check and retcode:                                                                                                                                             │
│ ❱  516 │   │   │   raise CalledProcessError(retcode, process.args,                                                                                                               │
│    517 │   │   │   │   │   │   │   │   │    output=stdout, stderr=stderr)                                                                                                        │
│    518 │   return CompletedProcess(process.args, retcode, stdout, stderr)                                                                                                        │
│    519                                                                                                                                                                           │
│                                                                                                                                                                                  │
│ ╭──────────────────────────────────────────────────── locals ────────────────────────────────────────────────────╮                                                               │
│ │ capture_output = False                                                                                         │                                                               │
│ │          check = True                                                                                          │                                                               │
│ │          input = None                                                                                          │                                                               │
│ │         kwargs = {'stdout': -1, 'stderr': -2, 'text': True, 'encoding': 'UTF-8', 'errors': 'backslashreplace'} │                                                               │
│ │      popenargs = (['docker', 'info'],)                                                                         │                                                               │
│ │        process = <subprocess.Popen object at 0x7f2092ea3cd0>                                                   │                                                               │
│ │        retcode = 1                                                                                             │                                                               │
│ │         stderr = None                                                                                          │                                                               │
│ │         stdout = "\nThe command 'docker' could not be found in this WSL 2 distro.\nWe recommend to a"+150      │                                                               │
│ │        timeout = None                                                                                          │                                                               │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
CalledProcessError: Command '['docker', 'info']' returned non-zero exit status 1.

The above exception was the direct cause of the following exception:

╭─────────────────────────────────────────────────────────────────────── Traceback (most recent call last) ────────────────────────────────────────────────────────────────────────╮
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/__main__.py:29 in main                                                                                         │
│                                                                                                                                                                                  │
│   26 │   │   │   Path.cwd() / "pyproject.toml",                                                                                                                                  │
│   27 │   │   │   overrides=overrides,                                                                                                                                            │
│   28 │   │   )                                                                                                                                                                   │
│ ❱ 29 │   │   command(**options)                                                                                                                                                  │
│   30 │   except HelpText as e:                                                                                                                                                   │
│   31 │   │   logger.info()                                                                                                                                                       │
│   32 │   │   logger.info(str(e))                                                                                                                                                 │
│                                                                                                                                                                                  │
│ ╭────────────────────────────────────────────────────────────────────────── locals ───────────────────────────────────────────────────────────────────────────╮                  │
│ │       command = <briefcase.platforms.linux.system.LinuxSystemBuildCommand object at 0x7f2092ef90a0>                                                         │                  │
│ │       Command = <class 'briefcase.platforms.linux.system.LinuxSystemBuildCommand'>                                                                          │                  │
│ │       console = <briefcase.console.Console object at 0x7f20941e81c0>                                                                                        │                  │
│ │             e = BriefcaseCommandError('Briefcase was unable to use Docker commands. Check your Docker\ninstallation, and try again.\n')                     │                  │
│ │ extra_cmdline = ['--target', 'fedora']                                                                                                                      │                  │
│ │        logger = <briefcase.console.Log object at 0x7f20941e8e20>                                                                                            │                  │
│ │       options = {'update': False, 'update_requirements': False, 'update_support': False, 'update_resources': False, 'no_update': False, 'test_mode': False} │                  │
│ │     overrides = {}                                                                                                                                          │                  │
│ │       printer = <briefcase.console.Printer object at 0x7f20944e3250>                                                                                        │                  │
│ │        result = 200                                                                                                                                         │                  │
│ ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯                  │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/commands/build.py:115 in __call__                                                                              │
│                                                                                                                                                                                  │
│   112 │   │                                                                                                                                                                      │
│   113 │   │   # Confirm host compatibility, that all required tools are available,                                                                                               │
│   114 │   │   # and that the app configuration is finalized.                                                                                                                     │
│ ❱ 115 │   │   self.finalize(app)                                                                                                                                                 │
│   116 │   │                                                                                                                                                                      │
│   117 │   │   if app:                                                                                                                                                            │
│   118 │   │   │   state = self._build_app(                                                                                                                                       │
│                                                                                                                                                                                  │
│ ╭───────────────────────────────────────────────── locals ──────────────────────────────────────────────────╮                                                                    │
│ │                 app = None                                                                                │                                                                    │
│ │           no_update = False                                                                               │                                                                    │
│ │             options = {}                                                                                  │                                                                    │
│ │                self = <briefcase.platforms.linux.system.LinuxSystemBuildCommand object at 0x7f2092ef90a0> │                                                                    │
│ │           test_mode = False                                                                               │                                                                    │
│ │              update = False                                                                               │                                                                    │
│ │ update_requirements = False                                                                               │                                                                    │
│ │    update_resources = False                                                                               │                                                                    │
│ │      update_support = False                                                                               │                                                                    │
│ ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯                                                                    │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/commands/base.py:578 in finalize                                                                               │
│                                                                                                                                                                                  │
│   575 │   │   │   to finalize. By default, all apps will be finalized.                                                                                                           │
│   576 │   │   """                                                                                                                                                                │
│   577 │   │   self.verify_host()                                                                                                                                                 │
│ ❱ 578 │   │   self.verify_tools()                                                                                                                                                │
│   579 │   │                                                                                                                                                                      │
│   580 │   │   if app is None:                                                                                                                                                    │
│   581 │   │   │   for app in self.apps.values():                                                                                                                                 │
│                                                                                                                                                                                  │
│ ╭────────────────────────────────────────── locals ──────────────────────────────────────────╮                                                                                   │
│ │  app = None                                                                                │                                                                                   │
│ │ self = <briefcase.platforms.linux.system.LinuxSystemBuildCommand object at 0x7f2092ef90a0> │                                                                                   │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────╯                                                                                   │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/platforms/linux/system.py:374 in verify_tools                                                                  │
│                                                                                                                                                                                  │
│    371 │   │   """If we're using Docker, verify that it is available."""                                                                                                         │
│    372 │   │   super().verify_tools()                                                                                                                                            │
│    373 │   │   if self.use_docker:                                                                                                                                               │
│ ❱  374 │   │   │   Docker.verify(tools=self.tools, image_tag=self.target_image)                                                                                                  │
│    375 │                                                                                                                                                                         │
│    376 │   def clone_options(self, command):                                                                                                                                     │
│    377 │   │   """Clone the target_image option."""                                                                                                                              │
│                                                                                                                                                                                  │
│ ╭────────────────────────────────────────── locals ──────────────────────────────────────────╮                                                                                   │
│ │ self = <briefcase.platforms.linux.system.LinuxSystemBuildCommand object at 0x7f2092ef90a0> │                                                                                   │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────╯                                                                                   │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/integrations/base.py:77 in verify                                                                              │
│                                                                                                                                                                                  │
│    74 │   ) -> ToolT:                                                                          ╭───────────────────────────────── locals ──────────────────────────────────╮     │
│    75 │   │   """Confirm the tool is available and usable on the host platform."""             │    app = None                                                             │     │
│    76 │   │   cls.verify_host(tools=tools)                                                     │    cls = <class 'briefcase.integrations.docker.Docker'>                   │     │
│ ❱  77 │   │   tool = cls.verify_install(tools=tools, app=app, **kwargs)                        │ kwargs = {'image_tag': 'fedora'}                                          │     │
│    78 │   │   return tool                                                                      │  tools = <briefcase.integrations.base.ToolCache object at 0x7f2092f98d00> │     │
│    79 │                                                                                        ╰───────────────────────────────────────────────────────────────────────────╯     │
│    80 │   @classmethod                                                                                                                                                           │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/integrations/docker.py:153 in verify_install                                                                   │
│                                                                                                                                                                                  │
│   150 │   │   │   return tools.docker                                                          ╭─────────────────────────────────── locals ───────────────────────────────────╮  │
│   151 │   │                                                                                    │       cls = <class 'briefcase.integrations.docker.Docker'>                   │  │
│   152 │   │   cls._version_compat(tools=tools)                                                 │ image_tag = 'fedora'                                                         │  │
│ ❱ 153 │   │   cls._user_access(tools=tools)                                                    │    kwargs = {'app': None}                                                    │  │
│   154 │   │   cls._buildx_installed(tools=tools)                                               │     tools = <briefcase.integrations.base.ToolCache object at 0x7f2092f98d00> │  │
│   155 │   │                                                                                    ╰──────────────────────────────────────────────────────────────────────────────╯  │
│   156 │   │   tools.docker = Docker(tools=tools, image_tag=image_tag)                                                                                                            │
│                                                                                                                                                                                  │
│ /home/user/tmp/beeware/venv/lib/python3.8/site-packages/briefcase/integrations/docker.py:212 in _user_access                                                                     │
│                                                                                                                                                                                  │
│   209 │   │   │   ):                                                                                                                                                             │
│   210 │   │   │   │   raise BriefcaseCommandError(cls.DAEMON_NOT_RUNNING_ERROR) from e                                                                                           │
│   211 │   │   │   else:                                                                                                                                                          │
│ ❱ 212 │   │   │   │   raise BriefcaseCommandError(cls.GENERIC_DOCKER_ERROR) from e                                                                                               │
│   213 │                                                                                                                                                                          │
│   214 │   @classmethod                                                                                                                                                           │
│   215 │   def _buildx_installed(cls, tools: ToolCache):                                                                                                                          │
│                                                                                                                                                                                  │
│ ╭───────────────────────────────────────────────── locals ──────────────────────────────────────────────────╮                                                                    │
│ │            cls = <class 'briefcase.integrations.docker.Docker'>                                           │                                                                    │
│ │ failure_output = "\nThe command 'docker' could not be found in this WSL 2 distro.\nWe recommend to a"+150 │                                                                    │
│ │          tools = <briefcase.integrations.base.ToolCache object at 0x7f2092f98d00>                         │                                                                    │
│ ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
BriefcaseCommandError: Briefcase was unable to use Docker commands. Check your Docker
installation, and try again.
```

</details>

### Additional context

_No response_
