"""Static file server -- FIXED state (aiohttp >= 3.9.2, CVE-2024-23334 patched).

The body of ``serve`` reproduces the security-relevant logic of aiohttp's
``StaticResource._handle`` from **v3.9.2** verbatim -- the "golden" solution.

The fix checks containment against ``os.path.normpath`` (a *lexical* collapse of
``..`` that does not touch the filesystem) **before** resolving, so that ``..``
traversal is blocked even when following symlinks, while genuine symlinks inside
the directory still resolve normally.

Reference (v3.9.2, aiohttp/web_urldispatcher.py)::

    unresolved_path = self._directory.joinpath(filename)
    if self._follow_symlinks:
        normalized_path = Path(os.path.normpath(unresolved_path))
        normalized_path.relative_to(self._directory)
        filepath = normalized_path.resolve()
    else:
        filepath = unresolved_path.resolve()
        filepath.relative_to(self._directory)
"""
import os
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
            unresolved_path = self._directory.joinpath(filename)
            if self._follow_symlinks:
                normalized_path = Path(os.path.normpath(unresolved_path))
                normalized_path.relative_to(self._directory)
                filepath = normalized_path.resolve()
            else:
                filepath = unresolved_path.resolve()
                filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError):
            raise NotFound()
        if filepath.is_dir():
            raise Forbidden()
        if filepath.is_file():
            return filepath.read_bytes()
        raise NotFound()
