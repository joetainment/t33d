"""
maya_jupyter/maya_init.py
=========================
Run this script ONCE inside Autodesk Maya's Script Editor (Python tab) to
prepare Maya for Jupyter kernel connections.

What it does
------------
1. Installs the ``_jupyter_exec()`` wrapper function into Maya's __main__
   namespace so that it is callable from the commandPort socket.
2. Opens Maya's commandPort (a TCP server) on JUPYTER_PORT so that the
   external Jupyter kernel process can send code to this Maya instance.

How to run in Maya
------------------
Option A — paste into Script Editor and hit Execute:
    Just open this file, copy the contents, paste into Maya's Python tab, run.

Option B — exec from the Script Editor (Maya 2025 is Python 3; execfile is Python 2 only):
    exec(open(r"T:/t33d/t33d/code/maya/t33d_maya_and_jupyter_lab_connector/maya_jupyter/maya_init.py").read())

Option C — add to userSetup.py so it runs every time Maya starts:
    exec(open(r"<path_to_maya_init.py>").read())

Configuration
-------------
Change JUPYTER_PORT below if port 7001 is in use (e.g., for multiple Maya
instances).  The Jupyter kernel must be told the same port via the
MAYA_KERNEL_PORT environment variable or --MayaKernel.maya_port flag.


The commandPort limitation and why _jupyter_exec() exists
----------------------------------------------------------
Maya's commandPort (TCP) in Python mode (-sourceType "python") evaluates a
Python expression and returns its value as a string.  It can do ONE of:

  A) Return the string value of the last expression  (default behaviour)
  B) Echo stdout/stderr back over the socket         (-echoOutput flag)

But NOT both simultaneously.  Worse, Maya 2025 has a str/bytes type bug that
crashes the socket handler every single time -echoOutput sends a response,
making option B completely broken in Maya 2025.

The fix: a wrapper function that captures stdout/stderr internally
------------------------------------------------------------------
_jupyter_exec(code_b64) does the following inside Maya:

  1. Saves sys.stdout and sys.stderr.
  2. Replaces them with a StringIO buffer (capturing all print() output).
  3. Executes the user's code (eval-then-exec pattern, mirroring IPython).
  4. Restores sys.stdout and sys.stderr.
  5. Returns a JSON string: {"stdout": "...", "result": "...", "error": "..."}

The JSON string is the function's return value, which commandPort sends back
to the kernel as its response.  No -echoOutput needed.  Both print output and
expression results arrive in a single, structured response.

Execution model (eval-then-exec, like IPython)
----------------------------------------------
- Try ``eval(compile(code, 'eval'))`` first.
  Works for expressions: ``cmds.ls()``, ``x + 1``, ``[i for i in range(5)]``
  The expression value is captured and returned in the "result" field.

- On SyntaxError, fall back to ``exec(compile(code, 'exec'))``.
  Works for statements: ``x = 1``, ``def f(): ...``, ``import maya.cmds``
  No return value (result=None), but print() output is captured.

- Any other exception is caught and returned in the "error" field as a full
  formatted traceback string.

Namespace persistence
---------------------
All code is executed in ``__main__.__dict__``, so variables and imports
persist across Jupyter cells exactly like a normal Python interactive session
or Maya's own Script Editor.
"""

import sys
import io
import json
import base64
import traceback as _traceback
import __main__

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

JUPYTER_PORT = 7001  # Change this if you need a different port.
                     # Match with MAYA_KERNEL_PORT on the kernel side.

# ---------------------------------------------------------------------------
# Guard: this script must be executed inside Autodesk Maya
# ---------------------------------------------------------------------------

try:
    import maya.cmds as cmds
except ImportError:
    raise RuntimeError(
        "maya_init.py must be run inside Autodesk Maya's Script Editor, "
        "not as a standalone Python script outside of Maya."
    )


# ---------------------------------------------------------------------------
# The core wrapper — installed into __main__ so it is callable from the socket
# ---------------------------------------------------------------------------

def _jupyter_exec(code_b64: str) -> str:
    """
    Execute base64-encoded Python code in Maya's __main__ namespace.

    This function is called by the external Jupyter kernel process.  The
    kernel sends the expression ``_jupyter_exec("<base64>")`` over the TCP
    commandPort; Maya evaluates it, calls this function, and returns the
    resulting JSON string as the commandPort response.

    Parameters
    ----------
    code_b64 : str
        The user's cell code, base64-encoded as ASCII.
        Base64 encoding is used because the code may contain any mix of
        single quotes, double quotes, backslashes, and newlines — all of
        which would break the outer ``_jupyter_exec("...")`` call if the
        code were embedded as a raw string literal.

    Returns
    -------
    str
        JSON string with the following keys:

        "stdout"  : str        -- everything written to stdout / stderr
                                  during the cell's execution.
        "result"  : str | null -- repr() of the expression's return value,
                                  or null for statements / None results.
        "error"   : str | null -- full formatted traceback if an exception
                                  was raised, or null on success.

    Notes on future rich-output support
    ------------------------------------
    To support rich output (matplotlib plots, HTML tables, etc.) later, add
    a "display_items" list to the returned JSON.  Each item should be a dict
    with "data" (mime-type → content mapping) and "metadata" keys, matching
    Jupyter's display_data message format.

    The kernel (kernel.py) already has a commented-out hook in do_execute()
    that iterates over "display_items" and sends display_data ZMQ messages.
    On the Maya side, monkey-patch IPython.display.display() (if available)
    to append items to a local list, then include that list in the JSON.
    """

    # --- Decode the cell code from base64 -----------------------------------
    try:
        code = base64.b64decode(code_b64.encode('ascii')).decode('utf-8')
    except Exception as exc:
        return json.dumps({
            'stdout': '',
            'result': None,
            'error':  f'[maya_jupyter] Failed to base64-decode cell code: {exc}',
        })

    # --- Redirect stdout and stderr to capture all print() output -----------
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    capture    = io.StringIO()
    sys.stdout = capture
    sys.stderr = capture

    result = None
    error  = None

    try:
        # --- eval path: single expressions (value is displayed in Jupyter) --
        # compile() with mode='eval' raises SyntaxError for statements,
        # so we use that as the branch condition rather than guessing.
        try:
            result = eval(
                compile(code, '<jupyter-cell>', 'eval'),
                vars(__main__)
            )
        except SyntaxError:
            # --- exec path: statements, multi-line blocks, definitions -------
            exec(  # noqa: S102
                compile(code, '<jupyter-cell>', 'exec'),
                vars(__main__)
            )

    except BaseException:
        # Catch everything — including KeyboardInterrupt and SystemExit — so
        # that exceptions in user code never propagate up into Maya itself and
        # potentially destabilise the session.
        error = _traceback.format_exc()

    finally:
        # Always restore stdout/stderr, even if something went horribly wrong.
        captured_output = capture.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return json.dumps({
        'stdout': captured_output,
        # Don't emit None as a result — matches Python REPL / IPython behaviour
        # where ``x = 5`` shows nothing, but ``x`` shows ``5``.
        'result': repr(result) if result is not None else None,
        'error':  error,
    })


# ---------------------------------------------------------------------------
# Open the commandPort and register the wrapper
# ---------------------------------------------------------------------------

def setup_jupyter_connection(port: int = JUPYTER_PORT) -> None:
    """
    Open Maya's commandPort on ``port`` and install ``_jupyter_exec`` into
    __main__ so it is reachable when the kernel sends a command.

    Safe to call multiple times — the old port is closed and reopened.

    Parameters
    ----------
    port : int
        TCP port to listen on.  Must match MAYA_KERNEL_PORT on the kernel side.
    """
    port_name = f':{port}'

    # Close any pre-existing commandPort on this port (idempotent).
    # cmds.commandPort raises if no port is open, so we swallow the exception.
    try:
        cmds.commandPort(port_name, close=True)
        print(f'[maya_jupyter] Closed previous commandPort on {port_name}')
    except Exception:
        pass  # Nothing was open — that's fine.

    # Install the wrapper function into __main__ so the commandPort evaluator
    # can find it.  Maya's commandPort (-sourceType python) evaluates
    # expressions in __main__'s namespace, so assigning here is all we need.
    __main__._jupyter_exec = _jupyter_exec

    # Open the port in Python mode.
    # !! Do NOT add -echoOutput !!
    # Maya 2025 has a str/bytes bug that crashes the socket handler on every
    # response when -echoOutput is active.  Our wrapper captures output
    # internally via StringIO, so -echoOutput is not needed.
    cmds.commandPort(name=port_name, sourceType='python')

    print(f'[maya_jupyter] commandPort opened   : {port_name}')
    print(f'[maya_jupyter] _jupyter_exec ready  : __main__._jupyter_exec')
    print(f'[maya_jupyter] Waiting for Jupyter kernel connections...')


# Run immediately when this file is executed in Maya's Script Editor.
setup_jupyter_connection(JUPYTER_PORT)
