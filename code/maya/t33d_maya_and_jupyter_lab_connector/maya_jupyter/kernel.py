"""
maya_jupyter/kernel.py
======================
The Jupyter kernel process that bridges JupyterLab and Autodesk Maya 2025.

This process runs OUTSIDE Maya.  JupyterLab talks to it over ZMQ sockets
(handled transparently by the ipykernel framework).  This kernel talks to
Maya over a plain TCP socket via Maya's commandPort.

Architecture / data flow
------------------------

  JupyterLab (browser)
       │
       │  ZMQ (execute_request)
       ▼
  MayaKernel.do_execute()           ← this file
       │
       │  1. base64-encode cell code
       │  2. open TCP socket → Maya commandPort
       │  3. send:  _jupyter_exec("<b64_code>")\n
       │  4. recv:  JSON string until connection closes
       │  5. parse JSON
       │
       ├──► ZMQ stream          (stdout/stderr text)
       ├──► ZMQ execute_result  (expression repr value)
       └──► ZMQ error           (traceback on exception)
            │
            ▼
       JupyterLab displays output in cell

Why one TCP connection per cell?
---------------------------------
Maya's commandPort is designed as a stateless request-response server.
Opening a fresh connection per cell is simple, reliable, and matches
the commandPort's design.  The overhead is negligible for interactive use.

Configuration
-------------
Maya host/port can be set three ways (highest priority first):

  1. Environment variables:
       MAYA_KERNEL_HOST   (default: 127.0.0.1)
       MAYA_KERNEL_PORT   (default: 7001)
       MAYA_KERNEL_TIMEOUT (default: 30 seconds)

  2. Traitlet config flags passed to the kernel launch command:
       --MayaKernel.maya_host=192.168.1.5
       --MayaKernel.maya_port=7002

  3. Built-in defaults (127.0.0.1:7001).

For multiple simultaneous Maya instances, run maya_init.py in each with
a different JUPYTER_PORT, then create a separate kernel.json per instance
(or launch kernels with different MAYA_KERNEL_PORT env vars).

Extending for rich output (future work)
----------------------------------------
The JSON payload returned by _jupyter_exec() is designed to be extended.
To add rich output support (matplotlib plots, HTML tables, Maya viewport
renders, etc.):

  Maya side (maya_init.py):
    - Monkey-patch IPython.display.display() (if available) to append items
      to a thread-local ``_display_items`` list during cell execution.
    - Include ``"display_items": [...]`` in the returned JSON, where each
      item is {"data": {<mimetype>: <content>}, "metadata": {}}.

  Kernel side (this file):
    - Uncomment the "Future rich output hook" block in do_execute().
    - For each item in response.get('display_items', []):
        self.send_response(self.iopub_socket, 'display_data', item)
    - text/plain is already supported; add text/html, image/png, etc. as
      needed by extending the 'data' dict on the Maya side.
"""

import base64
import json
import os
import socket

from ipykernel.kernelbase import Kernel
from traitlets import Int, Unicode


# ---------------------------------------------------------------------------
# Helper: parse a Python traceback string into (ename, evalue)
# ---------------------------------------------------------------------------

def _parse_exception(tb_text: str) -> tuple:
    """
    Extract the exception class name and message from a formatted traceback.

    Python tracebacks end with a line like:
        ValueError: the message here
    or just:
        StopIteration

    We walk backwards through the lines looking for the first non-indented,
    non-'Traceback' line, which is the exception summary.

    Returns
    -------
    tuple[str, str]
        (ename, evalue) suitable for Jupyter's 'error' message format.
        Falls back to ('Error', tb_text) if nothing parseable is found.
    """
    for line in reversed(tb_text.splitlines()):
        line = line.strip()
        if not line:
            continue
        if line.startswith('Traceback'):
            continue
        # Lines that start with spaces are part of the stack frames — skip.
        # The exception summary line is flush left.
        if line[0] == ' ':
            continue
        if ': ' in line:
            parts = line.split(': ', 1)
            return parts[0].strip(), parts[1].strip()
        return line, ''
    return 'Error', tb_text


# ---------------------------------------------------------------------------
# Kernel
# ---------------------------------------------------------------------------

class MayaKernel(Kernel):
    """
    A Jupyter kernel that executes code in a running Autodesk Maya 2025.

    Prerequisite: run maya_init.py inside Maya's Script Editor first.
    That opens the commandPort and installs the _jupyter_exec() wrapper.
    """

    # ---- Jupyter kernel metadata -------------------------------------------
    # These strings appear in the kernel picker and in notebook metadata.

    implementation         = 'maya_jupyter'
    implementation_version = '0.1.0'
    language               = 'python'
    language_version       = '3.x'   # Maya 2025 ships Python 3.11
    language_info          = {
        'name':            'python',
        'mimetype':        'text/x-python',
        'file_extension':  '.py',
        # CodeMirror / Pygments mode so the editor syntax-highlights Python:
        'codemirror_mode': {'name': 'ipython', 'version': 3},
        'pygments_lexer':  'ipython3',
    }
    banner = 'Maya 2025 Python Kernel  |  t33d_maya_and_jupyter_lab_connector'

    # ---- Configurable connection settings (overridable via env / CLI) -------

    maya_host = Unicode(
        '127.0.0.1',
        help=(
            'Hostname or IP address of the machine running Maya. '
            'Override with the MAYA_KERNEL_HOST environment variable.'
        ),
    ).tag(config=True)

    maya_port = Int(
        7001,
        help=(
            'TCP port that Maya\'s commandPort is listening on. '
            'Must match JUPYTER_PORT in maya_init.py. '
            'Override with the MAYA_KERNEL_PORT environment variable.'
        ),
    ).tag(config=True)

    recv_timeout = Int(
        30,
        help=(
            'Seconds to wait for a response from Maya before giving up. '
            'Increase this for cells that drive long-running Maya operations '
            '(simulations, renders, heavy loops). '
            'Override with the MAYA_KERNEL_TIMEOUT environment variable.'
        ),
    ).tag(config=True)

    # ------------------------------------------------------------------------

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Environment variable overrides let users set the connection details
        # in shell profiles or launch scripts without editing kernel.json.
        host    = os.environ.get('MAYA_KERNEL_HOST')
        port    = os.environ.get('MAYA_KERNEL_PORT')
        timeout = os.environ.get('MAYA_KERNEL_TIMEOUT')
        if host:
            self.maya_host = host
        if port:
            self.maya_port = int(port)
        if timeout:
            self.recv_timeout = int(timeout)

    # -------------------------------------------------------------------------
    # Internal: TCP communication with Maya
    # -------------------------------------------------------------------------

    def _send_to_maya(self, code: str) -> dict:
        """
        Send ``code`` to Maya via the commandPort and return the parsed JSON.

        Protocol
        --------
        1. Base64-encode the code (handles any mix of quotes/backslashes/
           newlines inside the cell without breaking the outer function call).
        2. Build the command string:  ``_jupyter_exec("<b64>")\n``
           This is a valid Python expression that Maya evaluates.  Maya calls
           our wrapper, which returns a JSON string; commandPort returns that
           JSON string as its reply.
        3. Open a TCP connection, send the command, read until the connection
           closes (Maya closes it after sending its reply), then parse JSON.

        Error handling
        --------------
        Communication failures (connection refused, timeout, bad JSON) are
        caught here and returned as synthetic error dicts so do_execute()
        always gets a consistent dict with 'stdout', 'result', 'error' keys.
        User-code exceptions are handled inside Maya and arrive in the normal
        'error' field of the JSON — they don't cause exceptions here.

        Notes on commandPort buffer limits
        -----------------------------------
        Maya's commandPort may have an undocumented maximum message size.
        Very large cells (tens of KB of source code) could potentially be
        truncated.  In practice this is rarely an issue for interactive work.
        Base64 encoding inflates size by ~33%, so a 30 KB cell becomes ~40 KB.
        If truncation occurs, split the cell into smaller pieces.
        """
        code_b64 = base64.b64encode(code.encode('utf-8')).decode('ascii')
        command  = f'_jupyter_exec("{code_b64}")\n'

        raw = b''
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.recv_timeout)
                sock.connect((self.maya_host, self.maya_port))
                sock.sendall(command.encode('utf-8'))

                # Read response chunks until the connection closes.
                # Maya closes the connection after sending its complete reply,
                # so recv() returning b'' signals end-of-response.
                # socket.timeout between chunks means Maya is slow or hung.
                chunks = []
                while True:
                    try:
                        chunk = sock.recv(4096)
                    except socket.timeout:
                        # Nothing received within recv_timeout — give up and
                        # work with whatever we have (might be partial).
                        break
                    if not chunk:
                        break   # Connection closed — normal end of reply.
                    chunks.append(chunk)

                raw = b''.join(chunks)

        except ConnectionRefusedError:
            return {
                'stdout': '',
                'result': None,
                'error': (
                    f'[maya_jupyter] Connection refused at '
                    f'{self.maya_host}:{self.maya_port}.\n'
                    f'Make sure Maya is running and that you have executed '
                    f'maya_init.py in Maya\'s Script Editor.'
                ),
            }
        except OSError as exc:
            return {
                'stdout': '',
                'result': None,
                'error': f'[maya_jupyter] Socket error: {type(exc).__name__}: {exc}',
            }

        # Decode response bytes.
        raw_text = raw.decode('utf-8', errors='replace').strip()

        if not raw_text:
            return {
                'stdout': '',
                'result': None,
                'error': (
                    '[maya_jupyter] Maya returned an empty response.\n'
                    'This usually means _jupyter_exec() is not installed — '
                    'run maya_init.py inside Maya first.'
                ),
            }

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            return {
                'stdout': '',
                'result': None,
                'error': (
                    f'[maya_jupyter] Could not parse Maya response as JSON: {exc}\n'
                    f'Raw response ({len(raw_text)} chars): {raw_text[:500]!r}'
                ),
            }

    # -------------------------------------------------------------------------
    # Jupyter kernel protocol — the one method we really need to implement
    # -------------------------------------------------------------------------

    def do_execute(self, code, silent,
                   store_history=True, user_expressions=None,
                   allow_stdin=False):
        """
        Execute ``code`` in Maya and send output back to JupyterLab.

        Called once per cell by the ipykernel framework.

        Parameters
        ----------
        code : str
            The cell source code (may be multi-line).
        silent : bool
            If True, execute without sending any display messages.
            ipykernel uses this internally for completion and introspection
            requests.  We still report error status when silent=True.
        store_history : bool
            Whether to add this cell to execution history (handled by base).
        user_expressions : dict or None
            Extra expressions to evaluate after execution (not used here).
        allow_stdin : bool
            Whether input() calls are allowed (not implemented — Maya's
            commandPort is not interactive).

        Returns
        -------
        dict
            Execution reply: {'status': 'ok', ...} or {'status': 'error', ...}
        """

        # Nothing to do for blank cells.
        if not code.strip():
            return {
                'status':          'ok',
                'execution_count': self.execution_count,
                'payload':         [],
                'user_expressions': {},
            }

        response = self._send_to_maya(code)

        stdout = response.get('stdout') or ''
        result = response.get('result')    # repr() string, or None
        error  = response.get('error')    # traceback string, or None

        # --- Relay output to JupyterLab (skipped when silent=True) ----------
        if not silent:

            # 1. Stdout/stderr stream — everything printed during execution.
            if stdout:
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stdout',
                    'text': stdout,
                })

            # 2. Execute result — the repr() of an expression's return value.
            #    Only present when the cell was a single evaluable expression
            #    (eval path in _jupyter_exec).  Statements produce result=None.
            if result is not None:
                self.send_response(self.iopub_socket, 'execute_result', {
                    'execution_count': self.execution_count,
                    'data':            {'text/plain': result},
                    'metadata':        {},
                })

            # --- Future rich output hook ------------------------------------
            # When _jupyter_exec() is extended to capture display() calls,
            # uncomment this block to relay them to JupyterLab:
            #
            # for item in response.get('display_items', []):
            #     self.send_response(self.iopub_socket, 'display_data', {
            #         'data':     item.get('data', {}),
            #         'metadata': item.get('metadata', {}),
            #     })

        # --- Error handling -------------------------------------------------
        # Note: stdout is shown BEFORE the error.  A cell that prints something
        # and then raises an exception correctly shows both the output and the
        # traceback, matching IPython's behaviour.
        if error:
            ename, evalue = _parse_exception(error)
            tb_lines = error.splitlines()

            if not silent:
                self.send_response(self.iopub_socket, 'error', {
                    'ename':     ename,
                    'evalue':    evalue,
                    'traceback': tb_lines,
                })

            return {
                'status':          'error',
                'execution_count': self.execution_count,
                'ename':           ename,
                'evalue':          evalue,
                'traceback':       tb_lines,
            }

        return {
            'status':           'ok',
            'execution_count':  self.execution_count,
            'payload':          [],
            'user_expressions': {},
        }

    def do_shutdown(self, restart):
        """
        Clean shutdown.  Maya manages its own process, so we have nothing to
        tear down on the kernel side.  The commandPort stays open in Maya.
        """
        return {'status': 'ok', 'restart': restart}


# ---------------------------------------------------------------------------
# Entry point
# Called by kernel.json: python -m maya_jupyter.kernel -f <connection_file>
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MayaKernel)
