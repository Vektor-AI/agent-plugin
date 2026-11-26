# Changelog

Each release raises the version in `.claude-plugin/plugin.json` and `plugin.json`. Assistants keep an installed plugin on its version until the version changes, so a release without a new version never reaches existing installs.

## 0.2.2

- Added finance review previews for truck settlements, carrier bills and staff pay. They use a separate finance connection approved by your organization.

## 0.2.0

- Earlier installs now receive the Analytics workflow. It was added without a new version, so updates skipped it.
- Added listing details for plugin directories: icon, keywords, documentation, support, privacy and terms links, and Codex listing text.
- Package checks run Claude's directory validator, check skill frontmatter against the Agent Skills fields, and require a new version for each release.

## 0.1.0

- First preview with dispatch exceptions, manifest and fleet context, and document readiness workflows.
