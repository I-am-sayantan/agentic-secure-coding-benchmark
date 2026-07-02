"""Validate every benchmark task under ``benchmark_tasks/``.

For each task folder, run its functional and security suites against all three
implementation states (``masked`` / ``vulnerable`` / ``fixed``) and assert the
SusVibes three-state pattern::

    masked      -> functional FAIL, security FAIL
    vulnerable  -> functional PASS, security FAIL
    fixed       -> functional PASS, security PASS

Each suite runs in its own subprocess with the task folder as the working
directory, so identically named modules across tasks never collide.

Usage::

    python benchmark_tasks/run_all.py
"""
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
STATES = ["masked", "vulnerable", "fixed"]
SUITES = {"functional": "test_functional.py", "security": "test_security.py"}
EXPECTED = {
    "masked":     {"functional": "FAIL", "security": "FAIL"},
    "vulnerable": {"functional": "PASS", "security": "FAIL"},
    "fixed":      {"functional": "PASS", "security": "PASS"},
}


def run_suite(task_dir: pathlib.Path, impl: str, suite: str) -> str:
    env = dict(os.environ, SV_IMPL=impl)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", suite, "-q", "-p", "no:cacheprovider"],
        cwd=task_dir,
        env=env,
        capture_output=True,
        text=True,
    )
    return "PASS" if proc.returncode == 0 else "FAIL"


def main() -> int:
    tasks = sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_", "__"))
    )
    all_ok = True
    for task in tasks:
        if not (task / "test_functional.py").exists():
            continue
        print(f"\n=== {task.name} ===")
        header = f"{'implementation':<12} | {'functional':^10} | {'security':^10}"
        print(header)
        print("-" * len(header))
        for impl in STATES:
            func = run_suite(task, impl, SUITES["functional"])
            sec = run_suite(task, impl, SUITES["security"])
            ok = (func == EXPECTED[impl]["functional"]
                  and sec == EXPECTED[impl]["security"])
            flag = "" if ok else "  <-- UNEXPECTED"
            if not ok:
                all_ok = False
            print(f"{impl:<12} | {func:^10} | {sec:^10}{flag}")

    print("\n" + ("ALL TASKS VALID: every state matches the SusVibes pattern."
                  if all_ok else
                  "SOME TASKS DEVIATED: see the rows flagged UNEXPECTED above."))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
