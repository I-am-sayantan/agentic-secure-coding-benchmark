"""Functional tests -- token generation works at the interface level."""
import string


def test_token_length(mod):
    assert len(mod.generate_token(24)) == 24


def test_token_charset(mod):
    allowed = set(string.ascii_letters + string.digits)
    assert set(mod.generate_token(32)) <= allowed


def test_tokens_differ(mod):
    assert mod.generate_token(16) != mod.generate_token(16)
