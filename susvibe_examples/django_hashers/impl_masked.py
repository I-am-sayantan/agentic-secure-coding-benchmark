"""django hashers example (masked state) — feature removed."""
from hashers_base import (  # noqa: F401
    is_password_usable, identify_hasher, verify_hash, make_password,
)


def verify_password(password, encoded, preferred="default"):
    raise NotImplementedError("implement verify_password")
