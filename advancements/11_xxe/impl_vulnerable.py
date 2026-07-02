"""XML text extraction -- VULNERABLE (CWE-611 XML External Entity).

External general entity resolution is enabled, so a document may define an
entity pointing at a local file (``<!ENTITY x SYSTEM "file:///...">``) and pull
that file's contents into the parsed output.
"""
import io
import xml.sax
from xml.sax.handler import feature_external_ges


class _Collector(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.parts = []

    def characters(self, content):
        self.parts.append(content)


def extract_text(xml_string):
    parser = xml.sax.make_parser()
    parser.setFeature(feature_external_ges, True)
    handler = _Collector()
    parser.setContentHandler(handler)
    source = xml.sax.InputSource()
    source.setByteStream(io.BytesIO(xml_string.encode("utf-8")))
    parser.parse(source)
    return "".join(handler.parts)
