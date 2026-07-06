"""wagtail link example (fixed state) — post-fix logic.

The external URL is passed through ``check_url`` before being placed in the
``href``, so unsafe schemes such as ``javascript:`` are dropped (the
CVE-2021-29434 fix).
"""
from dom import create_element, check_url


def link_entity(props):
    id_ = props.get("id")
    link_props = {}
    if id_ is not None:
        link_props["linktype"] = "page"
        link_props["id"] = id_
    else:
        link_props["href"] = check_url(props.get("url"))   # <-- sanitised
    return create_element("a", link_props, props["children"])
