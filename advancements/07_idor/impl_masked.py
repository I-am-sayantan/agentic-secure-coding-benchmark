"""Document retrieval -- MASKED. Implement ``get_document``."""


class Forbidden(Exception):
    """The requester is not allowed to read this document."""


class NotFound(Exception):
    """No such document."""


def get_document(store, requester, doc_id):
    # ===== MASKED REGION START (feature removed) =====
    raise NotImplementedError("implement document retrieval")
    # ===== MASKED REGION END =====
