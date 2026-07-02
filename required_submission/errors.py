"""Shared exceptions for the static file server feature.

These mirror aiohttp's ``HTTPForbidden`` / ``HTTPNotFound`` in a dependency-free
way, so the three implementation states (masked / vulnerable / fixed) and both
test suites can share one set of exception types.
"""


class Forbidden(Exception):
    """The requested path is not allowed (absolute/UNC path, or a directory)."""


class NotFound(Exception):
    """The requested file does not exist or cannot be served."""
