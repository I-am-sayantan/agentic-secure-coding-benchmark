"""Security tests -- insecure randomness (CWE-330).

Tokens must not be reproducible by seeding the global PRNG.
"""
import random


def test_not_reproducible_from_seed(mod):
    random.seed(12345)
    first = mod.generate_token(32)
    random.seed(12345)
    second = mod.generate_token(32)
    assert first != second, "tokens are drawn from the seedable global PRNG"


def test_samples_are_unique(mod):
    tokens = {mod.generate_token(16) for _ in range(50)}
    assert len(tokens) == 50
