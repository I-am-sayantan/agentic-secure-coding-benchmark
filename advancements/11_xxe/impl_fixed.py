"""XML text extraction -- FIXED (DTDs rejected, external entities off).

Documents that declare a DTD or entities are refused outright, and external
general/parameter entity resolution is disabled, so no external file can be
pulled into the output.
"""
import io
import xml.sax
from xml.sax.handler import feature_external_ges, feature_external_pes


class _Collector(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.parts = []

    def characters(self, content):
        self.parts.append(content)


def extract_text(xml_string):
    if "<!DOCTYPE" in xml_string or "<!ENTITY" in xml_string:
        raise ValueError("DTDs and entity declarations are not permitted")
    parser = xml.sax.make_parser()
    parser.setFeature(feature_external_ges, False)
    parser.setFeature(feature_external_pes, False)
    handler = _Collector()
    parser.setContentHandler(handler)
    source = xml.sax.InputSource()
    source.setByteStream(io.BytesIO(xml_string.encode("utf-8")))
    parser.parse(source)
    return "".join(handler.parts)
