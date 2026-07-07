```diff

diff --git a/nltk/downloader.py b/nltk/downloader.py
--- a/nltk/downloader.py
+++ b/nltk/downloader.py
@@ -2285,24 +2285,7 @@ def unzip(filename, root, verbose=True):
             raise Exception(message)
 
 
-def _unzip_iter(filename, root, verbose=True):
-    if verbose:
-        sys.stdout.write("Unzipping %s" % os.path.split(filename)[1])
-        sys.stdout.flush()
-
-    try:
-        zf = zipfile.ZipFile(filename)
-    except zipfile.BadZipFile:
-        yield ErrorMessage(filename, "Error with downloaded zip file")
-        return
-    except Exception as e:
-        yield ErrorMessage(filename, e)
-        return
-
-    zf.extractall(root)
-
-    if verbose:
-        print()
+
 
 
 ######################################################################
```
