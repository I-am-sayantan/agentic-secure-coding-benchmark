r"""Product-code validation -- FIXED (linear pattern).

``^\w+$`` accepts exactly the same strings but has no nested quantifier, so it
runs in linear time and cannot be driven into catastrophic backtracking.
"""
import re

_PATTERN = re.compile(r"^\w+$")


def is_match(text):
    return _PATTERN.match(text) is not None
