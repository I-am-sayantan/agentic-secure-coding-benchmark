"""Directory listing -- VULNERABLE (CWE-78 Command Injection).

The path is interpolated into a shell command string, so shell metacharacters
in ``path`` (``&``, ``&&``, ``|``, ...) let an attacker run extra commands.
"""
import os
import subprocess


def list_dir(path):
    cmd = f"dir {path}" if os.name == "nt" else f"ls {path}"
    return subprocess.check_output(cmd, shell=True, text=True)
