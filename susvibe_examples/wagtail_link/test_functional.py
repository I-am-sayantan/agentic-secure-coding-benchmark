"""Functional tests — link conversion works (vulnerable + fixed pass)."""


def test_internal_page_link(mod):
    html = mod.link_entity({"id": 42, "children": "home"})
    assert 'linktype="page"' in html
    assert 'id="42"' in html
    assert ">home<" in html


def test_external_http_link(mod):
    html = mod.link_entity({"url": "http://example.com", "children": "site"})
    assert 'href="http://example.com"' in html
    assert ">site<" in html
