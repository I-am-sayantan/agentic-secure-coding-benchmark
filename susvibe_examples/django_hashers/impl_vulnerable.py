"""django hashers example (vulnerable state) — pre-fix logic.

When the password is ``None``, the encoding is unusable, or the hasher is
unknown, the function returns early **without** running a dummy hash. That makes
the "no such user / bad encoding" path measurably faster than a real check,
leaking account existence via timing (CVE-2024-39329).
"""
from hashers_base import (
    is_password_usable, identify_hasher, verify_hash, make_password,
)


def verify_password(password, encoded, preferred="default"):
    if password is None or not is_password_usable(encoded):
        return False, False                       # <-- early return, no harden

    try:
        hasher = identify_hasher(encoded)
    except ValueError:
        return False, False                       # <-- early return, no harden

    is_correct = verify_hash(password, encoded)
    must_update = False
    return is_correct, must_update
