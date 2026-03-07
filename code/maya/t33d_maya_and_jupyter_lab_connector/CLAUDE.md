# CLAUDE.md -- maya_jupyter kernel
AI context for this project. Intended for Claude and other agents working in this codebase.

---

## What this project is

A two-process system that lets JupyterLab drive Python inside a live, full-GUI
Autodesk Maya 2025 session.  Cells typed in a Jupyter notebook are executed by
Maya's Python interpreter -- not a separate Python process -- so the full scene,
GUI, `maya.cmds`, `pymel`, and all other Maya APIs are available.

---

## Why it was built this way

### The commandPort limitation

Maya exposes a TCP server called `commandPort`.  In Python mode
(`-sourceType "python"`), it evaluates a Python expression and returns the
result.  The challenge: you can get **either** the return value **or** stdout
output (via `-echoOutput`), but not both.

Additional blocker: Maya 2025 has a `str/bytes` bug in the `-echoOutput` path
that crashes the socket handler on every response.  `-echoOutput` is therefore
completely unusable on Maya 2025.

### The chosen solution: `_jupyter_exec()` wrapper

A wrapper function installed into Maya's `__main__` namespace captures stdout
internally (via `sys.stdout = io.StringIO()`) and packages both captured output
and the expression result into a single JSON string, which becomes the
commandPort return value.

The kernel sends:
```
_jupyter_exec("<base64_encoded_code>")
```
Maya evaluates this function call, the function returns JSON, and the kernel
parses it.

Base64 encoding is used for the code payload because cell code can contain any
combination of quotes, backslashes, and newlines that would break the outer
function-call string literal if embedded directly.

### eval-then-exec execution model

Mirrors IPython:
1. Try `eval(compile(code, 'eval'))` → captures expression result for display
2. On `SyntaxError`, fall back to `exec(compile(code, 'exec'))` → for statements
3. All other exceptions caught as `BaseException` → formatted traceback in JSON

Using `BaseException` (not `Exception`) ensures `KeyboardInterrupt` and
`SystemExit` in user code are caught by the wrapper rather than propagating
into Maya's process.

### Why `__main__` as the execution namespace

Maya's commandPort evaluates expressions in `__main__`.  The Script Editor also
uses `__main__`.  Using `vars(__main__)` means variables persist between cells
naturally (just like a normal interactive Python session or Maya's own Script
Editor).

### One TCP connection per cell

Maya's commandPort is designed as stateless request-response.  Opening a fresh
TCP connection per cell is simple, reliable, and has negligible overhead for
interactive use.  No connection pooling or keep-alive is needed.

---

## File structure

```
t33d_maya_and_jupyter_lab_connector/
    CLAUDE.md                   ← this file (AI context)
    README.md                   ← human-readable setup guide
    pyproject.toml              ← package metadata and dependencies
    maya_jupyter/
        __init__.py             ← package init, version, re-exports MayaKernel
        maya_init.py            ← run INSIDE Maya: opens commandPort, installs wrapper
        kernel.py               ← Jupyter kernel process (runs OUTSIDE Maya)
        install.py              ← registers kernel spec with Jupyter
```

---

## How the two components interact

```
JupyterLab (browser)
     │
     │ ZMQ  (ipykernel handles this transparently)
     ▼
kernel.py : MayaKernel.do_execute(code)
     │
     │  1. base64-encode code
     │  2. connect TCP to Maya commandPort (maya_host:maya_port)
     │  3. send:  _jupyter_exec("<b64>")\n
     │  4. recv:  JSON until connection closes
     │  5. parse JSON → {stdout, result, error}
     │
     ├── ZMQ stream(stdout)
     ├── ZMQ execute_result(result)
     └── ZMQ error(traceback)
          │
          ▼
     JupyterLab displays output in cell
```

Maya side (`maya_init.py`, runs in Maya's Python):
```
commandPort receives: _jupyter_exec("<b64>")
     │
     ▼
_jupyter_exec():
     │  decode base64 → code string
     │  redirect sys.stdout/stderr → StringIO
     │  try eval(code) or exec(code) in __main__.__dict__
     │  catch BaseException → format traceback
     │  restore sys.stdout/stderr
     └── return json.dumps({stdout, result, error})
          │
          ▼
commandPort returns JSON string to kernel
```

---

## Key implementation decisions and gotchas

### `recv` until connection close
Maya closes the TCP connection after sending its complete reply.  The kernel
reads in a loop until `recv()` returns `b''` (connection closed).  A
`socket.timeout` between chunks is treated as end-of-reply.  There is no
explicit message framing.

### The socket timeout (`recv_timeout`, default 30s)
Applies per `recv()` call.  Long-running Maya operations (simulations, renders)
may need a higher timeout.  Set `MAYA_KERNEL_TIMEOUT=300` for render-heavy work.

### `kernel.json` is generated dynamically at install time
`install.py` writes `kernel.json` with `sys.executable` as `argv[0]`.  This
ensures the kernel process always launches with the correct Python -- important
inside virtual environments.

### Error vs. communication failure
Both user-code exceptions and network/protocol errors end up in `response['error']`.
The error message text distinguishes them:
- `[maya_jupyter]` prefix → kernel infrastructure error (connection, JSON parse)
- No prefix → Python traceback from user code

### `silent=True` mode
ipykernel calls `do_execute` with `silent=True` for internal requests
(completion, introspection).  We skip all ZMQ display messages in this case,
but still report the correct status ('ok' or 'error').

---

## Known limitations

| Limitation | Notes |
|---|---|
| No Ctrl-C / interrupt | Interrupting a running Maya cell is not implemented. The `recv_timeout` is the only safety net. Future: use `interrupt_mode: message` in kernel.json and implement `do_interrupt()`. |
| No tab completion | `do_complete()` is not implemented. Tab completion falls back to empty. Future: forward completion requests to Maya via commandPort. |
| No stdin / input() | `allow_stdin=False`. `input()` inside a cell will hang. |
| commandPort buffer limit | Maya may truncate very large commands. Unknown exact limit. ~40 KB base64 payloads (30 KB of code) seem safe in practice. |
| Single Maya instance per port | Each kernel instance connects to one port. For multiple Maya sessions, use different ports and install separate kernel specs. |
| Maya 2025 `-echoOutput` bug | Do NOT add `-echoOutput` to the `cmds.commandPort()` call. It crashes Maya's socket handler on every response. |
| Multi-statement cells don't show result | `print("a"); 1+1` shows stdout "a" but NOT result `2`. Only pure single-expression cells (eval path) return a result value. IPython does last-expression extraction even in exec mode; this kernel does not. Future: use `ast` module to split the last statement out as an expression before exec'ing the rest. |

---

## Future: rich output support

The JSON payload from `_jupyter_exec` is designed to be extended.  To add
inline plots, HTML tables, Maya viewport renders, etc.:

**Maya side (`maya_init.py`):**
1. Before executing user code, initialise a thread-local `_display_items = []`.
2. Monkey-patch `IPython.display.display()` (if available) to append
   `{"data": {mimetype: content}, "metadata": {}}` dicts to `_display_items`.
3. Add `"display_items": _display_items` to the returned JSON.

**Kernel side (`kernel.py`):**
- Uncomment the "Future rich output hook" block in `do_execute()`.
- For each item in `response.get('display_items', [])`, call:
  ```python
  self.send_response(self.iopub_socket, 'display_data', item)
  ```
- `text/plain` is already supported.  Add `text/html`, `image/png`, etc.
  by producing those MIME types on the Maya side.

---

## Dependencies

Runtime (kernel process, outside Maya):
- `ipykernel >= 6.0`     -- Kernel base class and ZMQ infrastructure
- `jupyter-client >= 7.0` -- KernelSpecManager for install.py
- Standard library only  -- `base64`, `io`, `json`, `os`, `socket`

Maya side (maya_init.py):
- Standard library only  -- `base64`, `io`, `json`, `sys`, `traceback`
- `maya.cmds`            -- already present in Maya's Python environment

---

## Testing checklist

After any change, verify:
1. Maya runs `maya_init.py` without errors; commandPort opens on 7001.
2. `python -m maya_jupyter.install` succeeds; `jupyter kernelspec list` shows `maya_jupyter`.
3. In JupyterLab:
   - `print("hello")` → output "hello", no result line.
   - `1 + 1` → result `2`, no stdout.
   - `print("a"); 1 + 1` → stdout "a", NO result `2`.  Multi-statement lines go
     through exec (not eval), so no result value is captured.  This is a known
     simplification vs IPython, which does last-expression extraction in exec mode.
     To see both, use two cells, or `print("a"); print(1 + 1)`.
   - `import maya.cmds as cmds; cmds.sphere()` → sphere in Maya viewport, no result
     (multi-statement → exec path).  Use `cmds.sphere()` alone on a line to see result.
   - `cmds.ls()` → result shown (single expression → eval path).
   - `raise ValueError("test")` → full traceback inline.
   - `x = 42` in cell 1; `x` in cell 2 → `42` (state persistence).
   - `MAYA_KERNEL_PORT=7002` env var → kernel connects to 7002.
