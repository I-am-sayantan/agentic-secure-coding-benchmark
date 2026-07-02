"""HTTPS client context -- FIXED (verification on).

Returns the standard client context, which verifies the server certificate
chain and checks the hostname against the certificate.
"""
import ssl


def build_ssl_context():
    return ssl.create_default_context()
