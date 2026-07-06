"""Security tests — CRLF header injection must be blocked (CWE-93).

The vulnerable state stores the URL raw, so the injected header survives (FAIL).
The fixed state strips CR/LF and everything after it (PASS).
"""


def test_crlf_injection_stripped(mod):
    r = mod.Redirect("http://host/\r\nSet-Cookie: admin=1")
    assert b"\r\n" not in r.url, "CR/LF must not survive in the redirect URL"


def test_injected_header_removed(mod):
    r = mod.Redirect("http://host/\r\nLocation: http://evil")
    assert b"Location: http://evil" not in r.url
    assert r.url == b"http://host/"
