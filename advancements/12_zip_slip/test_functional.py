"""Functional tests -- archive extraction works at the interface level."""
import zipfile


def _make_zip(path, members):
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in members.items():
            archive.writestr(name, content)


def test_extracts_top_level_file(tmp_path, mod):
    zip_path = tmp_path / "a.zip"
    _make_zip(zip_path, {"hello.txt": "hi"})
    dest = tmp_path / "out"
    dest.mkdir()
    mod.extract_zip(str(zip_path), str(dest))
    assert (dest / "hello.txt").read_text() == "hi"


def test_extracts_nested_file(tmp_path, mod):
    zip_path = tmp_path / "b.zip"
    _make_zip(zip_path, {"sub/deep.txt": "content"})
    dest = tmp_path / "out"
    dest.mkdir()
    mod.extract_zip(str(zip_path), str(dest))
    assert (dest / "sub" / "deep.txt").read_text() == "content"


def test_extracts_multiple_files(tmp_path, mod):
    zip_path = tmp_path / "c.zip"
    _make_zip(zip_path, {"x.txt": "1", "y.txt": "2"})
    dest = tmp_path / "out"
    dest.mkdir()
    mod.extract_zip(str(zip_path), str(dest))
    assert (dest / "x.txt").read_text() == "1"
    assert (dest / "y.txt").read_text() == "2"
