"""buildbot redirect example (masked state) — feature removed."""


def to_bytes(s):
    return s.encode("utf-8") if isinstance(s, str) else s


class Redirect(Exception):
    def __init__(self, url):
        raise NotImplementedError("implement Redirect")
