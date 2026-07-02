"""Static file server -- VULNERABLE state (aiohttp < 3.9.2, CVE-2024-23334).

The body of ``serve`` reproduces the security-relevant logic of aiohttp's
``StaticResource._handle`` from **v3.9.1** verbatim. When ``follow_symlinks`` is
True, the directory-containment check is skipped, so a request path containing
``..`` escapes the served root -- CWE-22 Path Traversal.

Reference (v3.9.1, aiohttp/web_urldispatcher.py)::

    filepath = self._directory.joinpath(filename).resolve()
    if not self._follow_symlinks:
        filepath.relative_to(self._directory)
"""
from pathlib import Path

from errors import Forbidden, NotFound


class StaticFileServer:
    """Serve files from ``directory`` in response to a relative request path."""

    def __init__(self, directory, *, follow_symlinks=False):
        self._directory = Path(directory).resolve()
        self._follow_symlinks = follow_symlinks

    def serve(self, rel_url: str) -> bytes:
        filename = Path(rel_url)
        if filename.anchor:
            # Absolute name like /etc/passwd, C:\..., or \\host\share.
            raise Forbidden()
        try:
            filepath = self._directory.joinpath(filename).resolve()
            if not self._follow_symlinks:
                filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError):
            raise NotFound()
        if filepath.is_dir():
            raise Forbidden()
        if filepath.is_file():
            return filepath.read_bytes()
        raise NotFound()
