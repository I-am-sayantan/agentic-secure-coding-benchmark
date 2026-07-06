"""Shared password-hashing primitives for the django timing-attack example.

A tiny, deterministic stand-in for django.contrib.auth.hashers. Every call to
``make_password`` (the "dummy hash" used to equalise timing) increments
``HARDEN_CALLS`` so a test can observe whether the constant-time hardening path
actually ran.
"""

HARDEN_CALLS = 0


def reset_harden():
    global HARDEN_CALLS
    HARDEN_CALLS = 0


def make_password(raw):
    """Stand-in for the real hasher; bumps a counter so tests can see it ran."""
    global HARDEN_CALLS
    HARDEN_CALLS += 1
    return f"hashed${raw}"


def is_password_usable(encoded):
    return bool(encoded) and not encoded.startswith("!")


def identify_hasher(encoded):
    if not encoded or "$" not in encoded:
        raise ValueError("unknown hasher")
    return encoded.split("$", 1)[0]


def verify_hash(password, encoded):
    """True when password matches the stored 'hashed$<raw>' digest."""
    try:
        algo, raw = encoded.split("$", 1)
    except ValueError:
        return False
    return algo == "hashed" and raw == password
