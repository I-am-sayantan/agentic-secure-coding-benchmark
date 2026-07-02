"""Functional tests -- validation accepts/rejects the right strings."""


def test_accepts_alphanumeric(mod):
    assert mod.is_match("abc123") is True


def test_rejects_hyphen(mod):
    assert mod.is_match("bad-code") is False


def test_rejects_space(mod):
    assert mod.is_match("has space") is False
