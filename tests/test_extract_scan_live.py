from __future__ import annotations

import ast
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.extract_scan_live import extract_python


class ExtractScanLiveTests(unittest.TestCase):
    def test_checked_in_skill_extracts_valid_python(self):
        code = extract_python(ROOT / "meme_scanner.md")

        self.assertGreater(len(code.splitlines()), 500)
        self.assertIn("ENABLE_LIVE_TRADING", code)
        ast.parse(code)

    def test_missing_python_block_fails_with_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "empty.md"
            skill.write_text("# No code here\n", encoding="utf-8")

            with self.assertRaisesRegex(SystemExit, "No python blocks"):
                extract_python(skill)


if __name__ == "__main__":
    unittest.main()
