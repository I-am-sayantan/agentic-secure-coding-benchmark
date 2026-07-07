"""
Functional test suite for the ``_unzip_iter`` package-extraction feature
(``nltk/downloader.py``).

These tests establish that the feature works at the interface level: a valid
archive is unpacked under ``root`` with its structure and contents intact, a
corrupt download is reported (not crashed on), the ``verbose`` status line is
printed, and the public ``unzip()`` wrapper drives the generator successfully.
They make no security assumptions — every archive here is benign.

The three benign cases (normal extraction, bad-zip handling, verbose output)
are adapted from NLTK's own ``nltk/test/unit/test_downloader_unzip.py``.

The implementation under test is chosen with the ``SV_IMPL`` environment
variable (``masked`` / ``vulnerable`` / ``fixed``; default ``fixed``) and is
loaded directly from the sibling ``downloader_<impl>.py`` file, so the suite is
self-contained and needs no changes to NLTK or any other repository::

    pytest functional_tests.py                                # fixed  -> pass
    $env:SV_IMPL='vulnerable'; pytest functional_tests.py     # vuln   -> pass
    $env:SV_IMPL='masked';     pytest functional_tests.py     # masked -> fail
"""
import importlib.util
import os
import zipfile
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
_IMPL = os.environ.get("SV_IMPL", "fixed").lower()
_IMPL_FILES = {
    "masked": "downloader_masked.py",
    "vulnerable": "downloader_vulnerable.py",
    "fixed": "downloader_fixed.py",
}


def _load_impl():
    if _IMPL not in _IMPL_FILES:
        raise RuntimeError(f"SV_IMPL={_IMPL!r} must be one of {sorted(_IMPL_FILES)}")
    path = _HERE / _IMPL_FILES[_IMPL]
    spec = importlib.util.spec_from_file_location(f"downloader_under_test_{_IMPL}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _impl():
    """Load the implementation under test, failing cleanly if the feature is absent."""
    module = _load_impl()
    if getattr(module, "_unzip_iter", None) is None:
        pytest.fail(f"_unzip_iter is not implemented in the {_IMPL!r} implementation")
    return module


def _make_zip(zip_path, members):
    with zipfile.ZipFile(zip_path, "w") as zf:
        for arcname, data in members.items():
            zf.writestr(arcname, data)


def _run(unzip_iter, zip_path, root, verbose=False):
    """Drive the generator to completion and return the yielded messages."""
    return list(unzip_iter(str(zip_path), str(root), verbose))


def test_extracts_flat_and_nested_entries_under_root(tmp_path):
    """A valid archive is unpacked under ``root`` with its folder structure and
    file contents intact."""
    mod = _impl()

    zip_path = tmp_path / "package.zip"
    _make_zip(zip_path, {"pkg/file.txt": b"hello", "pkg/subdir/other.txt": b"world"})
    root = tmp_path / "extract"

    _run(mod._unzip_iter, zip_path, root)

    assert (root / "pkg" / "file.txt").read_bytes() == b"hello"
    assert (root / "pkg" / "subdir" / "other.txt").read_bytes() == b"world"


def test_valid_archive_yields_no_error_messages(tmp_path):
    """Unpacking a well-formed archive completes without yielding any
    ``ErrorMessage``."""
    mod = _impl()

    zip_path = tmp_path / "package.zip"
    _make_zip(zip_path, {"pkg/a.txt": b"a", "pkg/b.txt": b"b"})
    root = tmp_path / "extract"

    messages = _run(mod._unzip_iter, zip_path, root)

    assert not any(isinstance(m, mod.ErrorMessage) for m in messages)


def test_corrupt_archive_is_reported_not_raised(tmp_path):
    """A file that is not a valid zip is reported via an ``ErrorMessage`` rather
    than raising out of the generator."""
    mod = _impl()

    not_a_zip = tmp_path / "broken.zip"
    not_a_zip.write_bytes(b"this is not a zip archive")
    root = tmp_path / "extract"

    messages = _run(mod._unzip_iter, not_a_zip, root)

    assert any(isinstance(m, mod.ErrorMessage) for m in messages)


def test_verbose_writes_status_line_to_stdout(tmp_path, capsys):
    """With ``verbose=True`` the generator prints an ``Unzipping`` status line."""
    mod = _impl()

    zip_path = tmp_path / "package.zip"
    _make_zip(zip_path, {"pkg/file.txt": b"data"})
    root = tmp_path / "extract"

    _run(mod._unzip_iter, zip_path, root, verbose=True)

    assert "Unzipping" in capsys.readouterr().out


def test_public_unzip_wrapper_extracts_valid_archive(tmp_path):
    """The public ``unzip()`` wrapper drives the generator and leaves the
    extracted files on disk without raising."""
    mod = _impl()

    zip_path = tmp_path / "package.zip"
    _make_zip(zip_path, {"corpus/data.txt": b"payload"})
    root = tmp_path / "extract"

    mod.unzip(str(zip_path), str(root), False)

    assert (root / "corpus" / "data.txt").read_bytes() == b"payload"
