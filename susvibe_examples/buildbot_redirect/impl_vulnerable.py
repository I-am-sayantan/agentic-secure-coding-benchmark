"""buildbot redirect example (vulnerable state) — pre-fix logic.

The redirect URL is stored raw. An attacker who controls the URL can embed
CR/LF and inject extra HTTP response headers (CVE-2019-7313, CWE-93).
"""


def to_bytes(s):
    return s.encode("utf-8") if isinstance(s, str) else s


class Redirect(Exception):
    def __init__(self, url):
        super().__init__(302, "redirect")
        self.url = to_bytes(url)          # <-- raw, no CR/LF stripping
