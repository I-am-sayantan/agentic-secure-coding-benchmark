"""Validate the three benchmark states for the aiohttp-session example.

    masked      -> functional FAIL, security FAIL
    vulnerable  -> functional PASS, security FAIL
    fixed       -> functional PASS, security PASS

Usage:  python run_validation.py
"""
import os
import subprocess
import sys

STATES = ["masked", "vulnerable", "fixed"]
SUITES = {"functional": "test_functional.py", "security": "test_security.py"}
EXPECTED = {
    "masked":     {"functional": "FAIL", "security": "FAIL"},
    "vulnerable": {"functional": "PASS", "security": "FAIL"},
    "fixed":      {"functional": "PASS", "security": "PASS"},
}

HERE = os.path.dirname(os.path.abspath(__file__))


def run_suite(impl: str, path: str) -> str:
    env = dict(os.environ, SV_IMPL=impl)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", path, "-q"],
        env=env, cwd=HERE, capture_output=True, text=True,
    )
    return "PASS" if proc.returncode == 0 else "FAIL"


def main() -> int:
    results = {
        impl: {name: run_suite(impl, path) for name, path in SUITES.items()}
        for impl in STATES
    }
    header = f"{'implementation':<12} | {'functional':^10} | {'security':^10}"
    print(header)
    print("-" * len(header))
    ok = True
    for impl in STATES:
        func, sec = results[impl]["functional"], results[impl]["security"]
        bad = (func != EXPECTED[impl]["functional"]
               or sec != EXPECTED[impl]["security"])
        flag = "  <-- UNEXPECTED" if bad else ""
        print(f"{impl:<12} | {func:^10} | {sec:^10}{flag}")
        ok = ok and not bad
    print()
    print("VALID: all three states match the expected SusVibes pattern."
          if ok else "INVALID: a state deviated from the expected pattern.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
