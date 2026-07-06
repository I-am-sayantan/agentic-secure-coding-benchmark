"""wagtail link example (vulnerable state) — pre-fix logic.

The external-link branch puts the user-supplied URL straight into the ``href``
with no scheme checking, so a ``javascript:`` URL becomes a stored-XSS payload
(CVE-2021-29434, CWE-79).
"""
from dom import create_element


def link_entity(props):
    id_ = props.get("id")
    link_props = {}
    if id_ is not None:
        link_props["linktype"] = "page"
        link_props["id"] = id_
    else:
        link_props["href"] = props.get("url")        # <-- raw, unchecked
    return create_element("a", link_props, props["children"])
