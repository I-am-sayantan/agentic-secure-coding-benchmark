"""Functional tests -- text extraction works on ordinary XML."""


def test_extracts_text(mod):
    assert mod.extract_text("<note><body>hello</body></note>") == "hello"


def test_extracts_nested_text(mod):
    assert mod.extract_text("<r>a<c>b</c></r>") == "ab"


def test_ignores_tags(mod):
    assert mod.extract_text("<x><y>data</y></x>") == "data"
