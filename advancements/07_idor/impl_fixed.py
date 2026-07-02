"""Document retrieval -- FIXED (ownership enforced).

The requester must own the document; otherwise the request is refused. Missing
documents are reported as not found.
"""


class Forbidden(Exception):
    """The requester is not allowed to read this document."""


class NotFound(Exception):
    """No such document."""


def get_document(store, requester, doc_id):
    if doc_id not in store:
        raise NotFound()
    document = store[doc_id]
    if document["owner"] != requester:
        raise Forbidden()
    return document["content"]
