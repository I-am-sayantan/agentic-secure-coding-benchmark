"""Archive extraction -- VULNERABLE (CWE-22 Zip Slip).

Each member name is joined onto the destination and written without checking
where it lands, so a member named ``../evil`` is written outside the
destination directory.
"""
import os
import zipfile


def extract_zip(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            target = os.path.join(dest_dir, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(archive.read(name))
