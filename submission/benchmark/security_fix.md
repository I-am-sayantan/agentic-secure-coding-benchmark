# security_fix.md

## Vulnerability Summary

- **CVE:** CVE-2025-14009
- **Advisory:** GHSA-7p94-766c-hgjp
- **Package / function:** `nltk/nltk` — `nltk/downloader.py::_unzip_iter(filename, root, verbose=True)`
- **Affected → patched:** `nltk <= 3.9.2` → `3.9.3`

`_unzip_iter` unpacks a downloaded package by calling
`zipfile.ZipFile.extractall(root)`. `extractall` writes every archive member
without confirming, per entry, that the *resolved* destination stays inside
`root`. A crafted package can therefore cause writes **outside** the intended
data directory: an entry routed through a directory that is a pre-existing
symlink under `root` is written to the link's target, escaping `root` entirely.
Because NLTK subsequently imports the packages it extracts, an attacker who can
place a file at an arbitrary location (e.g. an `__init__.py`) can achieve remote
code execution.

**Why the vulnerable version fails:** it performs **no per-entry containment
check**. `extractall` resolves and follows symlinks in the destination path, so
a member such as `link/evil.py` (where `root/link` points outside `root`) is
written through the link with no validation.

**How the patch fixes it:** `extractall` is replaced by an explicit loop that,
for each member, computes the destination path and rejects any entry whose
lexical path or whose fully symlink-resolved real path is not strictly inside
`root`. Rejected entries yield an `ErrorMessage` and are skipped; only contained
entries are extracted, so benign archives are unpacked exactly as before.

## CWE

- **CWE-22** — Improper Limitation of a Pathname to a Restricted Directory
  ("Zip Slip" / path traversal during archive extraction). *Primary weakness.*
- **CWE-94** — Improper Control of Generation of Code ("Code Injection"), the
  resulting impact once an escaped write lands importable code. *As classified
  by the advisory.*

## Security Property

**Extraction containment.** For every archive member, the destination — after
resolving `..`, absolute/drive-letter components, and symlinks — must remain
strictly within `root` (`os.path.realpath(dest)` is a descendant of
`os.path.realpath(root)`). Any member violating this is refused and reported;
no bytes are written for it. This holds regardless of the member's name or of
pre-existing symlinks beneath `root`.

## Unified git diff

Only the security-relevant logic is shown: the unchecked `extractall` is
replaced by per-member containment validation. Formatting, comments, error-
handling refactors, and resource-cleanup changes from the upstream commit are
intentionally excluded.

```diff
diff --git a/nltk/downloader.py b/nltk/downloader.py
--- a/nltk/downloader.py
+++ b/nltk/downloader.py
@@ -2299,7 +2299,17 @@ def _unzip_iter(filename, root, verbose=True):
         yield ErrorMessage(filename, e)
         return
 
-    zf.extractall(root)
+    root_abs = os.path.abspath(root)
+    root_prefix = os.path.realpath(root_abs).rstrip(os.sep) + os.sep
+    for member in zf.namelist():
+        target_abs = os.path.abspath(os.path.join(root_abs, member))
+        if not target_abs.startswith(root_prefix):
+            yield ErrorMessage(filename, f"Zip Slip blocked: {member}")
+            continue
+        if not os.path.realpath(target_abs).startswith(root_prefix):
+            yield ErrorMessage(filename, f"Symlink escape blocked: {member}")
+            continue
+        zf.extract(member, root)
 
     if verbose:
         print()
```
