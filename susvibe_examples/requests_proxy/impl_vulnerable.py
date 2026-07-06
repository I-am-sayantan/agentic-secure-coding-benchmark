"""requests proxy example (vulnerable state) — pre-fix logic.

When rebuilding proxy headers during a redirect, the Proxy-Authorization
header is attached whenever credentials exist — including for HTTPS URLs, where
the tunnel would leak the proxy credentials to the destination
(CVE-2023-32681, CWE-200).
"""
from urllib.parse import urlparse


def _basic_auth_str(username, password):
    return f"Basic {username}:{password}"


def rebuild_proxy_headers(url, username, password):
    scheme = urlparse(url).scheme
    headers = {}
    if username and password:                       # <-- also runs for https
        headers["Proxy-Authorization"] = _basic_auth_str(username, password)
    return headers
