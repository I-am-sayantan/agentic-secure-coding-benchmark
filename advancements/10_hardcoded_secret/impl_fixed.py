"""API key retrieval -- FIXED (from the environment).

The key is read from the environment at call time and never stored in source.
If it is not configured, the function refuses rather than returning a baked-in
fallback.
"""
import os


def get_api_key():
    try:
        return os.environ["APP_API_KEY"]
    except KeyError:
        raise RuntimeError("APP_API_KEY is not configured")
