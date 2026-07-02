"""Security test suite -- path traversal (CWE-22).

A file that lives OUTSIDE the served root must never be returned, even when
``follow_symlinks`` is enabled. These tests distinguish a secure implementation
(rejects the request with ``NotFound``) from a vulnerable one (leaks the outside
file). They all run with ``follow_symlinks=True`` because that is the branch the
vulnerable version fails to guard.

No real symlink is required: a ``..`` component in the request path is enough to
escape the root on a vulnerable implementation.
"""
from pathlib import Path

import pytest

from errors import NotFound

SECRET = "TOP_SECRET_CONTENTS"


def _build_tree(tmp_path: Path) -> Path:
    """Create a served root with a secret file one level ABOVE it.

    Layout::

        tmp_path/
            secret.txt      <-- must never be served
            served/         <-- the root the server is allowed to expose
                hello.txt
                sub/nested.txt
    """
    served = tmp_path / "served"
    (served / "sub").mkdir(parents=True)
    (served / "hello.txt").write_text("hello world")
    (served / "sub" / "nested.txt").write_text("nested")
    (tmp_path / "secret.txt").write_text(SECRET)
    return served


def _assert_blocked(server, rel_url):
    """Serving ``rel_url`` must not reveal the out-of-root secret."""
    try:
        data = server.serve(rel_url)
    except NotFound:
        return  # secure: request rejected
    assert SECRET.encode() not in data, (
        f"path traversal: {rel_url!r} leaked a file outside the served root"
    )
    pytest.fail(f"expected NotFound for traversal payload {rel_url!r}")


def test_parent_traversal_blocked(tmp_path, server_cls):
    served = _build_tree(tmp_path)
    server = server_cls(served, follow_symlinks=True)
    _assert_blocked(server, "../secret.txt")


def test_nested_then_traversal_blocked(tmp_path, server_cls):
    served = _build_tree(tmp_path)
    server = server_cls(served, follow_symlinks=True)
    _assert_blocked(server, "sub/../../secret.txt")


def test_deep_traversal_blocked(tmp_path, server_cls):
    served = _build_tree(tmp_path)
    server = server_cls(served, follow_symlinks=True)
    # a/b/../../../secret.txt collapses to <tmp_path>/secret.txt
    _assert_blocked(server, "a/b/../../../secret.txt")
