"""buildbot redirect example (fixed state) — post-fix logic.

Before storing the redirect URL it strips a CR/LF and everything after it, so
no extra HTTP headers can be injected (the CVE-2019-7313 fix).
"""
import re

_CR_LF_RE = re.compile(rb"[\r\n]+.*")


def to_bytes(s):
    return s.encode("utf-8") if isinstance(s, str) else s


def protect_redirect_url(url):
    return _CR_LF_RE.sub(b"", url)


class Redirect(Exception):
    def __init__(self, url):
        super().__init__(302, "redirect")
        self.url = protect_redirect_url(to_bytes(url))   # <-- CR/LF stripped
