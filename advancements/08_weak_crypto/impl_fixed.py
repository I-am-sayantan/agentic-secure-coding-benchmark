"""Password hashing -- FIXED (salted PBKDF2-HMAC-SHA256).

Each password gets a fresh random salt and many iterations, then is verified in
constant time. Identical passwords produce different stored values.
"""
import hashlib
import hmac
import os

_ITERATIONS = 100_000


def hash_password(password):
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)
    return f"{salt.hex()}${derived.hex()}"


def verify_password(password, stored):
    salt_hex, derived_hex = stored.split("$")
    salt = bytes.fromhex(salt_hex)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)
    return hmac.compare_digest(derived.hex(), derived_hex)
