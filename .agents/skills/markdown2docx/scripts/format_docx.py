#!/usr/bin/env python3
"""MySDD DOCXの共通レイアウトをOOXMLへ適用する。"""

from __future__ import annotations

import argparse
import logging
import os
import tempfile
import time
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

LOGGER = logging.getLogger(__name__)
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
W = f"{{{W_NS}}}"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
NAMESPACES = {
    "w": W_NS,
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": MC_NS,
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "o": "urn:schemas-microsoft-com:office:office",
    "v": "urn:schemas-microsoft-com:vml",
    "w10": "urn:schemas-microsoft-com:office:word",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16": "http://schemas.microsoft.com/office/word/2018/wordml",
    "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16du": "http://schemas.microsoft.com/office/word/2023/wordml/word16du",
    "w16sdtdh": "http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash",
    "w16sdtfl": "http://schemas.microsoft.com/office/word/2024/wordml/sdtformatlock",
    "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
}
CALLOUT_PALETTE = {
    "note": ("EAF2F8", "4472C4"),
    "tip": ("E2F0D9", "548235"),
    "important": ("E4DFEC", "7030A0"),
    "warning": ("FCE4D6", "C00000"),
    "caution": ("FFF2CC", "BF9000"),
}
for prefix, namespace in NAMESPACES.items():
    ET.register_namespace(prefix, namespace)


def _child(parent: ET.Element, name: str) -> ET.Element:
    element = parent.find(W + name)
    if element is None:
        element = ET.SubElement(parent, W + name)
    return element


def _properties(element: ET.Element, name: str) -> ET.Element:
    properties = element.find(W + name)
    if properties is None:
        properties = ET.Element(W + name)
        element.insert(0, properties)
    return properties


def _style_ids(styles: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for style in styles.findall(W + "style"):
        name = style.find(W + "name")
        if name is not None:
            result[name.get(W + "val", "").casefold()] = style.get(W + "styleId", "")
    return result


def _paragraph_style(paragraph: ET.Element) -> str | None:
    properties = paragraph.find(W + "pPr")
    style = properties.find(W + "pStyle") if properties is not None else None
    return style.get(W + "val") if style is not None else None


def _set_paragraph_style(paragraph: ET.Element, style_id: str) -> ET.Element:
    properties = _properties(paragraph, "pPr")
    _child(properties, "pStyle").set(W + "val", style_id)
    return properties


def _disable_heading_numbering(properties: ET.Element) -> None:
    numbering = _child(properties, "numPr")
    _child(numbering, "numId").set(W + "val", "0")


def _normalize_styles(styles: ET.Element) -> None:
    for tag in ("sz", "szCs"):
        for element in styles.iter(W + tag):
            if element.get(W + "val") == "21":
                element.set(W + "val", "20")


def _color_callouts(styles: ET.Element) -> None:
    for style in styles.findall(W + "style"):
        if style.get(W + "type") != "paragraph":
            continue
        name = style.find(W + "name")
        style_name = name.get(W + "val", "").casefold() if name is not None else ""
        role = next(
            (
                key
                for key in CALLOUT_PALETTE
                if style_name == key or style_name.startswith(f"{key} ")
            ),
            None,
        )
        if role is None:
            continue
        fill, border_color = CALLOUT_PALETTE[role]
        properties = _properties(style, "pPr")
        shading = _child(properties, "shd")
        shading.set(W + "val", "clear")
        shading.set(W + "color", "auto")
        shading.set(W + "fill", fill)
        borders = _child(properties, "pBdr")
        left = _child(borders, "left")
        left.set(W + "val", "single")
        left.set(W + "sz", "18")
        left.set(W + "space", "6")
        left.set(W + "color", border_color)


def _normalize_tables(document: ET.Element) -> None:
    for table in document.iter(W + "tbl"):
        properties = _properties(table, "tblPr")
        _child(properties, "jc").set(W + "val", "center")
    for row in document.iter(W + "tr"):
        properties = _properties(row, "trPr")
        for header in list(properties.findall(W + "tblHeader")):
            properties.remove(header)
        _child(properties, "cantSplit")


def _enable_field_updates(settings: ET.Element) -> None:
    _child(settings, "updateFields").set(W + "val", "true")


def _page_break_run() -> ET.Element:
    run = ET.Element(W + "r")
    ET.SubElement(run, W + "br", {W + "type": "page"})
    return run


def _toc_paragraph(style_id: str) -> ET.Element:
    paragraph = ET.Element(W + "p")
    _set_paragraph_style(paragraph, style_id)

    begin = ET.SubElement(paragraph, W + "r")
    ET.SubElement(
        begin, W + "fldChar", {W + "fldCharType": "begin", W + "dirty": "true"}
    )
    instruction_run = ET.SubElement(paragraph, W + "r")
    instruction = ET.SubElement(instruction_run, W + "instrText")
    instruction.set(f"{{{XML_NS}}}space", "preserve")
    instruction.text = ' TOC \\o "1-3" \\h \\z \\u '
    separator = ET.SubElement(paragraph, W + "r")
    ET.SubElement(separator, W + "fldChar", {W + "fldCharType": "separate"})
    placeholder = ET.SubElement(paragraph, W + "r")
    ET.SubElement(placeholder, W + "t").text = "目次を更新してください。"
    end = ET.SubElement(paragraph, W + "r")
    ET.SubElement(end, W + "fldChar", {W + "fldCharType": "end"})
    return paragraph


def _toc_heading(style_id: str) -> ET.Element:
    paragraph = ET.Element(W + "p")
    _set_paragraph_style(paragraph, style_id)
    run = ET.SubElement(paragraph, W + "r")
    ET.SubElement(run, W + "t").text = "目次"
    return paragraph


def _format_generated(document: ET.Element, styles: ET.Element) -> None:
    style_ids = _style_ids(styles)
    required = ["title", "toc heading", "heading 1", "heading 2"]
    missing = [name for name in required if not style_ids.get(name)]
    if missing:
        raise ValueError(f"必要なWordスタイルがありません: {', '.join(missing)}")

    body = document.find(W + "body")
    if body is None:
        raise ValueError("DOCX本文がありません。")

    paragraphs = [element for element in list(body) if element.tag == W + "p"]
    heading_one = style_ids["heading 1"]
    title = next((p for p in paragraphs if _paragraph_style(p) == heading_one), None)
    if title is None:
        raise ValueError("表紙へ変換する見出しレベル1がありません。")

    title_properties = _set_paragraph_style(title, style_ids["title"])
    numbering = title_properties.find(W + "numPr")
    if numbering is not None:
        title_properties.remove(numbering)
    page_break_before = title_properties.find(W + "pageBreakBefore")
    if page_break_before is not None:
        title_properties.remove(page_break_before)
    _child(title_properties, "jc").set(W + "val", "center")
    spacing = _child(title_properties, "spacing")
    spacing.set(W + "before", "4200")
    spacing.set(W + "after", "0")
    title.append(_page_break_run())

    heading_map: dict[str, str] = {}
    for source_level in range(2, 7):
        source = style_ids.get(f"heading {source_level}")
        target = style_ids.get(f"heading {source_level - 1}")
        if source and target:
            heading_map[source] = target

    promoted_headings = 0
    for paragraph in paragraphs:
        if paragraph is title:
            continue
        target_style = heading_map.get(_paragraph_style(paragraph) or "")
        if target_style is None:
            continue
        properties = _set_paragraph_style(paragraph, target_style)
        _disable_heading_numbering(properties)
        if target_style == heading_one:
            _child(properties, "pageBreakBefore")
            promoted_headings += 1

    if promoted_headings == 0:
        raise ValueError("本文の見出しレベル1へ昇格できる章見出しがありません。")

    title_index = list(body).index(title)
    body.insert(title_index + 1, _toc_heading(style_ids["toc heading"]))
    body.insert(
        title_index + 2, _toc_paragraph(style_ids.get("toc 1", style_ids["heading 2"]))
    )


def _serialize_xml(root: ET.Element) -> bytes:
    used_namespaces: set[str] = set()
    for element in root.iter():
        for qualified_name in (element.tag, *element.attrib):
            if qualified_name.startswith("{"):
                used_namespaces.add(qualified_name[1:].split("}", 1)[0])
    prefixes = {
        prefix
        for prefix, namespace in NAMESPACES.items()
        if namespace in used_namespaces
    }
    ignorable = root.get(f"{{{MC_NS}}}Ignorable")
    if ignorable:
        root.set(
            f"{{{MC_NS}}}Ignorable",
            " ".join(token for token in ignorable.split() if token in prefixes),
        )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def format_docx(path: Path, mode: str) -> None:
    if not path.is_file() or path.suffix.casefold() != ".docx":
        raise ValueError(f"DOCXが見つかりません: {path}")

    with ZipFile(path) as source:
        entries = {
            info.filename: (info, source.read(info.filename))
            for info in source.infolist()
        }

    required = ("word/document.xml", "word/styles.xml", "word/settings.xml")
    missing = [name for name in required if name not in entries]
    if missing:
        raise ValueError(f"必要なOOXML部品がありません: {', '.join(missing)}")

    document = ET.fromstring(entries["word/document.xml"][1])
    styles = ET.fromstring(entries["word/styles.xml"][1])
    settings = ET.fromstring(entries["word/settings.xml"][1])

    _normalize_styles(styles)
    _color_callouts(styles)
    _normalize_tables(document)
    _enable_field_updates(settings)
    if mode == "generated":
        _format_generated(document, styles)

    entries["word/document.xml"] = (
        entries["word/document.xml"][0],
        _serialize_xml(document),
    )
    entries["word/styles.xml"] = (entries["word/styles.xml"][0], _serialize_xml(styles))
    entries["word/settings.xml"] = (
        entries["word/settings.xml"][0],
        _serialize_xml(settings),
    )

    descriptor, temporary_name = tempfile.mkstemp(suffix=".docx", dir=path.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with ZipFile(temporary, "w", ZIP_DEFLATED) as target:
            for info, data in entries.values():
                target.writestr(info, data)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def check_docx(path: Path, mode: str) -> None:
    with ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        styles = ET.fromstring(archive.read("word/styles.xml"))

    if any(
        element.get(W + "val") == "21"
        for tag in ("sz", "szCs")
        for element in styles.iter(W + tag)
    ):
        raise ValueError("10.5ptのスタイルが残っています。")
    if any(True for _ in document.iter(W + "tblHeader")):
        raise ValueError("表のヘッダー行を繰り返す指定が残っています。")
    for table in document.iter(W + "tbl"):
        properties = table.find(W + "tblPr")
        alignment = properties.find(W + "jc") if properties is not None else None
        if alignment is None or alignment.get(W + "val") != "center":
            raise ValueError("ページ中央に配置されていない表があります。")
    styles_by_name = _style_ids(styles)
    for role, (fill, border_color) in CALLOUT_PALETTE.items():
        style_id = next(
            (
                style_id
                for name, style_id in styles_by_name.items()
                if name == role or name.startswith(f"{role} ")
            ),
            None,
        )
        if style_id is None:
            continue
        style = next(
            element
            for element in styles.findall(W + "style")
            if element.get(W + "styleId") == style_id
        )
        shading = style.find(f"{W}pPr/{W}shd")
        left = style.find(f"{W}pPr/{W}pBdr/{W}left")
        if shading is None or shading.get(W + "fill") != fill:
            raise ValueError(f"{role}注意ブロックの背景色が一致しません。")
        if left is None or left.get(W + "color") != border_color:
            raise ValueError(f"{role}注意ブロックの罫線色が一致しません。")
    if mode == "generated":
        style_ids = _style_ids(styles)
        body = document.find(W + "body")
        if body is None:
            raise ValueError("DOCX本文がありません。")
        paragraphs = [element for element in list(body) if element.tag == W + "p"]
        if not paragraphs or _paragraph_style(paragraphs[0]) != style_ids.get("title"):
            raise ValueError("先頭の文書名が表紙Titleになっていません。")
        if not any(
            "TOC" in (element.text or "") for element in document.iter(W + "instrText")
        ):
            raise ValueError("目次フィールドがありません。")
        heading_one = style_ids.get("heading 1")
        chapter_headings = [p for p in paragraphs if _paragraph_style(p) == heading_one]
        if not chapter_headings:
            raise ValueError("本文の見出しレベル1がありません。")
        heading_style = next(
            (
                style
                for style in styles.findall(W + "style")
                if style.get(W + "styleId") == heading_one
            ),
            None,
        )
        style_properties = (
            heading_style.find(W + "pPr") if heading_style is not None else None
        )
        style_has_page_break = (
            style_properties is not None
            and style_properties.find(W + "pageBreakBefore") is not None
        )
        for paragraph in chapter_headings:
            properties = paragraph.find(W + "pPr")
            direct_page_break = (
                properties is not None
                and properties.find(W + "pageBreakBefore") is not None
            )
            if not style_has_page_break and not direct_page_break:
                raise ValueError("改ページ指定のない見出しレベル1があります。")


def main() -> None:
    started = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generated", "reference"))
    parser.add_argument("docx", type=Path)
    parser.add_argument("--check", action="store_true", help="変更せずに設定を検証する")
    arguments = parser.parse_args()

    path = arguments.docx.resolve()
    if arguments.check:
        check_docx(path, arguments.mode)
    else:
        format_docx(path, arguments.mode)
        check_docx(path, arguments.mode)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    LOGGER.info(
        "docx mode=%s check=%s elapsed_seconds=%.3f",
        arguments.mode,
        arguments.check,
        time.perf_counter() - started,
    )


if __name__ == "__main__":
    main()
