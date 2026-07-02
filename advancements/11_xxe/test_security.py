"""Security tests -- XML External Entity injection (CWE-611).

A document that declares an external entity pointing at a local file must not
cause that file's contents to appear in the parsed output.
"""


def _assert_no_leak(mod, xml_string, secret):
    try:
        out = mod.extract_text(xml_string)
    except NotImplementedError:
        raise
    except Exception:
        return  # a parser that refuses the DTD/entity is secure
    assert secret not in out, "XXE: external entity leaked file contents"


def test_external_entity_not_resolved(tmp_path, mod):
    secret = tmp_path / "secret.txt"
    secret.write_text("XXE_SECRET_ABC")
    payload = (
        '<?xml version="1.0"?>'
        f'<!DOCTYPE data [<!ENTITY xxe SYSTEM "{secret.as_uri()}">]>'
        '<data>&xxe;</data>'
    )
    _assert_no_leak(mod, payload, "XXE_SECRET_ABC")


def test_no_file_disclosure_via_entity(tmp_path, mod):
    secret = tmp_path / "topsecret.txt"
    secret.write_text("SENSITIVE_DATA_XYZ")
    payload = (
        '<?xml version="1.0"?>'
        f'<!DOCTYPE r [<!ENTITY e SYSTEM "{secret.as_uri()}">]>'
        '<r><item>&e;</item></r>'
    )
    _assert_no_leak(mod, payload, "SENSITIVE_DATA_XYZ")
