# Missing Package Extraction Helper in the NLTK Downloader

## Current Issue

The NLTK downloader (`nltk/downloader.py`) can fetch corpus and model packages
as `.zip` files, but it can no longer unpack them. The public `unzip()` function
delegates the actual work to a helper generator, `_unzip_iter(filename, root,
verbose)`, and that helper is currently missing from the module.

When `unzip()` is called on a freshly downloaded package, it loops over the
messages produced by `_unzip_iter(...)`. Because the function does not exist, the
call raises a `NameError` and nothing is written to the data directory.
Downloaded packages stay as unopened `.zip` files, and `nltk.data` cannot find
the corpora or models they contain — every download that ends in an "unzip" step
is broken until the helper is restored.

## Expected Behavior

The module should provide a `_unzip_iter(filename, root, verbose=True)` generator
that:

1. **Extracts the archive**: Opens the zip file at `filename` and writes every
   entry it contains into the destination directory `root`, recreating the
   archive's internal folder layout. For example, a `treebank.zip` whose entries
   live under `treebank/` should leave its files on disk under `<root>/treebank/`.
2. **Prints a status line**: When `verbose` is `True`, writes an
   `Unzipping <archive-name>` message to standard output as it begins, and
   completes the line when it finishes.
3. **Reports unreadable archives**: If `filename` is corrupt or cannot be opened
   as a zip file, yields an `ErrorMessage(filename, ...)` describing the failure
   and stops, instead of letting the exception propagate out of `unzip()`.
4. **Works as a generator for `unzip()`**: Yields its status and error messages
   so the existing `unzip()` wrapper can consume them and raise if an
   `ErrorMessage` is produced.

The helper should accept `filename` (the downloaded `.zip` file), `root` (the
directory its contents belong in), and a `verbose` flag. On success it should
leave the fully unpacked package on disk under `root`, ready for the rest of
NLTK to load.
