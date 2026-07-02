"""URL fetching -- VULNERABLE (CWE-918 Server-Side Request Forgery).

Any URL the caller supplies is fetched, including ones that resolve to internal
addresses (loopback, private ranges, the cloud metadata endpoint). The fetch
itself is stubbed so the harness stays offline; the missing defence is the
host/address check.
"""


class BlockedError(Exception):
    """Raised when a URL is not allowed to be fetched."""


def fetch(url):
    return b"<fetched:" + url.encode() + b">"
