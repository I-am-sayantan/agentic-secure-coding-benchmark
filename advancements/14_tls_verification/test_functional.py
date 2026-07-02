"""Functional tests -- the context builder returns a usable client context."""
import ssl


def test_returns_ssl_context(mod):
    assert isinstance(mod.build_ssl_context(), ssl.SSLContext)


def test_is_tls_client_context(mod):
    assert mod.build_ssl_context().protocol == ssl.PROTOCOL_TLS_CLIENT


def test_context_is_not_none(mod):
    assert mod.build_ssl_context() is not None
