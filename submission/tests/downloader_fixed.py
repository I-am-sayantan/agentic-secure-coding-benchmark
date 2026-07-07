# Natural Language Toolkit: Corpus & Model Downloader
#
# Copyright (C) 2001-2025 NLTK Project
# Author: Edward Loper <edloper@gmail.com>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT
"""
FIXED excerpt of ``nltk/downloader.py`` (post-fix, tag ``3.9.3``).

The secure ``_unzip_iter`` from PR nltk/nltk#3468 (commit 1056b323). Only the
code needed to see ``_unzip_iter`` in context is reproduced: the imports it
uses, the message classes it yields, and the ``unzip`` caller. The function
body is copied faithfully from the merged fix.
"""
import os
import sys
import zipfile


######################################################################
# Message Passing Objects  (verbatim from nltk/downloader.py)
######################################################################


class DownloaderMessage:
    """A status message object, used by ``incr_download`` to
    communicate its progress."""


class ErrorMessage(DownloaderMessage):
    """Data server encountered an error"""

    def __init__(self, package, message):
        self.package = package
        if isinstance(message, Exception):
            self.message = str(message)
        else:
            self.message = message


class ProgressMessage(DownloaderMessage):
    """Indicates how much progress the data server has made"""

    def __init__(self, progress):
        self.progress = progress


######################################################################
# Unzipping  (verbatim from nltk/downloader.py, post-fix)
######################################################################

# change this to periodically yield progress messages?
# [xx] get rid of topdir parameter -- we should be checking
# this when we build the index, anyway.
def unzip(filename, root, verbose=True):
    """
    Extract the contents of the zip file ``filename`` into the
    directory ``root``.
    """
    for message in _unzip_iter(filename, root, verbose):
        if isinstance(message, ErrorMessage):
            raise Exception(message)


def _unzip_iter(filename, root, verbose=True):
    """
    Secure ZIP extraction with minimal behavioural changes.

    - Prevents classic Zip-Slip (.., absolute paths, drive letters)
    - Prevents writes through pre-existing symlinks
    - Preserves original extraction behaviour for valid archives
    """

    if verbose:
        sys.stdout.write("Unzipping %s" % os.path.split(filename)[1])
        sys.stdout.flush()

    try:
        zf = zipfile.ZipFile(filename)
    except Exception as e:
        yield ErrorMessage(filename, e)
        return

    # Canonical root
    root_abs = os.path.abspath(root)
    root_real = os.path.realpath(root_abs)
    root_prefix = root_real.rstrip(os.sep) + os.sep

    # Ensure the extraction root directory exists
    os.makedirs(root, exist_ok=True)

    try:
        for member in zf.namelist():

            # Construct target path
            raw_target = os.path.join(root_abs, member)
            target_abs = os.path.abspath(raw_target)

            # Zip-Slip check (absolute/traversal/drive-letter cases)
            if not target_abs.startswith(root_prefix):
                yield ErrorMessage(filename, f"Zip Slip blocked: {member}")
                continue

            # Symlink-escape check
            target_real = os.path.realpath(target_abs)
            if not target_real.startswith(root_prefix):
                yield ErrorMessage(filename, f"Symlink escape blocked: {member}")
                continue

            # Safe extraction
            try:
                zf.extract(member, root)
            except Exception as e:
                yield ErrorMessage(filename, f"Extraction error for {member}: {e}")
                continue
    finally:
        zf.close()

    if verbose:
        print()
