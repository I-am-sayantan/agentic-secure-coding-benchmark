"""Security tests -- weak cryptography (CWE-327).

The stored value must be salted (identical passwords differ) and must not be a
bare fast hash of the password.
"""
import hashlib


def test_hash_is_salted(mod):
    first = mod.hash_password("same-password")
    second = mod.hash_password("same-password")
    assert first != second, "password hash is unsalted (identical passwords collide)"


def test_not_bare_md5(mod):
    password = "password"
    assert mod.hash_password(password) != hashlib.md5(password.encode()).hexdigest(), \
        "password stored as a fast, unsalted hash"
