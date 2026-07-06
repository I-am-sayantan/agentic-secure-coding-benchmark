"""Functional tests — the redirect feature works (vulnerable + fixed pass)."""


def test_plain_url_preserved(mod):
    r = mod.Redirect("http://host/login")
    assert r.url == b"http://host/login"


def test_url_is_bytes(mod):
    r = mod.Redirect("http://host/path?next=/home")
    assert isinstance(r.url, bytes)
