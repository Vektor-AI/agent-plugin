"""Check the public package without connecting to Vektor or an assistant."""

import json
import re
from collections.abc import Hashable
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)", re.DOTALL)
MARKDOWN_LINK = re.compile(r"\]\((?:<([^>\n]+)>|([^\s)]+))")


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict:
        self.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, Hashable) or key in mapping:
                raise ConstructorError(
                    "while reading frontmatter",
                    node.start_mark,
                    f"invalid or duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def read_json(path: str):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SystemExit(f"{path}: {error}") from error


def require(condition, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def check_manifests() -> None:
    portable = read_json("plugin.json")
    schema = read_json("schemas/plugin.schema.json")
    error = next(Draft202012Validator(schema).iter_errors(portable), None)
    require(error is None, f"plugin.json: {error.message}" if error else "")
    require(
        portable.get("$schema") == schema["$id"], "plugin.json must identify the vendored schema"
    )

    claude = read_json(".claude-plugin/plugin.json")
    require(isinstance(claude, dict), "Expected a Claude plugin manifest object")
    for field in ("name", "version", "description", "author", "license", "homepage", "repository"):
        require(
            field in portable and portable[field] == claude.get(field),
            f"Manifests disagree on {field}",
        )
    require(portable["name"] == "vektor", "The install ID must be vektor")
    interface = portable.get("extensions", {}).get("com.openai", {}).get("interface", {})
    require(
        interface.get("displayName") == claude.get("displayName") == "Vektor TMS",
        "Manifests disagree on the Vektor TMS display name",
    )

    check_marketplace(".agents/plugins/marketplace.json", {"source": "local", "path": "./"})
    check_marketplace(".claude-plugin/marketplace.json", "./")


def check_marketplace(path: str, source: dict[str, str] | str) -> None:
    marketplace = read_json(path)
    require(isinstance(marketplace, dict), f"{path}: expected a marketplace object")
    require(
        marketplace.get("name") == "vektor-plugins",
        f"{path}: the marketplace ID must be vektor-plugins",
    )
    plugins = marketplace.get("plugins")
    require(
        isinstance(plugins, list) and len(plugins) == 1 and isinstance(plugins[0], dict),
        f"{path}: expected one plugin",
    )
    require(
        plugins[0].get("name") == "vektor" and plugins[0].get("source") == source,
        f"{path}: the marketplace entry must point to this plugin's repository root",
    )


def check_links(path: Path, body: str, scope: Path) -> None:
    for bracketed, bare in MARKDOWN_LINK.findall(body):
        link = urlsplit(bracketed or bare)
        reference = unquote(link.path)
        if not reference or link.scheme or link.netloc:
            continue
        target = (path.parent / reference).resolve()
        require(
            target.is_relative_to(scope) and target.exists(),
            f"Missing or out-of-scope reference {reference} in {path.relative_to(ROOT)}",
        )


def check_skills() -> set[str]:
    skills_root = ROOT / "skills"
    require(skills_root.is_dir() and not skills_root.is_symlink(), "Expected a skills directory")
    skill_dirs = sorted(skills_root.iterdir())
    require(skill_dirs, "Expected at least one skill")
    names = set()
    for directory in skill_dirs:
        name = directory.name
        require(
            directory.is_dir() and not directory.is_symlink(), f"Invalid skill directory {name}"
        )
        require(len(name) <= 64 and NAME.fullmatch(name), f"Invalid skill name {name}")
        for file in directory.rglob("*"):
            require(not file.is_symlink(), f"Unexpected symlink {file.relative_to(ROOT)}")

        skill_file = directory / "SKILL.md"
        require(skill_file.is_file(), f"Expected SKILL.md in {name}")
        match = FRONTMATTER.fullmatch(skill_file.read_text(encoding="utf-8"))
        require(match and match.group(2).strip(), f"Incomplete skill {name}")
        try:
            metadata = yaml.load(match.group(1), Loader=UniqueKeyLoader)
        except yaml.YAMLError as error:
            raise SystemExit(f"Invalid frontmatter in {name}: {error}") from error
        require(isinstance(metadata, dict), f"Expected frontmatter fields in {name}")
        require(metadata.get("name") == name, f"Skill frontmatter name must match {name}")
        description = metadata.get("description")
        require(
            isinstance(description, str) and description.strip() and len(description) <= 1024,
            f"Invalid description for {name}",
        )
        require(metadata.get("license") == "Apache-2.0", f"Missing Apache-2.0 license for {name}")
        require("allowed-tools" not in metadata, f"Unexpected tool preapproval for {name}")
        for document in directory.rglob("*.md"):
            body = (
                match.group(2) if document == skill_file else document.read_text(encoding="utf-8")
            )
            check_links(document, body, directory)
        names.add(name)
    return names


def check_cases(skills: set[str]) -> int:
    seen = set()
    covered = set()
    cases = read_json("evals/cases.json")
    require(isinstance(cases, list) and cases, "Expected a list of synthetic cases")
    for case in cases:
        require(isinstance(case, dict), "Each synthetic case must be an object")
        case_id = case.get("id")
        require(
            isinstance(case_id, str) and NAME.fullmatch(case_id) and case_id not in seen,
            f"Invalid or duplicate case {case_id}",
        )
        seen.add(case_id)
        skill = case.get("skill")
        require(
            "skill" in case and (skill is None or isinstance(skill, str) and skill in skills),
            f"Unknown or missing skill {skill} in {case_id}",
        )
        covered.add(skill)
        for field in ("prompt", "fixture"):
            value = case.get(field)
            require(isinstance(value, str) and value.strip(), f"Invalid {field} in {case_id}")
        outcomes = case.get("expected")
        require(
            isinstance(outcomes, list)
            and outcomes
            and all(isinstance(outcome, str) and outcome.strip() for outcome in outcomes),
            f"Invalid expected outcomes in {case_id}",
        )
    require(
        skills | {None} == covered, "Each skill and a non-activation case need evaluation coverage"
    )
    return len(cases)


if __name__ == "__main__":
    check_manifests()
    for path in ("README.md", "CONTRIBUTING.md", "SECURITY.md", "schemas/README.md"):
        document = ROOT / path
        check_links(document, document.read_text(encoding="utf-8"), ROOT)
    skills = check_skills()
    count = check_cases(skills)
    print(
        f"Validated manifests, marketplaces, local links, {len(skills)} skills and {count} synthetic cases."
    )
