#!/usr/bin/env python3
"""Markdownから配布用DOCXへの変換契約を回帰Testする。"""

from __future__ import annotations

import hashlib
import logging
import subprocess
import sys
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
FINALIZER = REPOSITORY_ROOT / ".agents" / "skills" / "markdown2docx" / "main.py"
RELEASE_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "release-hld-docx.yml"
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


def style_names(styles: ET.Element) -> dict[str, str]:
    """Style IDと表示名の対応を返す。"""
    names = {}
    for style in styles.findall(".//w:style", NAMESPACES):
        name = style.find("w:name", NAMESPACES)
        if name is not None:
            names[style.get(word_attribute("styleId"), "")] = name.get(
                word_attribute("val"), ""
            )
    return names


def paragraph_style_name(paragraph: ET.Element, names: dict[str, str]) -> str:
    """段落Styleの表示名を返す。"""
    style = paragraph.find("w:pPr/w:pStyle", NAMESPACES)
    if style is None:
        return ""
    return names.get(style.get(word_attribute("val"), ""), "")


def paragraph_text(paragraph: ET.Element) -> str:
    """段落の表示Textを返す。"""
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NAMESPACES))


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
        """代表文書が表示内容を更新した配布用DOCXとして生成される。"""
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
                    subprocess.run(
                        [sys.executable, str(FINALIZER), "finalize", str(output)],
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    subprocess.run(
                        [sys.executable, str(FINALIZER), "refresh", str(output)],
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

                    document_text = "".join(document.itertext())
                    self.assertIn(representative_id, document_text)
                    names = style_names(styles)
                    paragraphs = document.findall(".//w:p", NAMESPACES)
                    texts = [paragraph_text(paragraph) for paragraph in paragraphs]
                    styles_by_paragraph = [
                        paragraph_style_name(paragraph, names)
                        for paragraph in paragraphs
                    ]

                    title_paragraphs = []
                    for paragraph, style_name in zip(
                        paragraphs, styles_by_paragraph, strict=True
                    ):
                        if style_name.lower() == "title":
                            title_paragraphs.append(paragraph)
                    self.assertEqual(len(title_paragraphs), 1)
                    self.assertIn(title, paragraph_text(title_paragraphs[0]))

                    self.assertNotIn("List of Figures", texts)
                    self.assertNotIn("List of Tables", texts)
                    for navigation_title in ("目次", "図一覧", "表一覧"):
                        self.assertIn(navigation_title, texts)

                    toc_start = texts.index("目次")
                    figure_start = texts.index("図一覧")
                    table_start = texts.index("表一覧")
                    toc_entries = [
                        text.strip()
                        for text in texts[toc_start + 1 : figure_start]
                        if text.strip()
                    ]
                    self.assertTrue(toc_entries)
                    figure_text = "".join(texts[figure_start + 1 : table_start])
                    self.assertTrue(figure_text.strip())

                    tables = document.findall(".//w:tbl", NAMESPACES)
                    self.assertGreater(len(tables), 0)
                    captions = [
                        text
                        for text, style_name in zip(
                            texts, styles_by_paragraph, strict=True
                        )
                        if style_name.lower() in {"表タイトル", "table caption"}
                    ]
                    self.assertEqual(len(captions), len(tables))
                    self.assertTrue(
                        all(caption.startswith("表") for caption in captions)
                    )
                    first_body_heading = next(
                        index
                        for index in range(table_start + 1, len(paragraphs))
                        if texts[index].strip().startswith("1. ")
                    )
                    table_entries = [
                        text.strip()
                        for text in texts[table_start + 1 : first_body_heading]
                        if text.strip()
                    ]
                    self.assertEqual(len(table_entries), len(tables))

                    for section in document.findall(".//w:sectPr", NAMESPACES):
                        margins = section.find("w:pgMar", NAMESPACES)
                        self.assertIsNotNone(margins)
                        expected = {
                            "top": "1440",
                            "bottom": "1440",
                            "left": "1080",
                            "right": "1080",
                        }
                        for margin, value in expected.items():
                            self.assertEqual(margins.get(word_attribute(margin)), value)

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

    def test_reference_doc_preserves_print_styles(self) -> None:
        """参照DOCXが共通の印刷Styleと余白を保持する。"""
        with ZipFile(REFERENCE_DOC) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))
            styles = ET.fromstring(archive.read("word/styles.xml"))
            settings = ET.fromstring(archive.read("word/settings.xml"))
        update_fields = settings.find("w:updateFields", NAMESPACES)
        self.assertIsNotNone(update_fields)
        self.assertIn(update_fields.get(word_attribute("val")), {"1", "true"})
        for style_id in ("Normal", "BodyText", "Table"):
            size = style_by_id(styles, style_id).find("w:rPr/w:sz", NAMESPACES)
            self.assertIsNotNone(size)
            self.assertEqual(size.get(word_attribute("val")), "20")
        for style_id in ("Heading1", "TOCHeading"):
            page_break = style_by_id(styles, style_id).find(
                "w:pPr/w:pageBreakBefore", NAMESPACES
            )
            self.assertIsNotNone(page_break)
        for style_id in ("TOC1", "TOC2", "TOC3", "TOC4", "TOC5", "TOC6"):
            spacing = style_by_id(styles, style_id).find("w:pPr/w:spacing", NAMESPACES)
            self.assertIsNotNone(spacing)
            self.assertEqual(spacing.get(word_attribute("after")), "0")
        table_alignment = style_by_id(styles, "Table").find("w:tblPr/w:jc", NAMESPACES)
        self.assertIsNotNone(table_alignment)
        self.assertEqual(table_alignment.get(word_attribute("val")), "center")
        for section in document.findall(".//w:sectPr", NAMESPACES):
            margins = section.find("w:pgMar", NAMESPACES)
            self.assertIsNotNone(margins)
            self.assertEqual(margins.get(word_attribute("top")), "1440")
            self.assertEqual(margins.get(word_attribute("bottom")), "1440")
            self.assertEqual(margins.get(word_attribute("left")), "1080")
            self.assertEqual(margins.get(word_attribute("right")), "1080")

    def test_release_workflow_publishes_prd_and_hld(self) -> None:
        """Release WorkflowがPRDとHLDを同時に登録する。"""
        workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("openspec/publics/prd.docx", workflow)
        self.assertIn("openspec/publics/hld.docx", workflow)
        release_line = next(
            line for line in workflow.splitlines() if "gh release create" in line
        )
        self.assertIn("prd.docx", release_line)
        self.assertIn("hld.docx", release_line)


def main() -> int:
    """Test Suiteを実行して成否を返す。"""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MarkdownToDocxTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
