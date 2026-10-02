#!/usr/bin/env python3
"""Pandocで生成したMySDD DOCXを配布可能な状態へ仕上げる。"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
MARKUP_COMPATIBILITY_NAMESPACE = (
    "http://schemas.openxmlformats.org/markup-compatibility/2006"
)
OFFICE_RELATIONSHIP_NAMESPACE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
)
PACKAGE_RELATIONSHIP_NAMESPACE = (
    "http://schemas.openxmlformats.org/package/2006/relationships"
)
NAMESPACES = {"w": WORD_NAMESPACE}
MARGINS = {"top": "1440", "bottom": "1440", "left": "1080", "right": "1080"}


def word_name(name: str) -> str:
    """WordprocessingMLの完全修飾名を返す。"""
    return f"{{{WORD_NAMESPACE}}}{name}"


def paragraph_style(paragraph: ET.Element) -> str:
    """段落のStyle IDを返す。"""
    style = paragraph.find("w:pPr/w:pStyle", NAMESPACES)
    return "" if style is None else style.get(word_name("val"), "")


def element_text(element: ET.Element) -> str:
    """Content Controlを含む要素内の表示Textを結合する。"""
    return "".join(node.text or "" for node in element.findall(".//w:t", NAMESPACES))


def navigation_entry_paragraph(text: str, page: int | None = None) -> ET.Element:
    """一覧の表示項目をTOC Styleで作る。"""
    paragraph = ET.Element(word_name("p"))
    properties = ET.SubElement(paragraph, word_name("pPr"))
    style = ET.SubElement(properties, word_name("pStyle"))
    style.set(word_name("val"), "TOC1")
    text_run = ET.SubElement(paragraph, word_name("r"))
    value = ET.SubElement(text_run, word_name("t"))
    value.text = text
    if page is not None:
        tab_run = ET.SubElement(paragraph, word_name("r"))
        ET.SubElement(tab_run, word_name("tab"))
        page_run = ET.SubElement(paragraph, word_name("r"))
        page_text = ET.SubElement(page_run, word_name("t"))
        page_text.text = str(page)
    return paragraph


def normalize_libreoffice_tables(document: ET.Element) -> None:
    """LibreOffice保存後も表の中央配置を維持する。"""
    for table in document.findall(".//w:tbl", NAMESPACES):
        properties = table.find("w:tblPr", NAMESPACES)
        if properties is None:
            properties = ET.Element(word_name("tblPr"))
            table.insert(0, properties)
        alignment = properties.find("w:jc", NAMESPACES)
        if alignment is None:
            alignment = ET.SubElement(properties, word_name("jc"))
        alignment.set(word_name("val"), "center")
        indent = properties.find("w:tblInd", NAMESPACES)
        if indent is not None:
            properties.remove(indent)


def update_margins(document: ET.Element) -> None:
    """全Sectionへ指定された「やや狭い」余白を設定する。"""
    sections = document.findall(".//w:sectPr", NAMESPACES)
    if not sections:
        raise ValueError("DOCXにSection設定がありません")
    for section in sections:
        margins = section.find("w:pgMar", NAMESPACES)
        if margins is None:
            margins = ET.SubElement(section, word_name("pgMar"))
        for name, value in MARGINS.items():
            margins.set(word_name(name), value)


def synchronize_even_headers_and_footers(root: Path, document: ET.Element) -> None:
    """LibreOfficeが作る空の偶数ページ用HeaderとFooterをDefault内容で置換する。"""
    relationships_path = root / "word" / "_rels" / "document.xml.rels"
    relationships = ET.parse(relationships_path).getroot()
    targets = {
        relationship.get("Id", ""): relationship.get("Target", "")
        for relationship in relationships.findall(
            f"{{{PACKAGE_RELATIONSHIP_NAMESPACE}}}Relationship"
        )
    }
    for section in document.findall(".//w:sectPr", NAMESPACES):
        for reference_name in ("headerReference", "footerReference"):
            references = section.findall(f"w:{reference_name}", NAMESPACES)
            by_type = {
                reference.get(word_name("type"), ""): reference
                for reference in references
            }
            if "even" not in by_type or "default" not in by_type:
                continue
            default_id = by_type["default"].get(
                f"{{{OFFICE_RELATIONSHIP_NAMESPACE}}}id", ""
            )
            even_id = by_type["even"].get(f"{{{OFFICE_RELATIONSHIP_NAMESPACE}}}id", "")
            default_target = root / "word" / targets[default_id]
            even_target = root / "word" / targets[even_id]
            even_target.write_bytes(default_target.read_bytes())


def remove_navigation_page_breaks(document: ET.Element) -> None:
    """TOCHeading Styleと重複する明示的Page Breakを除去する。"""
    for paragraph in document.findall(".//w:p", NAMESPACES):
        if paragraph_style(paragraph) != "TOCHeading":
            continue
        for run in paragraph.findall("w:r", NAMESPACES):
            for page_break in run.findall("w:br", NAMESPACES):
                if page_break.get(word_name("type")) == "page":
                    run.remove(page_break)
            if not list(run) and not (run.text or "").strip():
                paragraph.remove(run)


def refresh_with_word(path: Path) -> None:
    """Microsoft Wordで全Fieldを更新して保存する。"""
    environment = os.environ.copy()
    environment["MYSDD_DOCX_PATH"] = str(path.resolve())
    script = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  $document = $word.Documents.Open($env:MYSDD_DOCX_PATH)
  $document.Fields.Update() | Out-Null
  foreach ($toc in @($document.TablesOfContents)) { $toc.Update() }
  foreach ($list in @($document.TablesOfFigures)) { $list.Update() }
  $document.Save()
  $document.Close()
} finally {
  $word.Quit()
}
"""
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        check=True,
        env=environment,
    )


def unused_port() -> int:
    """LibreOffice接続用の空きPortを返す。"""
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def refresh_with_libreoffice(path: Path) -> None:
    """Headless LibreOfficeで全IndexとFieldを更新して保存する。"""
    try:
        import uno  # type: ignore[import-not-found]
        from com.sun.star.beans import PropertyValue  # type: ignore[import-not-found]
    except ImportError as error:
        msg = "LibreOffice Python UNOが必要です"
        raise RuntimeError(msg) from error

    port = unused_port()
    with tempfile.TemporaryDirectory(prefix="mysdd_lo_") as profile:
        accept = f"socket,host=127.0.0.1,port={port};urp;StarOffice.ServiceManager"
        process = subprocess.Popen(
            [
                "soffice",
                "--headless",
                f"--accept={accept}",
                "--norestore",
                "--nodefault",
                "--nofirststartwizard",
                f"-env:UserInstallation={Path(profile).as_uri()}",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            local_context = uno.getComponentContext()
            resolver = local_context.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", local_context
            )
            context = None
            for _ in range(40):
                try:
                    context = resolver.resolve(
                        f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext"
                    )
                    break
                except Exception:  # noqa: BLE001
                    time.sleep(0.25)
            if context is None:
                raise RuntimeError("LibreOfficeへ接続できません")
            desktop = context.ServiceManager.createInstanceWithContext(
                "com.sun.star.frame.Desktop", context
            )
            hidden = PropertyValue()
            hidden.Name = "Hidden"
            hidden.Value = True
            for _ in range(2):
                document = desktop.loadComponentFromURL(
                    uno.systemPathToFileUrl(str(path.resolve())),
                    "_blank",
                    0,
                    (hidden,),
                )
                indexes = document.getDocumentIndexes()
                for index in range(indexes.getCount()):
                    indexes.getByIndex(index).update()
                document.getTextFields().refresh()
                navigation_entries = collect_navigation_entries(document)
                document.store()
                document.close(True)
                replace_navigation_entries(path, navigation_entries)
        finally:
            process.terminate()
            process.wait(timeout=10)


def collect_navigation_entries(
    document: object,
) -> dict[str, list[tuple[str, int]]]:
    """LibreOfficeの配置結果から図表CaptionとPage番号を集める。"""
    entries: dict[str, list[tuple[str, int]]] = {"図一覧": [], "表一覧": []}
    style_to_list = {
        "ImageCaption": "図一覧",
        "Image Caption": "図一覧",
        "図タイトル": "図一覧",
        "TableCaption": "表一覧",
        "Table Caption": "表一覧",
        "表タイトル": "表一覧",
    }
    view_cursor = document.getCurrentController().getViewCursor()
    elements = document.Text.createEnumeration()
    while elements.hasMoreElements():
        element = elements.nextElement()
        if not element.supportsService("com.sun.star.text.Paragraph"):
            continue
        list_name = style_to_list.get(element.ParaStyleName)
        if list_name is None:
            continue
        view_cursor.gotoRange(element, False)
        entries[list_name].append((element.getString(), int(view_cursor.Page)))
    return entries


def replace_navigation_entries(
    path: Path, entries: dict[str, list[tuple[str, int]]]
) -> None:
    """LibreOfficeが削除する図表一覧を表示結果としてDOCXへ書き戻す。"""
    with tempfile.TemporaryDirectory(prefix="mysdd_lists_") as directory:
        root = Path(directory)
        with ZipFile(path) as archive:
            archive.extractall(root)
        document_path = root / "word" / "document.xml"
        document = ET.parse(document_path)
        body = document.getroot().find("w:body", NAMESPACES)
        if body is None:
            raise ValueError("DOCXに本文がありません")

        for title, end_title in (("図一覧", "表一覧"), ("表一覧", None)):
            children = list(body)
            start = next(
                index
                for index, child in enumerate(children)
                if element_text(child) == title
            )
            if end_title is None:
                end = next(
                    index
                    for index, child in enumerate(children[start + 1 :], start + 1)
                    if child.tag == word_name("p")
                    and paragraph_style(child).startswith("Heading1")
                )
            else:
                end = next(
                    index
                    for index, child in enumerate(children[start + 1 :], start + 1)
                    if element_text(child) == end_title
                )
            for child in children[start + 1 : end]:
                body.remove(child)
            values = entries[title]
            if not values and title == "図一覧":
                body.insert(
                    start + 1, navigation_entry_paragraph("該当する図はありません。")
                )
            else:
                for offset, (text, page) in enumerate(values, 1):
                    body.insert(start + offset, navigation_entry_paragraph(text, page))

        # LibreOfficeが残すIgnorable値は、未使用Namespace宣言をXML再保存時に
        # 失ってWordで破損扱いになるため、拡張要素がない確定結果から除去する。
        remove_navigation_page_breaks(document.getroot())
        normalize_libreoffice_tables(document.getroot())
        update_margins(document.getroot())
        synchronize_even_headers_and_footers(root, document.getroot())
        document.getroot().attrib.pop(
            f"{{{MARKUP_COMPATIBILITY_NAMESPACE}}}Ignorable", None
        )
        ET.register_namespace("w", WORD_NAMESPACE)
        document.write(document_path, encoding="utf-8", xml_declaration=True)
        temporary = path.with_suffix(".tmp.docx")
        with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
            for item in root.rglob("*"):
                if item.is_file():
                    archive.write(item, item.relative_to(root).as_posix())
        temporary.replace(path)


def refresh_fields(path: Path) -> None:
    """実行環境のField対応Office EngineでDOCXを更新する。"""
    if sys.platform == "win32":
        refresh_with_word(path)
    else:
        refresh_with_libreoffice(path)


def main() -> int:
    """指定DOCXを仕上げる。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("refresh",))
    parser.add_argument("documents", nargs="+", type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    for document in args.documents:
        if not document.is_file() or document.suffix.lower() != ".docx":
            parser.error(f"DOCXが存在しません: {document}")
        refresh_fields(document)
    print(
        f"{args.operation} documents={len(args.documents)} elapsed_seconds={time.perf_counter() - start:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
