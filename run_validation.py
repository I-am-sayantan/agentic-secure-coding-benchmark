"""Validate the three benchmark states.

Runs both test suites against each implementation and asserts the expected
SusVibes pass/fail pattern::

    masked      -> functional FAIL, security FAIL   (feature removed)
    vulnerable  -> functional PASS, security FAIL   (feature works, bug present)
    fixed       -> functional PASS, security PASS   (genuine fix)

Exits 0 if every cell matches, non-zero otherwise. Usage::

    python run_validation.py
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


def run_suite(impl: str, path: str) -> str:
    env = dict(os.environ, SV_IMPL=impl)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", path, "-q"],
        env=env,
        capture_output=True,
        text=True,
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
        func = results[impl]["functional"]
        sec = results[impl]["security"]
        flag = "" if (func == EXPECTED[impl]["functional"]
                      and sec == EXPECTED[impl]["security"]) else "  <-- UNEXPECTED"
        print(f"{impl:<12} | {func:^10} | {sec:^10}{flag}")
        if flag:
            ok = False

    print()
    if ok:
        print("VALID: all three states match the expected SusVibes pattern.")
        return 0
    print("INVALID: one or more states deviated from the expected pattern.")
    print("Expected pattern:")
    for impl in STATES:
        print(f"  {impl:<12} functional={EXPECTED[impl]['functional']:<4} "
              f"security={EXPECTED[impl]['security']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
