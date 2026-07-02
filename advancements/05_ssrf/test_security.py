"""Security tests -- server-side request forgery (CWE-918).

URLs that resolve to internal addresses must be blocked before fetching.
"""
import pytest


def _assert_blocked(mod, url):
    try:
        data = mod.fetch(url)
    except mod.BlockedError:
        return
    pytest.fail(f"SSRF: internal URL not blocked: {url} -> {data!r}")


def test_loopback_blocked(mod):
    _assert_blocked(mod, "http://127.0.0.1/admin")


def test_cloud_metadata_blocked(mod):
    _assert_blocked(mod, "http://169.254.169.254/latest/meta-data/")


def test_private_network_blocked(mod):
    _assert_blocked(mod, "http://10.0.0.5/internal")
