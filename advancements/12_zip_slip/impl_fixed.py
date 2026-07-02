"""Archive extraction -- FIXED (destination containment enforced).

Each member's final path is resolved and checked to stay inside the
destination directory before anything is written; escaping members are refused.
"""
import os
import zipfile


def extract_zip(zip_path, dest_dir):
    dest_root = os.path.realpath(dest_dir)
    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            target = os.path.realpath(os.path.join(dest_root, name))
            if target != dest_root and not target.startswith(dest_root + os.sep):
                raise ValueError(f"unsafe path in archive: {name}")
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(archive.read(name))
