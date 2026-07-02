"""URL fetching -- FIXED (internal addresses blocked).

The target host is resolved to an IP and rejected if it falls in loopback,
private, link-local, reserved, multicast or unspecified ranges before any fetch
happens. The fetch itself is stubbed so the harness stays offline.
"""
import ipaddress
import socket
from urllib.parse import urlparse


class BlockedError(Exception):
    """Raised when a URL is not allowed to be fetched."""


def _resolve(host):
    try:
        return ipaddress.ip_address(host)
    except ValueError:
        return ipaddress.ip_address(socket.gethostbyname(host))


def fetch(url):
    host = urlparse(url).hostname
    if not host:
        raise BlockedError("missing host")
    ip = _resolve(host)
    if (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_reserved or ip.is_multicast or ip.is_unspecified):
        raise BlockedError(f"internal address blocked: {ip}")
    return b"<fetched:" + url.encode() + b">"
