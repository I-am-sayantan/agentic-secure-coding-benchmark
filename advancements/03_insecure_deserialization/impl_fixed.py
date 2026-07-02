"""Session (de)serialization -- FIXED (JSON).

Uses JSON, a pure data format with no code-execution semantics. A crafted
byte stream can at worst fail to parse; it can never run code.
"""
import json


def dump_session(obj):
    return json.dumps(obj).encode("utf-8")


def load_session(data):
    return json.loads(data.decode("utf-8"))
