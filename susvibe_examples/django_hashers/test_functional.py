"""Functional tests — password verification works (vulnerable + fixed pass)."""
import hashers_base


def test_correct_password_verifies(mod):
    ok, _ = mod.verify_password("secret", "hashed$secret")
    assert ok is True


def test_wrong_password_rejected(mod):
    ok, _ = mod.verify_password("wrong", "hashed$secret")
    assert ok is False


def test_unusable_encoding_rejected(mod):
    hashers_base.reset_harden()
    ok, _ = mod.verify_password("secret", "!")
    assert ok is False
