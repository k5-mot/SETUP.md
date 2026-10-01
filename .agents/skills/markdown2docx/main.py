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
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
NAMESPACES = {"w": WORD_NAMESPACE}
NAVIGATION_TITLES = ("目次", "図一覧", "表一覧")
MARGINS = {"top": "1440", "bottom": "1440", "left": "1080", "right": "1080"}


def word_name(name: str) -> str:
    """WordprocessingMLの完全修飾名を返す。"""
    return f"{{{WORD_NAMESPACE}}}{name}"


def paragraph_style(paragraph: ET.Element) -> str:
    """段落のStyle IDを返す。"""
    style = paragraph.find("w:pPr/w:pStyle", NAMESPACES)
    return "" if style is None else style.get(word_name("val"), "")


def paragraph_text(paragraph: ET.Element) -> str:
    """段落内の表示Textを結合する。"""
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NAMESPACES))


def replace_paragraph_text(paragraph: ET.Element, value: str) -> None:
    """段落のStyleを保って表示Textを置換する。"""
    properties = paragraph.find("w:pPr", NAMESPACES)
    for child in list(paragraph):
        if child is not properties:
            paragraph.remove(child)
    run = ET.SubElement(paragraph, word_name("r"))
    text = ET.SubElement(run, word_name("t"))
    text.text = value


def field_run(field_code: str, value: str) -> list[ET.Element]:
    """更新可能なSimple FieldのRun列を作る。"""
    begin_run = ET.Element(word_name("r"))
    begin = ET.SubElement(begin_run, word_name("fldChar"))
    begin.set(word_name("fldCharType"), "begin")

    instruction_run = ET.Element(word_name("r"))
    instruction = ET.SubElement(instruction_run, word_name("instrText"))
    instruction.set(f"{{{XML_NAMESPACE}}}space", "preserve")
    instruction.text = f" {field_code} "

    separate_run = ET.Element(word_name("r"))
    separate = ET.SubElement(separate_run, word_name("fldChar"))
    separate.set(word_name("fldCharType"), "separate")

    value_run = ET.Element(word_name("r"))
    text = ET.SubElement(value_run, word_name("t"))
    text.text = value

    end_run = ET.Element(word_name("r"))
    end = ET.SubElement(end_run, word_name("fldChar"))
    end.set(word_name("fldCharType"), "end")
    return [begin_run, instruction_run, separate_run, value_run, end_run]


def caption_paragraph(number: int, title: str) -> ET.Element:
    """表番号Fieldを含む日本語Caption段落を作る。"""
    paragraph = ET.Element(word_name("p"))
    properties = ET.SubElement(paragraph, word_name("pPr"))
    style = ET.SubElement(properties, word_name("pStyle"))
    style.set(word_name("val"), "TableCaption")

    prefix_run = ET.SubElement(paragraph, word_name("r"))
    prefix = ET.SubElement(prefix_run, word_name("t"))
    prefix.text = "表 "
    for run in field_run(r"SEQ Table \* ARABIC", str(number)):
        paragraph.append(run)
    suffix_run = ET.SubElement(paragraph, word_name("r"))
    suffix = ET.SubElement(suffix_run, word_name("t"))
    suffix.text = f": {title}"
    return paragraph


def add_table_captions(body: ET.Element) -> None:
    """本文の全表へ直前見出しを用いたCaptionを追加する。"""
    heading = "表"
    heading_counts: defaultdict[str, int] = defaultdict(int)
    table_number = 0
    index = 0
    while index < len(body):
        child = body[index]
        if child.tag == word_name("p"):
            style = paragraph_style(child)
            if style.startswith("Heading") and paragraph_text(child).strip():
                heading = paragraph_text(child).strip()
        elif child.tag == word_name("tbl"):
            previous = body[index - 1] if index else None
            if (
                previous is not None
                and previous.tag == word_name("p")
                and paragraph_style(previous) == "TableCaption"
            ):
                index += 1
                continue
            table_number += 1
            heading_counts[heading] += 1
            occurrence = heading_counts[heading]
            title = heading if occurrence == 1 else f"{heading}（{occurrence}）"
            body.insert(index, caption_paragraph(table_number, title))
            index += 1
        index += 1


def update_navigation(document: ET.Element) -> None:
    """Navigation見出しと一覧Fieldが参照するStyle名を日本語化する。"""
    headings = [
        paragraph
        for paragraph in document.findall(".//w:p", NAMESPACES)
        if paragraph_style(paragraph) == "TOCHeading"
    ]
    if len(headings) < len(NAVIGATION_TITLES):
        msg = "DOCXに目次・図一覧・表一覧の見出しがありません"
        raise ValueError(msg)
    for paragraph, title in zip(headings[:3], NAVIGATION_TITLES, strict=True):
        replace_paragraph_text(paragraph, title)

    for instruction in document.findall(".//w:instrText", NAMESPACES):
        if instruction.text:
            instruction.text = instruction.text.replace("Image Caption", "図タイトル")
            instruction.text = instruction.text.replace("Table Caption", "表タイトル")


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


def finalize_docx(path: Path) -> None:
    """DOCXのNavigation、Caption、余白を更新する。"""
    with tempfile.TemporaryDirectory(prefix="mysdd_docx_") as directory:
        root = Path(directory)
        with ZipFile(path) as archive:
            archive.extractall(root)
        document_path = root / "word" / "document.xml"
        document = ET.parse(document_path)
        body = document.getroot().find("w:body", NAMESPACES)
        if body is None:
            raise ValueError("DOCXに本文がありません")
        update_navigation(document.getroot())
        add_table_captions(body)
        update_margins(document.getroot())
        ET.register_namespace("w", WORD_NAMESPACE)
        document.write(document_path, encoding="utf-8", xml_declaration=True)
        temporary = path.with_suffix(".tmp.docx")
        with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
            for item in root.rglob("*"):
                if item.is_file():
                    archive.write(item, item.relative_to(root).as_posix())
        temporary.replace(path)


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
            document = desktop.loadComponentFromURL(
                uno.systemPathToFileUrl(str(path.resolve())), "_blank", 0, (hidden,)
            )
            indexes = document.getDocumentIndexes()
            for index in range(indexes.getCount()):
                indexes.getByIndex(index).update()
            document.getTextFields().refresh()
            document.store()
            document.close(True)
        finally:
            process.terminate()
            process.wait(timeout=10)


def refresh_fields(path: Path) -> None:
    """実行環境のField対応Office EngineでDOCXを更新する。"""
    if sys.platform == "win32":
        refresh_with_word(path)
    else:
        refresh_with_libreoffice(path)


def main() -> int:
    """指定DOCXを仕上げる。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("finalize", "refresh"))
    parser.add_argument("documents", nargs="+", type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    for document in args.documents:
        if not document.is_file() or document.suffix.lower() != ".docx":
            parser.error(f"DOCXが存在しません: {document}")
        if args.operation == "finalize":
            finalize_docx(document)
        else:
            refresh_fields(document)
    print(
        f"{args.operation} documents={len(args.documents)} elapsed_seconds={time.perf_counter() - start:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
