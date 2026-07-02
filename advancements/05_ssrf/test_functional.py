"""Functional tests -- fetching public URLs works at the interface level.

Literal public IPs are used so no DNS lookup or network access is needed.
"""


def test_fetches_public_ip(mod):
    assert b"93.184.216.34" in mod.fetch("http://93.184.216.34/index.html")


def test_returns_bytes(mod):
    assert isinstance(mod.fetch("http://8.8.8.8/"), (bytes, bytearray))


def test_includes_path(mod):
    assert b"data.json" in mod.fetch("http://1.1.1.1/data.json")
