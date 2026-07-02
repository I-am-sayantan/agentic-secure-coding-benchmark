r"""Product-code validation -- VULNERABLE (CWE-1333 ReDoS).

The pattern ``^(\w+)+$`` has nested quantifiers. On a long run of word
characters followed by a non-matching character it backtracks catastrophically
(exponential time), so a short crafted input can hang the process.
"""
import re

_PATTERN = re.compile(r"^(\w+)+$")


def is_match(text):
    return _PATTERN.match(text) is not None
