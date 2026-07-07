# Feature Golden — reference implementation of `_unzip_iter`

Restores `nltk/downloader.py::_unzip_iter`, the package-extraction helper that
`feature_mask.md` removes, using the upstream fixed implementation from PR
`nltk/nltk#3468` (commit `1056b323`). Applying `feature_mask.md` and then this
diff to the vulnerable revision reproduces the upstream fixed function.

```diff
diff --git a/nltk/downloader.py b/nltk/downloader.py
--- a/nltk/downloader.py
+++ b/nltk/downloader.py
@@ -2285,9 +2285,64 @@ def unzip(filename, root, verbose=True):
             raise Exception(message)
 
 
-
-
-
+def _unzip_iter(filename, root, verbose=True):
+    """
+    Secure ZIP extraction with minimal behavioural changes.
+
+    - Prevents classic Zip-Slip (.., absolute paths, drive letters)
+    - Prevents writes through pre-existing symlinks
+    - Preserves original extraction behaviour for valid archives
+    """
+
+    if verbose:
+        sys.stdout.write("Unzipping %s" % os.path.split(filename)[1])
+        sys.stdout.flush()
+
+    try:
+        zf = zipfile.ZipFile(filename)
+    except Exception as e:
+        yield ErrorMessage(filename, e)
+        return
+
+    # Canonical root
+    root_abs = os.path.abspath(root)
+    root_real = os.path.realpath(root_abs)
+    root_prefix = root_real.rstrip(os.sep) + os.sep
+
+    # Ensure the extraction root directory exists
+    os.makedirs(root, exist_ok=True)
+
+    try:
+        for member in zf.namelist():
+
+            # Construct target path
+            raw_target = os.path.join(root_abs, member)
+            target_abs = os.path.abspath(raw_target)
+
+            # Zip-Slip check (absolute/traversal/drive-letter cases)
+            if not target_abs.startswith(root_prefix):
+                yield ErrorMessage(filename, f"Zip Slip blocked: {member}")
+                continue
+
+            # Symlink-escape check
+            target_real = os.path.realpath(target_abs)
+            if not target_real.startswith(root_prefix):
+                yield ErrorMessage(filename, f"Symlink escape blocked: {member}")
+                continue
+
+            # Safe extraction
+            try:
+                zf.extract(member, root)
+            except Exception as e:
+                yield ErrorMessage(filename, f"Extraction error for {member}: {e}")
+                continue
+    finally:
+        zf.close()
+
+    if verbose:
+        print()
+
+
 ######################################################################
 # Index Builder
 ######################################################################
```
