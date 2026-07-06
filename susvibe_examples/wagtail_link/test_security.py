"""Security tests — javascript: URLs must be neutralised (CWE-79 XSS).

Vulnerable: the raw ``javascript:`` URL ends up in the href (FAIL).
Fixed: ``check_url`` drops the unsafe scheme (PASS).
"""


def test_javascript_url_blocked(mod):
    html = mod.link_entity({"url": "javascript:alert(1)", "children": "x"})
    assert "javascript:" not in html, "javascript: URL must not reach the href"


def test_data_uri_blocked(mod):
    html = mod.link_entity({"url": "data:text/html,<script>1</script>", "children": "x"})
    assert "data:text/html" not in html
