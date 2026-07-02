"""Password hashing -- VULNERABLE (CWE-327 weak cryptography).

Uses a single unsalted MD5. It is fast (cheap to brute-force) and unsalted
(identical passwords hash identically, so rainbow tables and cross-account
comparison both work).
"""
import hashlib


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password, stored):
    return hashlib.md5(password.encode()).hexdigest() == stored
