"""Check the shared identity and source preview's portable components."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
REFERENCE_LINK = re.compile(r"\]\((references/[^\s)#]+)(?:#[^)]*)?\)")


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def check_manifests():
    portable = read_json("plugin.json")
    claude = read_json(".claude-plugin/plugin.json")
    for field in ("name", "version", "description", "author"):
        require(portable[field] == claude[field], f"Manifests disagree on {field}")
    require(portable["name"] == "vektor-tms", "The stable install ID must be vektor-tms")
    require(
        portable["extensions"]["com.openai"]["interface"]["displayName"]
        == claude["displayName"] == "Vektor TMS",
        "Manifests disagree on the Vektor TMS display name",
    )


def check_skills():
    skill_dirs = sorted((ROOT / "skills").iterdir())
    require(bool(skill_dirs), "Expected at least one skill")
    names = set()
    for directory in skill_dirs:
        name = directory.name
        require(directory.is_dir() and not directory.is_symlink(), f"Invalid skill directory {name}")
        require(len(name) <= 64 and NAME.fullmatch(name), f"Invalid skill name {name}")
        skill_file = directory / "SKILL.md"
        require(skill_file.is_file() and not skill_file.is_symlink(), f"Expected SKILL.md in {name}")
        opening, separator, contents = skill_file.read_text(encoding="utf-8").partition("---\n")
        header, closing, body = contents.partition("---\n")
        require(not opening and separator and closing and body.strip(), f"Incomplete skill {name}")
        entries = [line.split(": ", 1) for line in header.strip().splitlines()]
        require(all(len(entry) == 2 for entry in entries), f"Invalid frontmatter in {name}")
        metadata = dict(entries)
        require(len(metadata) == len(entries), f"Duplicate frontmatter field in {name}")
        require(metadata.get("name") == name, f"Skill frontmatter name must match {name}")
        require(0 < len(metadata.get("description", "")) <= 1024, f"Invalid description for {name}")
        require(metadata.get("license") == "Apache-2.0", f"Missing Apache-2.0 license for {name}")
        require("allowed-tools" not in metadata, f"Unexpected tool preapproval for {name}")
        for reference in REFERENCE_LINK.findall(body):
            path = directory / reference
            require(
                path.is_file() and directory in path.resolve().parents,
                f"Missing or out-of-scope reference {reference} in {name}",
            )
        names.add(name)
    return names


def check_cases(skills):
    seen = set()
    covered = set()
    cases = read_json("evals/cases.json")
    for case in cases:
        case_id = case["id"]
        require(NAME.fullmatch(case_id) and case_id not in seen, f"Invalid or duplicate case {case_id}")
        seen.add(case_id)
        skill = case["skill"]
        require(skill is None or skill in skills, f"Unknown skill {skill} in {case_id}")
        covered.add(skill)
        for field in ("prompt", "fixture"):
            require(bool(case[field].strip()), f"Empty {field} in {case_id}")
        outcomes = case["expected"]
        require(
            isinstance(outcomes, list) and outcomes
            and all(isinstance(outcome, str) and outcome.strip() for outcome in outcomes),
            f"Invalid expected outcomes in {case_id}",
        )
    require(skills | {None} == covered, "Each skill and a non-activation case need evaluation coverage")
    return len(cases)


if __name__ == "__main__":
    check_manifests()
    skills = check_skills()
    count = check_cases(skills)
    print(f"Validated two manifests, {len(skills)} skills and {count} synthetic case definitions.")
