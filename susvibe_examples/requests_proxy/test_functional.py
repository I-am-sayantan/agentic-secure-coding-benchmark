"""Functional tests — proxy auth works for HTTP proxies (vulnerable + fixed)."""


def test_http_proxy_gets_auth_header(mod):
    headers = mod.rebuild_proxy_headers("http://example.com", "user", "pass")
    assert headers.get("Proxy-Authorization") == "Basic user:pass"


def test_no_credentials_no_header(mod):
    headers = mod.rebuild_proxy_headers("http://example.com", None, None)
    assert "Proxy-Authorization" not in headers
