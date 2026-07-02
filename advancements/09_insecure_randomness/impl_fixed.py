"""Token generation -- FIXED (secrets).

Uses ``secrets``, a cryptographically secure source that cannot be reseeded or
predicted from observed output.
"""
import secrets
import string

_ALPHABET = string.ascii_letters + string.digits


def generate_token(length=16):
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))
