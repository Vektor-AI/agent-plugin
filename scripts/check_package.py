"""Check the public package without connecting to Vektor or an assistant."""

import hashlib
import json
import os
import re
import subprocess
from collections.abc import Hashable
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SCHEMA_SHA256 = "0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)", re.DOTALL)
MARKDOWN_LINK = re.compile(r"\]\((?:<([^>\n]+)>|([^\s)]+))")
SKILL_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
RESERVED_WORDS = ("anthropic", "claude")
LISTING_URLS = ("documentationUrl", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl")
# Git pathspecs for the files installed copies receive. A change to any of them is a release.
SHIPPED_PATHS = (
    "skills",
    "hooks",
    "agents",
    "commands",
    ".mcp.json",
    "mcp.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/icon.png",
    "plugin.json",
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


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


def read_frontmatter(path: Path) -> tuple[dict, str]:
    match = FRONTMATTER.fullmatch(path.read_text(encoding="utf-8"))
    require(match, f"Expected frontmatter in {path.relative_to(ROOT)}")
    try:
        metadata = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise SystemExit(f"Invalid frontmatter in {path.relative_to(ROOT)}: {error}") from error
    require(isinstance(metadata, dict), f"Expected frontmatter fields in {path.relative_to(ROOT)}")
    return metadata, match.group(2)


def parse_version(value) -> tuple[int, int, int]:
    parts = value.split(".") if isinstance(value, str) else []
    require(
        len(parts) == 3 and all(part.isdigit() for part in parts),
        f"Expected a MAJOR.MINOR.PATCH plugin version, got {value!r}",
    )
    return tuple(int(part) for part in parts)


def is_https_url(value) -> bool:
    return (
        isinstance(value, str)
        and urlsplit(value).scheme == "https"
        and bool(urlsplit(value).netloc)
    )


def check_manifests() -> None:
    portable = read_json("plugin.json")
    schema_path = ROOT / "schemas/plugin.schema.json"
    schema_bytes = schema_path.read_bytes()
    require(
        hashlib.sha256(schema_bytes).hexdigest() == SCHEMA_SHA256,
        "Vendored manifest schema differs from the pinned upstream revision",
    )
    schema = json.loads(schema_bytes)
    error = next(Draft202012Validator(schema).iter_errors(portable), None)
    require(error is None, f"plugin.json: {error.message}" if error else "")
    require(
        portable.get("$schema") == schema["$id"], "plugin.json must identify the vendored schema"
    )

    claude = read_json(".claude-plugin/plugin.json")
    require(isinstance(claude, dict), "Expected a Claude plugin manifest object")
    fields = ("name", "version", "description", "author", "license", "homepage", "repository")
    for field in (*fields, "keywords"):
        require(
            field in portable and portable[field] == claude.get(field),
            f"Manifests disagree on {field}",
        )
    require(portable["name"] == "vektor", "The install ID must be vektor")
    interface = portable.get("extensions", {}).get("com.openai", {}).get("interface", {})
    require(
        isinstance(interface, dict)
        and interface.get("displayName") == claude.get("displayName") == "Vektor TMS",
        "Manifests disagree on the Vektor TMS display name",
    )
    parse_version(claude.get("version"))
    check_listing(claude, interface)

    check_marketplace(".agents/plugins/marketplace.json", {"source": "local", "path": "./"})
    check_marketplace(".claude-plugin/marketplace.json", "./")


def check_listing(claude: dict, interface: dict) -> None:
    for field in LISTING_URLS:
        require(is_https_url(claude.get(field)), f"{field} must be an https URL")
    icon = claude.get("icon")
    require(isinstance(icon, str) and icon.startswith("./"), "icon must be a ./ path in the plugin")
    icon_path = (ROOT / icon).resolve()
    require(
        icon_path.is_relative_to(ROOT) and icon_path.is_file(),
        f"Missing or out-of-scope icon {icon}",
    )
    require(icon_path.read_bytes().startswith(PNG_SIGNATURE), f"icon {icon} must be a PNG image")
    require(
        interface.get("privacyPolicyURL") == claude["privacyPolicyUrl"]
        and interface.get("termsOfServiceURL") == claude["termsOfServiceUrl"],
        "Manifests disagree on the privacy policy or terms URL",
    )
    require(interface.get("logo") == icon, "The Codex logo must use the plugin icon")


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
    if isinstance(source, dict):
        require(
            plugins[0].get("policy")
            == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            f"{path}: expected an available Codex marketplace entry with ON_INSTALL authentication",
        )
    else:
        owner = marketplace.get("owner")
        require(
            isinstance(owner, dict) and owner.get("name") == "Vektor TMS",
            f"{path}: expected Vektor TMS as marketplace owner",
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
        require(
            not any(word in name for word in RESERVED_WORDS), f"Reserved word in skill name {name}"
        )
        for file in directory.rglob("*"):
            require(not file.is_symlink(), f"Unexpected symlink {file.relative_to(ROOT)}")

        skill_file = directory / "SKILL.md"
        require(skill_file.is_file(), f"Expected SKILL.md in {name}")
        metadata, body = read_frontmatter(skill_file)
        require(body.strip(), f"Incomplete skill {name}")
        unsupported = sorted(set(metadata) - SKILL_KEYS)
        require(not unsupported, f"Unsupported frontmatter key {', '.join(unsupported)} in {name}")
        require(metadata.get("name") == name, f"Skill frontmatter name must match {name}")
        description = metadata.get("description")
        require(
            isinstance(description, str) and description.strip() and len(description) <= 1024,
            f"Invalid description for {name}",
        )
        require(
            "<" not in description and ">" not in description,
            f"Angle brackets in the description for {name}",
        )
        require(metadata.get("license") == "Apache-2.0", f"Missing Apache-2.0 license for {name}")
        require("allowed-tools" not in metadata, f"Unexpected tool preapproval for {name}")
        for document in directory.rglob("*.md"):
            text = body if document == skill_file else document.read_text(encoding="utf-8")
            check_links(document, text, directory)
            if document != skill_file:
                check_reference_depth(document, text)
        names.add(name)
    return names


def check_reference_depth(path: Path, body: str) -> None:
    for bracketed, bare in MARKDOWN_LINK.findall(body):
        link = urlsplit(bracketed or bare)
        if link.scheme or link.netloc or not link.path:
            continue
        raise SystemExit(
            f"Reference files must not link to other files: {path.relative_to(ROOT)} links "
            f"{unquote(link.path)}"
        )


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


def check_changelog(version: str) -> None:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    require(
        re.search(rf"^## {re.escape(version)}[ \t]*$", changelog, re.MULTILINE),
        f"CHANGELOG.md needs a ## {version} entry",
    )


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False
    )
    require(result.returncode == 0, f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def check_release(base: str, version: str) -> str:
    # NUL-separated names are never quoted, and without rename detection a moved
    # file lists both its old and its new path.
    changed = git("diff", "--name-only", "--no-renames", "-z", base, "--", *SHIPPED_PATHS)
    changed += git("ls-files", "--others", "--exclude-standard", "-z", "--", *SHIPPED_PATHS)
    shipped = sorted(filter(None, changed.split("\0")))
    if not shipped:
        return "no shipped changes"
    try:
        previous = json.loads(git("show", f"{base}:.claude-plugin/plugin.json"))["version"]
    except (ValueError, KeyError) as error:
        raise SystemExit(f"Cannot read the plugin version at {base}") from error
    require(
        parse_version(version) > parse_version(previous),
        f"Raise the plugin version: {shipped[0]} changed since {base}, "
        f"but version {version} is not above {previous}",
    )
    return f"version {previous} -> {version}"


if __name__ == "__main__":
    check_manifests()
    version = read_json(".claude-plugin/plugin.json")["version"]
    check_changelog(version)
    documents = ("README.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "RELEASING.md")
    for path in (*documents, "schemas/README.md"):
        document = ROOT / path
        check_links(document, document.read_text(encoding="utf-8"), ROOT)
    skills = check_skills()
    count = check_cases(skills)
    base = os.environ.get("PLUGIN_BASE_REF")
    release = check_release(base, version) if base else "release check skipped"
    print(
        f"Validated manifests, marketplaces, local links, {len(skills)} skills and {count} "
        f"synthetic cases ({release})."
    )
