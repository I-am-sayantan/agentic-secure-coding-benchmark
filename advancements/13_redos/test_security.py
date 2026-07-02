"""Security tests -- regular-expression denial of service (CWE-1333).

Validation must finish quickly even on a crafted worst-case input. The call runs
in a separate process so catastrophic backtracking can be timed out and killed
instead of hanging the whole test run (a watchdog *thread* cannot interrupt a
regex match, which holds the GIL in C).
"""
import os
import subprocess
import sys

import pytest

_TIMEOUT_SECONDS = 2.0


def test_no_catastrophic_backtracking():
    impl = os.environ.get("SV_IMPL", "fixed")
    payload = "a" * 40 + "!"
    code = (
        "import importlib;"
        f"m = importlib.import_module('impl_{impl}');"
        f"m.is_match({payload!r})"
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("validation did not finish in time (catastrophic backtracking)")
    assert proc.returncode == 0, (
        f"validation raised instead of completing: {proc.stderr.strip()}"
    )
