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
        for directory in (".agents", ".claude-plugin", "skills", "evals", "schemas", "scripts"):
            shutil.copytree(ROOT / directory, self.preview / directory)
        for document in ("plugin.json", "README.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE"):
            shutil.copyfile(ROOT / document, self.preview / document)

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
        self.assertIn("Validated manifests, marketplaces", result.stdout)

    def test_disagreeing_manifest_versions(self):
        self.edit_json("plugin.json", lambda manifest: manifest.update(version="9.9.0"))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Manifests disagree on version", result.stderr)

    def test_invalid_portable_manifest(self):
        self.edit_json("plugin.json", lambda manifest: manifest.update(version=1))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugin.json: 1 is not of type", result.stderr)

    def test_marketplace_entry_points_elsewhere(self):
        self.edit_json(
            ".agents/plugins/marketplace.json",
            lambda marketplace: marketplace["plugins"][0]["source"].update(path="../"),
        )
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "marketplace entry must point to this plugin's repository root", result.stderr
        )

    def test_invalid_codex_marketplace_policy(self):
        self.edit_json(
            ".agents/plugins/marketplace.json",
            lambda marketplace: marketplace["plugins"][0]["policy"].update(
                authentication="ON_INSTALL_TYPO"
            ),
        )
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("with ON_INSTALL authentication", result.stderr)

    def test_missing_claude_marketplace_owner(self):
        self.edit_json(
            ".claude-plugin/marketplace.json", lambda marketplace: marketplace.pop("owner")
        )
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected Vektor TMS as marketplace owner", result.stderr)

    def test_modified_vendored_schema(self):
        self.edit_json("schemas/plugin.schema.json", lambda schema: schema.pop("required"))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema differs from the pinned upstream revision", result.stderr)

    def test_missing_readme_link(self):
        with (self.preview / "README.md").open("a", encoding="utf-8") as readme:
            readme.write("\n[Invalid](missing.md)\n")
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing or out-of-scope reference missing.md in README.md", result.stderr)

    def test_duplicate_skill_frontmatter(self):
        skill = self.preview / "skills/dispatch-exceptions/SKILL.md"
        original = skill.read_text(encoding="utf-8")
        skill.write_text(original.replace("---\n", "---\nname: duplicate\n", 1), encoding="utf-8")
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid or duplicate key 'name'", result.stderr)

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
        self.assertIn(
            "Missing or out-of-scope reference references/shift-handoff.md", result.stderr
        )


if __name__ == "__main__":
    unittest.main()
