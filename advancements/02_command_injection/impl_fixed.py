"""Directory listing -- FIXED (no shell).

The listing is produced directly by the OS API. No shell is spawned, so shell
metacharacters in ``path`` have no special meaning and cannot run commands.
"""
import os


def list_dir(path):
    return "\n".join(os.listdir(path))
