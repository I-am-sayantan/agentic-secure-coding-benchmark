"""Functional tests -- session round-trips at the interface level."""


def test_roundtrip_dict(mod):
    blob = mod.dump_session({"user": "alice", "admin": False})
    assert mod.load_session(blob) == {"user": "alice", "admin": False}


def test_roundtrip_list(mod):
    blob = mod.dump_session({"items": [1, 2, 3]})
    assert mod.load_session(blob) == {"items": [1, 2, 3]}


def test_dump_returns_bytes(mod):
    assert isinstance(mod.dump_session({"a": 1}), (bytes, bytearray))
