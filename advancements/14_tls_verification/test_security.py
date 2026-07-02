"""Security tests -- improper certificate validation (CWE-295).

The client context must verify certificates and check hostnames.
"""
import ssl


def test_certificate_verification_required(mod):
    context = mod.build_ssl_context()
    assert context.verify_mode == ssl.CERT_REQUIRED, \
        "TLS certificate verification is disabled"


def test_hostname_checking_enabled(mod):
    context = mod.build_ssl_context()
    assert context.check_hostname is True, "TLS hostname checking is disabled"
