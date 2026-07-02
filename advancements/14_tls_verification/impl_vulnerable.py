"""HTTPS client context -- VULNERABLE (CWE-295 improper certificate validation).

Certificate verification and hostname checking are switched off to make TLS
"just work" in the face of certificate errors -- which also makes every HTTPS
connection trivially interceptable by a man in the middle.
"""
import ssl


def build_ssl_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context
