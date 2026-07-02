"""Functional tests -- hashing/verification works at the interface level."""


def test_verify_correct_password(mod):
    stored = mod.hash_password("s3cret")
    assert mod.verify_password("s3cret", stored) is True


def test_reject_wrong_password(mod):
    stored = mod.hash_password("s3cret")
    assert mod.verify_password("wrong", stored) is False


def test_hash_is_string(mod):
    assert isinstance(mod.hash_password("anything"), str)
