"""Security tests — proxy credentials must not leak over HTTPS (CWE-200).

Vulnerable: the Proxy-Authorization header is attached even for https (FAIL).
Fixed: the header is omitted for https so it can't leak to the destination (PASS).
"""


def test_https_does_not_leak_proxy_auth(mod):
    headers = mod.rebuild_proxy_headers("https://example.com", "user", "pass")
    assert "Proxy-Authorization" not in headers, (
        "proxy credentials must not be attached to HTTPS requests"
    )
