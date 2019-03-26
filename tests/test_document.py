import pytest

from lxml_domesque import Document, InvalidOperation, TagNode


def test_cleanup_namespaces():
    document = Document('<root xmlns="D" xmlns:y="Y"><x:a xmlns:x="X"/><b/></root>')

    document.cleanup_namespaces(retain_prefixes=("y",))
    assert str(document) == '<root xmlns="D" xmlns:y="Y"><x:a xmlns:x="X"/><b/></root>'

    document.cleanup_namespaces()
    assert str(document) == '<root xmlns="D"><x:a xmlns:x="X"/><b/></root>'

    document.cleanup_namespaces(namespaces={None: "X", "d": "D"})
    assert str(document) == '<root xmlns="D"><x:a xmlns:x="X"/><b/></root>'


def test_contains():
    document_a = Document("<root><a/></root>")
    document_b = Document("<root><a/></root>")

    assert document_a.root[0] in document_a
    assert document_a.root[0] not in document_b


def test_invalid_document():
    with pytest.raises(ValueError):
        Document(0)


def test_set_root():
    document = Document("<root><node/></root>")
    document.root = document.root[0].detach()
    assert str(document) == "<node/>"

    document_2 = Document("<root><replacement/>parts</root>")
    with pytest.raises(InvalidOperation):
        document.root = document_2.root[0]


def test_xpath(files_path):
    document = Document(files_path / "marx_manifestws_1848.TEI-P5.xml")

    for i, page_break in enumerate(document.xpath(".//pb")):
        assert isinstance(page_break, TagNode)
        assert page_break.qualified_name == "{http://www.tei-c.org/ns/1.0}pb"

    assert i == 22

    for j, page_break in enumerate(document.xpath('.//pb[@n="I"]')):
        assert isinstance(page_break, TagNode)
        assert page_break.qualified_name == "{http://www.tei-c.org/ns/1.0}pb"
        assert page_break.attributes["n"] == "I"

    assert j == 0


def test_invalid_xpath(files_path):
    document = Document(files_path / "marx_manifestws_1848.TEI-P5.xml")

    with pytest.raises(InvalidOperation):
        tuple(document.xpath(".//pb/@facs"))

    with pytest.raises(InvalidOperation):
        tuple(document.xpath(".//comment()"))
