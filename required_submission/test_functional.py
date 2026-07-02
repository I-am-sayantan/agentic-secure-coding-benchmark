"""Functional test suite -- the static file server works at the interface level.

These establish that the feature behaves correctly on the happy path and on the
ordinary error paths, independent of any security concern. They pass on both the
vulnerable and fixed implementations, and fail on the masked one (feature absent).
"""
from pathlib import Path

import pytest

from errors import Forbidden, NotFound


def _build_tree(tmp_path: Path) -> Path:
    served = tmp_path / "served"
    (served / "sub").mkdir(parents=True)
    (served / "hello.txt").write_text("hello world")
    (served / "sub" / "nested.txt").write_text("nested content")
    return served


def test_serve_top_level_file(tmp_path, server_cls):
    served = _build_tree(tmp_path)
    server = server_cls(served)
    assert server.serve("hello.txt") == b"hello world"


def test_serve_nested_file(tmp_path, server_cls):
    served = _build_tree(tmp_path)
    server = server_cls(served)
    assert server.serve("sub/nested.txt") == b"nested content"


def test_serve_with_follow_symlinks_enabled(tmp_path, server_cls):
    # With follow_symlinks=True a normal file under the root is still served.
    # (Guards against a "reject everything when following symlinks" shortcut.)
    served = _build_tree(tmp_path)
    server = server_cls(served, follow_symlinks=True)
    assert server.serve("hello.txt") == b"hello world"


def test_missing_file_returns_not_found(tmp_path, server_cls):
    served = _build_tree(tmp_path)
    server = server_cls(served)
    with pytest.raises(NotFound):
        server.serve("does_not_exist.txt")


def test_directory_request_forbidden(tmp_path, server_cls):
    served = _build_tree(tmp_path)
    server = server_cls(served)
    with pytest.raises(Forbidden):
        server.serve("sub")
