"""Functional tests -- directory listing works at the interface level."""


def test_lists_single_file(tmp_path, mod):
    (tmp_path / "readme.txt").write_text("x")
    assert "readme.txt" in mod.list_dir(str(tmp_path))


def test_lists_multiple_files(tmp_path, mod):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("y")
    out = mod.list_dir(str(tmp_path))
    assert "a.txt" in out and "b.txt" in out


def test_lists_subdirectory(tmp_path, mod):
    (tmp_path / "sub").mkdir()
    assert "sub" in mod.list_dir(str(tmp_path))
