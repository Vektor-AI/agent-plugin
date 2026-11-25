import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageCheckTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.preview = Path(temp.name)
        for directory in (".claude-plugin", "skills", "evals", "scripts"):
            shutil.copytree(ROOT / directory, self.preview / directory)
        shutil.copyfile(ROOT / "plugin.json", self.preview / "plugin.json")

    def check_package(self):
        return subprocess.run(
            [sys.executable, "scripts/check_package.py"],
            cwd=self.preview,
            capture_output=True,
            text=True,
            timeout=15,
        )

    def edit_json(self, relative_path, edit):
        path = self.preview / relative_path
        value = json.loads(path.read_text(encoding="utf-8"))
        edit(value)
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_valid_shared_package(self):
        result = self.check_package()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated two manifests", result.stdout)

    def test_disagreeing_manifest_versions(self):
        self.edit_json("plugin.json", lambda manifest: manifest.update(version="9.9.0"))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Manifests disagree on version", result.stderr)

    def test_duplicate_evaluation_case(self):
        self.edit_json("evals/cases.json", lambda cases: cases.append(cases[0]))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid or duplicate case", result.stderr)

    def test_malformed_evaluation_outcome(self):
        self.edit_json("evals/cases.json", lambda cases: cases[0].update(expected="single string"))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid expected outcomes", result.stderr)

    def test_missing_skill_reference(self):
        (self.preview / "skills/dispatch-exceptions/references/shift-handoff.md").unlink()
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing or out-of-scope reference references/shift-handoff.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
