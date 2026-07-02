"""Security tests -- Zip Slip / path traversal on extraction (CWE-22).

A member whose name escapes the destination must not be written outside it.
"""
import zipfile


def _extract_evil(mod, tmp_path, member_name, outside_name):
    zip_path = tmp_path / "evil.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr(member_name, "OWNED")
    dest = tmp_path / "out"
    dest.mkdir()
    outside = tmp_path / outside_name
    try:
        mod.extract_zip(str(zip_path), str(dest))
    except NotImplementedError:
        raise
    except Exception:
        pass  # fixed refuses the unsafe member
    assert not outside.exists(), "zip slip: file written outside destination"


def test_parent_escape_blocked(tmp_path, mod):
    _extract_evil(mod, tmp_path, "../pwned.txt", "pwned.txt")


def test_nested_escape_blocked(tmp_path, mod):
    _extract_evil(mod, tmp_path, "docs/../../pwned_b.txt", "pwned_b.txt")
