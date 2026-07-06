"""Shared minimal DOM + URL whitelist for the wagtail link example.

``create_element`` renders a tiny anchor tag so the tests can inspect the
resulting HTML. ``check_url`` mirrors wagtail.core.whitelist.check_url: it only
permits safe schemes and neutralises everything else (e.g. ``javascript:``).
"""
from urllib.parse import urlparse

ALLOWED_SCHEMES = {"http", "https", "ftp", "mailto", "tel", ""}


def check_url(url_string):
    if not url_string:
        return None
    scheme = urlparse(url_string).scheme.lower()
    if scheme in ALLOWED_SCHEMES:
        return url_string
    return None  # unsafe scheme (javascript:, data:, ...) -> dropped


def create_element(tag, attrs, children):
    parts = []
    for k, v in attrs.items():
        if v is None:
            continue
        parts.append(f'{k}="{v}"')
    attr_str = (" " + " ".join(parts)) if parts else ""
    return f"<{tag}{attr_str}>{children}</{tag}>"
