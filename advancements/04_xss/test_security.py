"""Security tests -- cross-site scripting (CWE-79).

Markup in user input must be escaped, not emitted as live HTML.
"""


def test_script_tag_escaped(mod):
    out = mod.render_comment("eve", "<script>alert('xss')</script>")
    assert "<script>" not in out, "XSS: raw <script> tag rendered"
    assert "&lt;script&gt;" in out


def test_image_onerror_escaped(mod):
    out = mod.render_comment("eve", '"><img src=x onerror=alert(1)>')
    assert "<img" not in out, "XSS: raw <img> tag rendered"


def test_author_field_escaped(mod):
    out = mod.render_comment("<b>eve</b>", "hi")
    assert "<b>" not in out, "XSS: raw markup in author field rendered"
