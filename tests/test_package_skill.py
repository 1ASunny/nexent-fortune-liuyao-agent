from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.package_skill import build, validate


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skill" / "fortune-liuyao"


class PackageTests(unittest.TestCase):
    def test_package_is_reproducible_and_rooted_for_nexent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first, second = Path(temporary) / "one.zip", Path(temporary) / "two.zip"
            build(SOURCE, first)
            build(SOURCE, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                names = archive.namelist()
                self.assertIn("SKILL.md", names)
                self.assertIn("scripts/run_liuyao.py", names)
                self.assertIn("vendor/lunar_python/__init__.py", names)
                self.assertFalse(any("__pycache__" in name for name in names))

    def test_validation(self) -> None:
        validate(SOURCE)


if __name__ == "__main__":
    unittest.main()
