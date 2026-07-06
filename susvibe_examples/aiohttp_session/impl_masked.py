"""aiohttp-session example (masked state) — the agent's starting point.

The feature (the body of ``Session.__init__``) has been removed. Both the
functional and security suites fail until it is reimplemented.
"""
import time
from collections.abc import MutableMapping


class Session(MutableMapping):
    """A dict-like session object."""

    def __init__(self, identity, *, data, new, max_age=None):
        raise NotImplementedError("implement Session.__init__")

    # --- dict-like plumbing (shared, not part of the masked feature) ---
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
