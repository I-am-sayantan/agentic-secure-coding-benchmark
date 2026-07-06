# SusVibes Examples — Converted to Local Runnable Tasks

This folder takes the five official **SusVibes example instances** (shipped as `.md` files in
`../susvibes/datasets/default/examples/`) and converts each one into a **self-contained,
locally runnable benchmark task** — no Docker, no LLM pipeline, no cloning the upstream repo.

Each task keeps the SusVibes three-state model (masked / vulnerable / fixed) and two test suites
(functional + security), and is graded with plain `pytest`.

---

## Why this exists (and how it differs from SusVibes)

The real SusVibes examples are the *output* of an automated curation pipeline that needs
**Docker** (per-repo images), an **LLM API** (to write the mask, problem statement, and test
parsers), and the **upstream source code**. The `.md` files themselves are only *diffs +
descriptions* — they cannot be executed on their own.

We reproduced the same task shape **by hand**, using a different toolchain:

| Step | SusVibes (original) | This folder (what we did) |
|------|---------------------|---------------------------|
| Pick the vulnerability | mine CVE datasets | read the example's `README.md` (CVE + CWE) |
| Understand vulnerable vs. fixed code | agent + repo | read the example's `security_fix.md` diff |
| Write `impl_masked / vulnerable / fixed` | LLM agent + Docker | **GitHub Copilot**, extracted into small standalone modules |
| Write functional + security tests | LLM agent + repo tests | **GitHub Copilot**, hand-verified |
| Run / grade | Docker eval harness | **`pytest`** via `run_validation.py` (local) |

So: **Copilot generated the implementation code and tests; `pytest` ran them locally.** No Docker
and no LLM eval pipeline were used.

---

## Steps I took (reproducible)

1. **Read each example** in `../susvibes/datasets/default/examples/<instance>/`:
   - `README.md` → project, CVE id, CWE type.
   - `problem_statement.md` → the innocent feature ticket.
   - `security_fix.md` → the real vulnerable→fixed diff (the `-`/`+` lines).
2. **Identified the security-relevant unit** from the diff (the one function/class the fix
   touches).
3. **Used GitHub Copilot to generate three implementations** of that unit:
   - `impl_masked.py` — feature body removed (`raise NotImplementedError`).
   - `impl_vulnerable.py` — the pre-fix logic (the `-` side of the diff).
   - `impl_fixed.py` — the post-fix logic (the `+` side of the diff).
4. **Used GitHub Copilot to write two test suites**:
   - `test_functional.py` — proves the feature works (passes on vulnerable **and** fixed).
   - `test_security.py` — proves the bug is gone (fails on vulnerable, passes on fixed).
5. **Added the harness** (`conftest.py` selects the impl via the `SV_IMPL` env var;
   `run_validation.py` prints the 3×2 matrix).
6. **Ran `pytest` locally** and confirmed every task matches the expected SusVibes pattern.

---

## The five tasks

| Folder | Project | CVE | CWE | Security issue (vulnerable → fixed) |
|--------|---------|-----|-----|-------------------------------------|
| [aiohttp_session](aiohttp_session) | aio-libs/aiohttp-session | CVE-2018-1000814 | CWE-613 | expired session data still loaded → discarded past `max_age` |
| [buildbot_redirect](buildbot_redirect) | buildbot/buildbot | CVE-2019-7313 | CWE-93 | CRLF in redirect URL → stripped before use |
| [requests_proxy](requests_proxy) | psf/requests | CVE-2023-32681 | CWE-200 | `Proxy-Authorization` sent over HTTPS → omitted for https |
| [wagtail_link](wagtail_link) | wagtail/wagtail | CVE-2021-29434 | CWE-79 | `javascript:` URL in link href → sanitised via `check_url` |
| [django_hashers](django_hashers) | django/django | CVE-2024-39329 | timing (login oracle) | early return without dummy hash → constant-time hardening runs |

Each folder contains: `impl_masked.py`, `impl_vulnerable.py`, `impl_fixed.py`,
`test_functional.py`, `test_security.py`, `conftest.py`, `run_validation.py`
(plus a small shared helper where noted below).

---

## How to run

```powershell
# One task — prints the 3x2 matrix
cd susvibe_examples\wagtail_link
python run_validation.py

# Grade a single state by hand
$env:SV_IMPL = "vulnerable"; python -m pytest -q   # functional PASS, security FAIL
$env:SV_IMPL = "fixed";      python -m pytest -q   # all PASS
$env:SV_IMPL = $null
```

`SV_IMPL` selects which implementation the tests import (`masked` / `vulnerable` / `fixed`;
default `fixed`).

---

## Test results (verified locally with pytest)

Every task reproduces the required SusVibes pattern:

```
masked      -> functional FAIL, security FAIL   (feature removed)
vulnerable  -> functional PASS, security FAIL   (feature works, bug present)
fixed       -> functional PASS, security PASS   (genuine fix)
```

### Validation matrices (`run_validation.py`)

```
==================== aiohttp_session ====================
implementation | functional |  security
----------------------------------------
masked         |    FAIL    |    FAIL
vulnerable     |    PASS    |    FAIL
fixed          |    PASS    |    PASS
VALID: all three states match the expected SusVibes pattern.

==================== buildbot_redirect ====================
masked         |    FAIL    |    FAIL
vulnerable     |    PASS    |    FAIL
fixed          |    PASS    |    PASS
VALID

==================== requests_proxy ====================
masked         |    FAIL    |    FAIL
vulnerable     |    PASS    |    FAIL
fixed          |    PASS    |    PASS
VALID

==================== wagtail_link ====================
masked         |    FAIL    |    FAIL
vulnerable     |    PASS    |    FAIL
fixed          |    PASS    |    PASS
VALID

==================== django_hashers ====================
masked         |    FAIL    |    FAIL
vulnerable     |    PASS    |    FAIL
fixed          |    PASS    |    PASS
VALID
```

### Raw pytest summaries (functional + security together)

| Task | masked | vulnerable | fixed |
|------|--------|------------|-------|
| aiohttp_session | 6 failed | 2 failed, 4 passed | 6 passed |
| buildbot_redirect | 4 failed | 2 failed, 2 passed | 4 passed |
| requests_proxy | 3 failed | 1 failed, 2 passed | 3 passed |
| wagtail_link | 4 failed | 2 failed, 2 passed | 4 passed |
| django_hashers | 5 failed | 2 failed, 3 passed | 5 passed |

In every row: **masked** fails everything (feature gone), **vulnerable** passes the functional
tests but fails the security tests (the trap is real), and **fixed** passes all tests.

---

## Tooling summary

- **Code + tests generated with:** GitHub Copilot.
- **Executed / graded with:** `pytest` (locally).
- **Not used:** Docker, the SusVibes eval harness, any LLM curation pipeline, or upstream repo checkouts.
