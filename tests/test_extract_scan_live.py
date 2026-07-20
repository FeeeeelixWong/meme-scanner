from __future__ import annotations

import ast
import importlib.util
import os
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

    def test_default_replay_requires_no_credentials_and_explains_decisions(self):
        code = extract_python(ROOT / "meme_scanner.md")
        tracked_env = {
            name: os.environ.get(name)
            for name in (
                "MEME_SCANNER_MODE",
                "ENABLE_LIVE_TRADING",
                "OKX_API_KEY",
                "OKX_SECRET_KEY",
                "OKX_PASSPHRASE",
                "WALLET_PRIVATE_KEY",
            )
        }

        with tempfile.TemporaryDirectory() as tmp:
            generated = Path(tmp) / "scan_live.py"
            generated.write_text(code, encoding="utf-8")
            for name in tracked_env:
                os.environ.pop(name, None)

            try:
                spec = importlib.util.spec_from_file_location("replay_scan", generated)
                module = importlib.util.module_from_spec(spec)
                assert spec.loader is not None
                spec.loader.exec_module(module)

                self.assertTrue(module.REPLAY_MODE)
                self.assertEqual(module.WALLET_ADDRESS, "")

                module.load_replay_state()
                module.load_replay_soul()
                feed = module.state["feed"]
                decisions = {row["symbol"]: row["decision"] for row in feed}

                self.assertEqual(decisions["RUGDROP"], "BLOCK")
                self.assertEqual(decisions["EARLYBIRD"], "WATCH")
                self.assertEqual(decisions["CLEARPATH"], "PASS")
                self.assertTrue(all(row.get("reason_codes") for row in feed))
                self.assertEqual(module.state["positions"], {})
            finally:
                for name, value in tracked_env.items():
                    if value is None:
                        os.environ.pop(name, None)
                    else:
                        os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
