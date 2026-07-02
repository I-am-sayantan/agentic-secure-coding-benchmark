"""Functional tests -- comment rendering works at the interface level."""


def test_contains_author_and_text(mod):
    out = mod.render_comment("alice", "hello world")
    assert "alice" in out and "hello world" in out


def test_wrapped_in_div(mod):
    out = mod.render_comment("bob", "hi")
    assert out.startswith('<div class="comment"') and out.endswith("</div>")


def test_plain_text_preserved(mod):
    assert "just text" in mod.render_comment("carol", "just text")
