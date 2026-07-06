"""requests proxy example (fixed state) — post-fix logic.

The Proxy-Authorization header is only attached for non-HTTPS schemes; for
HTTPS the standard adapter (urllib3) handles tunnel auth, so the header is not
appended and cannot be leaked to the destination (the CVE-2023-32681 fix).
"""
from urllib.parse import urlparse


def _basic_auth_str(username, password):
    return f"Basic {username}:{password}"


def rebuild_proxy_headers(url, username, password):
    scheme = urlparse(url).scheme
    headers = {}
    if not scheme.startswith("https") and username and password:  # <-- guard
        headers["Proxy-Authorization"] = _basic_auth_str(username, password)
    return headers
