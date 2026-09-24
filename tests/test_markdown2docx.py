#!/usr/bin/env python3
"""MarkdownからDOCXへの公開変換手順を回帰Testする。"""

from __future__ import annotations

import hashlib
import logging
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

LOGGER = logging.getLogger(__name__)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PUBLICS = REPOSITORY_ROOT / "openspec" / "publics"
FORMATTER = (
    REPOSITORY_ROOT
    / ".agents"
    / "skills"
    / "markdown2docx"
    / "scripts"
    / "format_docx.py"
)
DOCUMENTS = {"prd": "QR-001", "hld": "ADR-001"}


class MarkdownToDocxTests(unittest.TestCase):
    """PRDとHLDの配布用DOCX生成を検証する。"""

    def test_representative_documents_are_generated(self) -> None:
        """代表文書ごとに非空DOCXが生成される。"""
        with tempfile.TemporaryDirectory() as directory:
            output_root = Path(directory)
            for name, representative_id in DOCUMENTS.items():
                with self.subTest(document=name):
                    started = time.perf_counter()
                    source = PUBLICS / f"{name}.md"
                    output = output_root / f"{name}.docx"
                    before = hashlib.sha256(source.read_bytes()).digest()

                    subprocess.run(
                        [
                            "pandoc",
                            str(source),
                            "--from=gfm",
                            "--to=docx",
                            f"--reference-doc={PUBLICS / 'template.docx'}",
                            f"--output={output}",
                        ],
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    subprocess.run(
                        [
                            "python",
                            str(FORMATTER),
                            "generated",
                            str(output),
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
                    self.assertIn(representative_id, "".join(document.itertext()))
                    LOGGER.info(
                        "docx document=%s elapsed_seconds=%.3f",
                        name,
                        time.perf_counter() - started,
                    )


def main() -> int:
    """Test Suiteを実行し、経過時間と成否を返す。"""
    started = time.perf_counter()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MarkdownToDocxTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    LOGGER.info("docx test elapsed_seconds=%.3f", time.perf_counter() - started)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
