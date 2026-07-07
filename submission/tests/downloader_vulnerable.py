# Natural Language Toolkit: Corpus & Model Downloader
#
# Copyright (C) 2001-2025 NLTK Project
# Author: Edward Loper <edloper@gmail.com>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT
"""
VULNERABLE excerpt of ``nltk/downloader.py`` (tag ``3.9.2``, pre-fix).

Vulnerability: CVE-2025-14009 / GHSA-7p94-766c-hgjp (Zip Slip -> arbitrary
code execution, CWE-94). Fixed upstream in 3.9.3 by PR nltk/nltk#3468.

Only the code required to see ``_unzip_iter`` in its real context is
reproduced here: the module imports it uses, the message classes it
yields, and the ``unzip`` caller. Every line below is copied verbatim
from the upstream file (unrelated module imports have been trimmed).
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
# Unzipping  (verbatim from nltk/downloader.py)
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
    if verbose:
        sys.stdout.write("Unzipping %s" % os.path.split(filename)[1])
        sys.stdout.flush()

    try:
        zf = zipfile.ZipFile(filename)
    except zipfile.BadZipFile:
        yield ErrorMessage(filename, "Error with downloaded zip file")
        return
    except Exception as e:
        yield ErrorMessage(filename, e)
        return

    zf.extractall(root)

    if verbose:
        print()
