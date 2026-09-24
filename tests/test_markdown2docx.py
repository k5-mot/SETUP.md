#!/usr/bin/env python3
"""MarkdownからDOCXへの直接変換契約を回帰Testする。"""

from __future__ import annotations

import hashlib
import logging
import subprocess
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PUBLICS = REPOSITORY_ROOT / "openspec" / "publics"
REFERENCE_DOC = (
    REPOSITORY_ROOT
    / ".agents"
    / "skills"
    / "markdown2docx"
    / "references"
    / "template.docx"
)
DOCUMENTS = {"prd": "QR-001", "hld": "ADR-001"}
WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NAMESPACES = {"w": WORD_NAMESPACE}


def word_attribute(name: str) -> str:
    """WordprocessingML属性名を完全修飾する。"""
    return f"{{{WORD_NAMESPACE}}}{name}"


def style_by_id(styles: ET.Element, style_id: str) -> ET.Element:
    """指定したWord Styleを返す。"""
    style = styles.find(f".//w:style[@w:styleId='{style_id}']", NAMESPACES)
    if style is None:
        raise AssertionError(f"missing Word style: {style_id}")
    return style


def yaml_title(source: Path) -> str:
    """先頭YAML Metadataから空でないTitleを返す。"""
    lines = source.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError(f"missing leading YAML metadata: {source}")
    for line in lines[1:]:
        if line == "---":
            break
        key, separator, value = line.partition(":")
        if key == "title" and separator and value.strip().strip("\"'"):
            return value.strip().strip("\"'")
    raise AssertionError(f"missing non-empty YAML title: {source}")


class MarkdownToDocxTests(unittest.TestCase):
    """PRDとHLDの配布用DOCX生成を検証する。"""

    def test_representative_documents_are_generated(self) -> None:
        """Pandocだけで代表文書の書式契約を満たすDOCXが生成される。"""
        with tempfile.TemporaryDirectory() as directory:
            output_root = Path(directory)
            for name, representative_id in DOCUMENTS.items():
                with self.subTest(document=name):
                    source = PUBLICS / f"{name}.md"
                    output = output_root / f"{name}.docx"
                    title = yaml_title(source)
                    before = hashlib.sha256(source.read_bytes()).digest()

                    subprocess.run(
                        [
                            "pandoc",
                            str(source),
                            "--from=gfm+implicit_figures",
                            "--to=docx",
                            "--standalone",
                            f"--reference-doc={REFERENCE_DOC}",
                            "--toc",
                            "--toc-depth=6",
                            "--lof",
                            "--lot",
                            "--metadata=toc-title:目次",
                            "--metadata=lof-title:図一覧",
                            "--metadata=lot-title:表一覧",
                            f"--output={output}",
                        ],
                        check=True,
                        capture_output=True,
                        text=True,
                    )

                    self.assertTrue(output.is_file())
                    self.assertGreater(output.stat().st_size, 0)
                    after = hashlib.sha256(source.read_bytes()).digest()
                    self.assertEqual(before, after)
                    with ZipFile(output) as archive:
                        document = ET.fromstring(archive.read("word/document.xml"))
                        styles = ET.fromstring(archive.read("word/styles.xml"))
                        settings = ET.fromstring(archive.read("word/settings.xml"))

                    document_text = "".join(document.itertext())
                    self.assertIn(representative_id, document_text)

                    title_paragraphs = []
                    for paragraph in document.findall(".//w:p", NAMESPACES):
                        paragraph_style = paragraph.find("w:pPr/w:pStyle", NAMESPACES)
                        if (
                            paragraph_style is not None
                            and paragraph_style.get(word_attribute("val")) == "Title"
                        ):
                            title_paragraphs.append(paragraph)
                    self.assertEqual(len(title_paragraphs), 1)
                    self.assertIn(title, "".join(title_paragraphs[0].itertext()))

                    field_codes = {
                        " ".join(node.text.split())
                        for node in document.findall(".//w:instrText", NAMESPACES)
                        if node.text
                    }
                    self.assertIn('TOC \\o "1-6" \\h \\z \\u', field_codes)
                    self.assertIn('TOC \\h \\z \\t "Image Caption" \\c', field_codes)
                    self.assertIn('TOC \\h \\z \\t "Table Caption" \\c', field_codes)

                    update_fields = settings.find("w:updateFields", NAMESPACES)
                    self.assertIsNotNone(update_fields)
                    self.assertIn(
                        update_fields.get(word_attribute("val")), {"1", "true"}
                    )

                    for style_id in ("Normal", "BodyText", "Table"):
                        size = style_by_id(styles, style_id).find(
                            "w:rPr/w:sz", NAMESPACES
                        )
                        self.assertIsNotNone(size)
                        self.assertEqual(size.get(word_attribute("val")), "20")

                    for style_id in ("Heading1", "TOCHeading"):
                        page_break = style_by_id(styles, style_id).find(
                            "w:pPr/w:pageBreakBefore", NAMESPACES
                        )
                        self.assertIsNotNone(page_break)

                    table_alignment = style_by_id(styles, "Table").find(
                        "w:tblPr/w:jc", NAMESPACES
                    )
                    self.assertIsNotNone(table_alignment)
                    self.assertEqual(
                        table_alignment.get(word_attribute("val")), "center"
                    )

                    tables = document.findall(".//w:tbl", NAMESPACES)
                    self.assertGreater(len(tables), 0)
                    for table in tables:
                        table_style = table.find("w:tblPr/w:tblStyle", NAMESPACES)
                        self.assertIsNotNone(table_style)
                        self.assertEqual(
                            table_style.get(word_attribute("val")), "Table"
                        )
                        first_row = table.find("w:tr", NAMESPACES)
                        self.assertIsNotNone(first_row)
                        self.assertIsNotNone(
                            first_row.find("w:trPr/w:tblHeader", NAMESPACES)
                        )


def main() -> int:
    """Test Suiteを実行して成否を返す。"""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MarkdownToDocxTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
