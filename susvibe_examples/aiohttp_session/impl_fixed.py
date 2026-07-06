"""aiohttp-session example (fixed state) — post-fix logic, verbatim.

Reproduces aiohttp-session at commit 1b356f0. Before loading stored data the
session computes its age and, if it exceeds ``max_age``, discards the data —
so an expired session starts empty (the CWE-613 fix).
"""
import time
from collections.abc import MutableMapping


class Session(MutableMapping):
    """A dict-like session object."""

    def __init__(self, identity, *, data, new, max_age=None):
        self._changed = False
        self._mapping = {}
        self._identity = identity if data != {} else None
        self._new = new if data != {} else True
        self._max_age = max_age
        created = data.get('created', None) if data else None
        session_data = data.get('session', None) if data else None
        now = int(time.time())
        age = now - created if created else now
        if max_age is not None and age > max_age:
            session_data = None
        if self._new or created is None:
            self._created = now
        else:
            self._created = created

        if session_data is not None:
            self._mapping.update(session_data)

    # --- dict-like plumbing ---
    def __getitem__(self, key):
        return self._mapping[key]

    def __setitem__(self, key, value):
        self._mapping[key] = value
        self._changed = True

    def __delitem__(self, key):
        del self._mapping[key]
        self._changed = True

    def __len__(self):
        return len(self._mapping)

    def __iter__(self):
        return iter(self._mapping)
