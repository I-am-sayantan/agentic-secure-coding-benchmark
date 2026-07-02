"""Comment rendering -- FIXED (HTML-escaped).

Both fields are HTML-escaped before interpolation, so any markup in user input
is rendered as inert text rather than executed.
"""
import html


def render_comment(username, comment):
    author = html.escape(username)
    body = html.escape(comment)
    return (
        f'<div class="comment">'
        f'<span class="author">{author}</span>: {body}'
        f'</div>'
    )
