"""Document retrieval -- VULNERABLE (CWE-639 Missing Authorization / IDOR).

Any authenticated caller can fetch any document by id; ownership is never
checked, so users can read each other's private documents.
"""


class Forbidden(Exception):
    """The requester is not allowed to read this document."""


class NotFound(Exception):
    """No such document."""


def get_document(store, requester, doc_id):
    if doc_id not in store:
        raise NotFound()
    return store[doc_id]["content"]
