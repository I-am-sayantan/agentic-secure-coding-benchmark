"""Validate the three benchmark states.

    masked      -> functional FAIL, security FAIL
    vulnerable  -> functional PASS, security FAIL
    fixed       -> functional PASS, security PASS
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


def run_suite(impl, path):
    env = dict(os.environ, SV_IMPL=impl)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", path, "-q"],
        env=env, cwd=HERE, capture_output=True, text=True,
    )
    return "PASS" if proc.returncode == 0 else "FAIL"


def main():
    results = {i: {n: run_suite(i, p) for n, p in SUITES.items()} for i in STATES}
    header = f"{'implementation':<12} | {'functional':^10} | {'security':^10}"
    print(header); print("-" * len(header))
    ok = True
    for i in STATES:
        f, s = results[i]["functional"], results[i]["security"]
        bad = (f != EXPECTED[i]["functional"] or s != EXPECTED[i]["security"])
        print(f"{i:<12} | {f:^10} | {s:^10}{'  <-- UNEXPECTED' if bad else ''}")
        ok = ok and not bad
    print()
    print("VALID: all three states match the expected SusVibes pattern."
          if ok else "INVALID: a state deviated from the expected pattern.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
