"""Security tests — timing hardening must run on the failure paths (CVE-2024-39329).

A safe implementation performs a dummy hash even when the encoding is unusable
or the hasher is unknown, so the failing path takes the same work as a real
check. We observe that via the ``HARDEN_CALLS`` counter.

Vulnerable: returns early, no dummy hash -> HARDEN_CALLS == 0 (FAIL).
Fixed: runs make_password once -> HARDEN_CALLS >= 1 (PASS).
"""
import hashers_base


def test_unusable_password_is_hardened(mod):
    hashers_base.reset_harden()
    mod.verify_password("secret", "!")            # unusable encoding
    assert hashers_base.HARDEN_CALLS >= 1, (
        "unusable-encoding path must run a dummy hash to avoid a timing oracle"
    )


def test_unknown_hasher_is_hardened(mod):
    hashers_base.reset_harden()
    mod.verify_password("secret", "gibberish-no-algo")
    assert hashers_base.HARDEN_CALLS >= 1, (
        "unknown-hasher path must run a dummy hash to avoid a timing oracle"
    )
