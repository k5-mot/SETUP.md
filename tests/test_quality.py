#!/usr/bin/env python3
"""CI品質Scriptの公開CLIを回帰Testする。"""

from __future__ import annotations

import logging
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

LOGGER = logging.getLogger(__name__)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LINK_CHECKER = REPOSITORY_ROOT / "scripts" / "check_markdown_links.py"


class QualityScriptTests(unittest.TestCase):
    """品質Scriptを利用者と同じCommand経由で検証する。"""

    def test_link_checker_reports_only_missing_local_targets(self) -> None:
        """欠落Linkを失敗にし、Target作成後は成功する。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            source.write_text(
                "[missing](target.md) and [external](https://example.com)\n",
                encoding="utf-8",
            )
            command = [
                sys.executable,
                str(LINK_CHECKER),
                "--root",
                str(root),
                "source.md",
            ]

            missing = subprocess.run(
                command, check=False, capture_output=True, text=True
            )
            self.assertEqual(1, missing.returncode)
            self.assertIn("target.md", missing.stderr)

            (root / "target.md").write_text("# Target\n", encoding="utf-8")
            resolved = subprocess.run(
                command, check=False, capture_output=True, text=True
            )
            self.assertEqual(0, resolved.returncode, resolved.stderr)


def main() -> int:
    """Test Suiteを実行し、経過時間と成否を返す。"""
    started = time.perf_counter()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(QualityScriptTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    LOGGER.info("quality test elapsed_seconds=%.3f", time.perf_counter() - started)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
