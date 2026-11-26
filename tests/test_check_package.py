import json
import os
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
        for document in (
            "plugin.json",
            "README.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "CHANGELOG.md",
            "RELEASING.md",
            "LICENSE",
        ):
            shutil.copyfile(ROOT / document, self.preview / document)

    def check_package(self, base=None):
        env = {key: value for key, value in os.environ.items() if key != "PLUGIN_BASE_REF"}
        if base:
            env["PLUGIN_BASE_REF"] = base
        return subprocess.run(
            [sys.executable, "scripts/check_package.py"],
            cwd=self.preview,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )

    def git(self, *args):
        identity = {
            "GIT_AUTHOR_NAME": "Package test",
            "GIT_AUTHOR_EMAIL": "package-test@example.com",
            "GIT_COMMITTER_NAME": "Package test",
            "GIT_COMMITTER_EMAIL": "package-test@example.com",
        }
        return subprocess.run(
            ["git", *args],
            cwd=self.preview,
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
            env={**os.environ, **identity},
        ).stdout.strip()

    def snapshot(self):
        """Record the copied package as a base commit without running commit hooks."""
        if not (self.preview / ".git").exists():
            self.git("init", "--quiet")
        self.git("add", "--all")
        return self.git("commit-tree", self.git("write-tree"), "-m", "base")

    def edit_skill(self, name="dispatch-exceptions"):
        skill = self.preview / f"skills/{name}/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nCheck the stop.\n", "utf-8")

    def set_version(self, version):
        for manifest in ("plugin.json", ".claude-plugin/plugin.json"):
            self.edit_json(manifest, lambda value: value.update(version=version))
        with (self.preview / "CHANGELOG.md").open("a", encoding="utf-8") as changelog:
            changelog.write(f"\n## {version}\n\n- Test release.\n")

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

    def test_missing_listing_url(self):
        self.edit_json(".claude-plugin/plugin.json", lambda manifest: manifest.pop("supportUrl"))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("supportUrl must be an https URL", result.stderr)

    def test_icon_must_be_png(self):
        (self.preview / ".claude-plugin/icon.png").write_bytes(b"not an image")
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be a PNG image", result.stderr)

    def test_disagreeing_keywords(self):
        self.edit_json("plugin.json", lambda manifest: manifest["keywords"].append("extra"))
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Manifests disagree on keywords", result.stderr)

    def test_disagreeing_codex_privacy_link(self):
        self.edit_json(
            "plugin.json",
            lambda manifest: manifest["extensions"]["com.openai"]["interface"].update(
                privacyPolicyURL="https://example.com/privacy"
            ),
        )
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("disagree on the privacy policy or terms URL", result.stderr)

    def test_unsupported_skill_frontmatter_key(self):
        skill = self.preview / "skills/analytics/SKILL.md"
        original = skill.read_text(encoding="utf-8")
        skill.write_text(original.replace("---\n", "---\nargument-hint: week\n", 1), "utf-8")
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported frontmatter key argument-hint in analytics", result.stderr)

    def test_angle_brackets_in_description(self):
        skill = self.preview / "skills/analytics/SKILL.md"
        original = skill.read_text(encoding="utf-8")
        skill.write_text(original.replace("description: ", "description: <b>Bold</b> ", 1), "utf-8")
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Angle brackets in the description for analytics", result.stderr)

    def test_reference_links_another_file(self):
        reference = self.preview / "skills/dispatch-exceptions/references/shift-handoff.md"
        with reference.open("a", encoding="utf-8") as handle:
            handle.write("\nSee [the skill](../SKILL.md).\n")
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Reference files must not link to other files", result.stderr)

    def test_changelog_needs_current_version(self):
        changelog = self.preview / "CHANGELOG.md"
        version = json.loads((self.preview / "plugin.json").read_text(encoding="utf-8"))["version"]
        changelog.write_text(
            changelog.read_text(encoding="utf-8").replace(f"## {version}", "## Unreleased"),
            "utf-8",
        )
        result = self.check_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"CHANGELOG.md needs a ## {version} entry", result.stderr)

    def test_release_requires_a_new_version(self):
        base = self.snapshot()
        self.edit_skill()
        result = self.check_package(base)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "Raise the plugin version: skills/dispatch-exceptions/SKILL.md", result.stderr
        )

    def test_release_with_a_new_version(self):
        base = self.snapshot()
        self.edit_skill()
        self.set_version("9.0.0")
        result = self.check_package(base)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("-> 9.0.0", result.stdout)

    def test_release_compares_the_target_branch_tip(self):
        # Another change already released 9.0.0 on the target branch. A branch that
        # also chose 9.0.0 for its own workflow change must raise the version again.
        self.set_version("9.0.0")
        tip = self.snapshot()
        self.edit_skill()
        result = self.check_package(tip)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("the version is still 9.0.0", result.stderr)

    def test_documentation_change_needs_no_new_version(self):
        base = self.snapshot()
        with (self.preview / "README.md").open("a", encoding="utf-8") as readme:
            readme.write("\nMore help.\n")
        result = self.check_package(base)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no shipped changes", result.stdout)


if __name__ == "__main__":
    unittest.main()
