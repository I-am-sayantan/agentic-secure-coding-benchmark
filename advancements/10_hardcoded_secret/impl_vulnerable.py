"""API key retrieval -- VULNERABLE (CWE-798 hardcoded credentials).

The live key is embedded in source. Anyone with read access to the code (repo
history, backups, a container image) obtains the credential.
"""


def get_api_key():
    return "sk-live-9f8e7d6c5b4a3f2e1d0c9b8a7SECRET"
