"""
Security test suite for the ``_unzip_iter`` package-extraction feature
(``nltk/downloader.py``).

Security property under test
----------------------------
Extracting a downloaded archive must never write **outside** the destination
directory ``root``.

Modern CPython's ``zipfile`` already neutralises *name-based* traversal — an
entry called ``../evil`` or ``/evil`` is stripped by ``ZipFile.extract`` and
lands harmlessly inside ``root``. The behaviour that actually separates a safe
extractor from an unsafe one is therefore whether it writes *through a
pre-existing directory link that points out of ``root``*. A naive
``zipfile.extractall(root)`` follows such a link and escapes; a safe
implementation resolves the real destination first and refuses. That genuine
escape is what every test below exercises.

Running it
----------
The implementation under test is chosen with the ``SV_IMPL`` environment
variable (``masked`` / ``vulnerable`` / ``fixed``; default ``fixed``) and is
loaded directly from the sibling ``downloader_<impl>.py`` file, so the suite is
self-contained and needs no changes to NLTK or any other repository::

    pytest security_tests.py                                  # fixed  -> pass
    $env:SV_IMPL='vulnerable'; pytest security_tests.py       # vuln   -> fail
    $env:SV_IMPL='masked';     pytest security_tests.py       # masked -> fail

A directory link is created with a real OS symlink where that is permitted,
falling back to an NTFS junction on Windows (which needs no privilege). If
neither is possible the tests skip rather than report a misleading pass.
"""
import importlib.util
import os
import subprocess
import sys
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


def _get_unzip_iter():
    """Return the feature under test, or fail cleanly if it is absent (masked)."""
    module = _load_impl()
    fn = getattr(module, "_unzip_iter", None)
    if fn is None:
        pytest.fail(f"_unzip_iter is not implemented in the {_IMPL!r} implementation")
    return fn


def _make_zip(zip_path, members):
    with zipfile.ZipFile(zip_path, "w") as zf:
        for arcname, data in members.items():
            zf.writestr(arcname, data)


def _make_dir_link(link_path, target_dir):
    """Create ``link_path`` as a directory link to ``target_dir``.

    Prefers a real symlink; on Windows without symlink privilege it falls back
    to an NTFS junction (``mklink /J``), which needs no elevation. Skips the
    test when neither mechanism is available.
    """
    link_path, target_dir = Path(link_path), Path(target_dir)
    try:
        os.symlink(target_dir, link_path, target_is_directory=True)
        return
    except (OSError, NotImplementedError, AttributeError):
        pass
    if sys.platform.startswith("win"):
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link_path), str(target_dir)],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and link_path.is_dir():
            return
    pytest.skip("cannot create a directory symlink or junction in this environment")


def _remove_dir_link(link_path):
    """Detach a link without touching its target (avoids clobbering during teardown)."""
    for remove in (os.unlink, os.rmdir):
        try:
            remove(str(link_path))
            return
        except OSError:
            continue


def _run(unzip_iter, zip_path, root):
    """Drive the generator to completion and return the yielded messages."""
    return list(unzip_iter(str(zip_path), str(root), False))


def test_link_escape_cannot_create_file_outside_root(tmp_path):
    """An entry routed through a pre-existing directory link must not be able
    to create a brand-new file outside the extraction root."""
    unzip_iter = _get_unzip_iter()

    outside = tmp_path / "outside"
    outside.mkdir()
    root = tmp_path / "extract"
    root.mkdir()
    _make_dir_link(root / "link", outside)
    try:
        zip_path = tmp_path / "attack.zip"
        _make_zip(zip_path, {"pkg/readme.txt": b"benign", "link/pwned.txt": b"owned"})

        _run(unzip_iter, zip_path, root)

        assert not (outside / "pwned.txt").exists(), (
            "extractor wrote a new file outside root through a directory link"
        )
    finally:
        _remove_dir_link(root / "link")


def test_link_escape_cannot_overwrite_file_outside_root(tmp_path):
    """An entry routed through a pre-existing directory link must not be able
    to overwrite a file that already exists outside the root."""
    unzip_iter = _get_unzip_iter()

    outside = tmp_path / "outside"
    outside.mkdir()
    protected = outside / "keep.txt"
    protected.write_bytes(b"ORIGINAL")
    root = tmp_path / "extract"
    root.mkdir()
    _make_dir_link(root / "link", outside)
    try:
        zip_path = tmp_path / "attack.zip"
        _make_zip(zip_path, {"link/keep.txt": b"TAMPERED"})

        _run(unzip_iter, zip_path, root)

        assert protected.read_bytes() == b"ORIGINAL", (
            "extractor overwrote a file outside root through a directory link"
        )
    finally:
        _remove_dir_link(root / "link")


def test_malicious_archive_stays_within_root_and_extracts_benign_entries(tmp_path):
    """The full property: no entry escapes the root, while legitimate entries
    are still extracted normally."""
    unzip_iter = _get_unzip_iter()

    outside = tmp_path / "outside"
    outside.mkdir()
    root = tmp_path / "extract"
    root.mkdir()
    _make_dir_link(root / "link", outside)
    try:
        zip_path = tmp_path / "mixed.zip"
        _make_zip(zip_path, {"corpus/data.txt": b"legit", "link/escape.txt": b"owned"})

        _run(unzip_iter, zip_path, root)

        # Nothing escaped through the link ...
        assert list(outside.iterdir()) == [], (
            "an archive entry escaped the extraction root through a directory link"
        )
        # ... and the legitimate entry was still extracted under root.
        assert (root / "corpus" / "data.txt").read_bytes() == b"legit"
    finally:
        _remove_dir_link(root / "link")
