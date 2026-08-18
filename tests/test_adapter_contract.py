from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.fortune_runtime import _run_dir, cast_line


class AdapterContractTests(unittest.TestCase):
    def test_run_id_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                _run_dir("../session", Path(temporary))

    def test_single_line_contract(self) -> None:
        value = cast_line(1)
        self.assertEqual(value["position"], 1)
        self.assertIn(value["value"], (6, 7, 8, 9))
        self.assertEqual(value["randomSource"], "python_secrets")


if __name__ == "__main__":
    unittest.main()
