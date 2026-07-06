"""django hashers example (fixed state) — post-fix logic.

Instead of returning early, the unusable/unknown paths set ``fake_runtime`` and
run a dummy hash once before returning, so the timing of a nonexistent user or
missing hasher matches that of a real verification (the CVE-2024-39329 fix).
"""
from hashers_base import (
    is_password_usable, identify_hasher, verify_hash, make_password,
)


def verify_password(password, encoded, preferred="default"):
    fake_runtime = password is None or not is_password_usable(encoded)

    try:
        hasher = identify_hasher(encoded)
    except ValueError:
        fake_runtime = True

    if fake_runtime:
        # Run the default hasher once to equalise timing between an existing
        # user with an unusable password and a nonexistent user / missing hasher.
        make_password("fake-runtime-password")
        return False, False

    is_correct = verify_hash(password, encoded)
    must_update = False
    return is_correct, must_update
