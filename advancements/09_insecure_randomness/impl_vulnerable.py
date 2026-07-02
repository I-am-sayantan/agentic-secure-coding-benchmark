"""Token generation -- VULNERABLE (CWE-330 insecure randomness).

Draws from the ``random`` module -- a deterministic Mersenne Twister seeded
from predictable state. An attacker who can influence or recover the seed can
reproduce the tokens.
"""
import random
import string

_ALPHABET = string.ascii_letters + string.digits


def generate_token(length=16):
    return "".join(random.choice(_ALPHABET) for _ in range(length))
