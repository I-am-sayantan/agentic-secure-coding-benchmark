"""Comment rendering -- VULNERABLE (CWE-79 Cross-Site Scripting).

User-supplied ``username`` and ``comment`` are interpolated straight into HTML.
A comment containing ``<script>`` is rendered as live markup in the browser.
"""


def render_comment(username, comment):
    return (
        f'<div class="comment">'
        f'<span class="author">{username}</span>: {comment}'
        f'</div>'
    )
