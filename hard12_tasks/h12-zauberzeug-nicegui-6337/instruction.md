You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

NICEGUI_PORT deeply engrained into LLM training data but doesn't actually work

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
NICEGUI_PORT=8113 nohup uv run python src/main.py
```

### Description

On first attempt of trying to launch a NiceGUI server, LLMs always try to set `NICEGUI_PORT`, which doesn't work. It still is on 8080. 

<img width="1432" height="244" alt="Image" src="https://github.com/user-attachments/assets/9c43d717-f71f-4f11-bf95-223c580ed333" />

Is because, we set that environment variable only for our internal use, of course it doesn't work, but this NICEGUI_PORT is so stuck in LLM's training dataset that it always tries this the first thing. 

<img width="1099" height="440" alt="Image" src="https://github.com/user-attachments/assets/a4c9d0e9-1e1d-4bf4-a607-44ee77571615" />

It is a common pattern after all. Note the model being tested (Sonnet 5 w/o internet) cannot reliably remember that it is NOT a settable env. 

<img width="583" height="693" alt="Image" src="https://github.com/user-attachments/assets/81c25daf-2d76-4ac3-ba61-e4a7ff0ca9e9" />



### NiceGUI Version

3.16.0

### Python Version

3.14.2

### Browser

Chrome

### Operating System

macOS

### Additional Context

Two solution:

- Log-warn if set, saying it won't work
- Be forced by an LLM to add a feature (actually not unreasonable)*

*you'd want to be able to adjust the port which something runs, without editing the source code. In this case `NICEGUI_PORT` should win over the `port` param. 
