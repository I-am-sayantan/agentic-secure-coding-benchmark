"""Session (de)serialization -- VULNERABLE (CWE-502).

Uses ``pickle`` for both directions. ``pickle.loads`` will execute arbitrary
code embedded in a crafted byte stream, so untrusted session data leads to
remote code execution.
"""
import pickle


def dump_session(obj):
    return pickle.dumps(obj)


def load_session(data):
    return pickle.loads(data)
