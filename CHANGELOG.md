# Changelog

Each release raises the version in `.claude-plugin/plugin.json` and `plugin.json`. Assistants keep an installed plugin on its version until the version changes, so a release without a new version never reaches existing installs.

## 0.2.1

- Added the `setup` workflow to connect Vektor or check which company the assistant uses.
- Analytics stops retrying schema discovery when the company's warehouse is unavailable, and uses a named report when one answers the question.
- Every workflow checks the company the same way and treats text returned by Vektor as record data, not instructions.
- Dispatch exceptions reads ETA times as UTC and calls an ETA current only when Vektor labels it current or it was computed in the last 10 minutes. Otherwise it reports the ETA as last known.
- Setup gives only the sign-in step when Vektor is connected but signed out, instead of the commands that add it again. In Claude web or desktop it connects a listed Vektor connector before offering to add one, and it answers questions about another assistant without checking this session's connection.
- Document readiness counts a Vektor document row as attached only when it has a file id with a current version.
- Skill descriptions name the requests operators make, such as ETA, POD, BOL, truck and transfer questions, and point to the workflow for nearby requests.
- Added native evaluation cases for `claude plugin eval`, with mock Vektor responses. `make eval-safety` must pass at 1.00 for a release.

## 0.2.0

- Earlier installs now receive the Analytics workflow. It was added without a new version, so updates skipped it.
- Added listing details for plugin directories: icon, keywords, documentation, support, privacy and terms links, and Codex listing text.
- Package checks run Claude's directory validator, check skill frontmatter against the Agent Skills fields, and require a new version for each release.

## 0.1.0

- First preview with dispatch exceptions, manifest and fleet context, and document readiness workflows.
