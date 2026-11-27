# Changelog

Each release raises the version in `.claude-plugin/plugin.json` and `plugin.json`. Assistants keep an installed plugin on its version until the version changes, so a release without a new version never reaches existing installs.

## 0.2.4

- In a shift handoff or list, dispatch exceptions puts a load whose risk rests only on a last-known ETA among the items needing a check, not the confirmed exceptions, and words its gap as the ETA's rather than calling the load late.

## 0.2.3

- Dispatch exceptions reads Vektor ETA durations and lateness as minutes and reports the ETA as Vektor computed it, which can include rest and appointment waits. It gives an early, on-time or late verdict only against an agreed appointment window. When the only ETA is last known, a one-load answer, or that load's entry in a handoff, opens with "Current delivery risk is unconfirmed."
- Document readiness also answers a bare "is it ready?" about a load reference by asking which readiness is meant.

## 0.2.2

- Analytics triggers on rate and average questions that a named Vektor report answers, and starts with schema discovery whenever the warehouse tool is available.
- Document readiness resolves each load reference to its Vektor record before reading documents, and reports a load it cannot resolve as unknown.

## 0.2.1

- Added the `setup` workflow to connect Vektor or check which company the assistant uses.
- Analytics stops retrying schema discovery when the company's warehouse is unavailable, and uses a named report when one answers the question.
- Every workflow checks the company the same way and treats text returned by Vektor as record data, not instructions.
- Dispatch exceptions reads ETA times as UTC and calls an ETA current only when Vektor labels it current or it was computed in the last 10 minutes. Otherwise it reports the ETA as last known.
- Setup gives only the sign-in step when Vektor is connected but signed out, instead of the commands that add it again. In Claude web or desktop it connects a listed Vektor connector before offering to add one, and it answers questions about another assistant without checking this session's connection.
- Document readiness counts a Vektor document row as attached only when it has a file id with a current version.
- Setup says when a connection's tool selection cannot confirm the company, and sends Claude Code users whose Vektor connector comes from their Claude account to sign in there. Analytics uses a named report when the connection has no schema tool.
- Skill descriptions name the requests operators make, such as ETA, POD, BOL, truck and transfer questions, and point to the workflow for nearby requests.

## 0.2.0

- Earlier installs now receive the Analytics workflow. It was added without a new version, so updates skipped it.
- Added listing details for plugin directories: icon, keywords, documentation, support, privacy and terms links, and Codex listing text.
- Package checks run Claude's directory validator, check skill frontmatter against the Agent Skills fields, and require a new version for each release.

## 0.1.0

- First preview with dispatch exceptions, manifest and fleet context, and document readiness workflows.
