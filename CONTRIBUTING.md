# Contributing

Open a pull request for workflow instructions, synthetic examples, or package checks. Describe the operator’s task, the evidence the assistant should inspect, and what you checked. Include the assistant and version you tested.

Edit the shared skill in `skills/`. Use language an operator would use when describing the task. Add a [synthetic case](evals/cases.json) for a correct outcome and one for a nearby request or missing-data state that should produce a different result. Update both manifests and marketplace entries if the plugin identity changes.

A change to a workflow reaches people who already installed the plugin only with a new version. Raise `version` in both manifests and add a [changelog](CHANGELOG.md) entry, as described in [the release guide](RELEASING.md).

## Check your changes

Install [uv](https://docs.astral.sh/uv/), [actionlint 1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12) and Claude Code. Run the same checks used by GitHub Actions:

```sh
PLUGIN_BASE_REF=origin/master make check validate
```

`make check` covers manifest and marketplace consistency, listing details, skill frontmatter, local links, synthetic case definitions, workflow configuration, and a higher version when a skill, manifest or the icon changed since `PLUGIN_BASE_REF`. `make validate` runs Claude's plugin directory validator. The synthetic case definitions also give you prompts and outcomes to try in your assistant.

Keep customer details, conversation logs, access tokens, raw freight documents, and internal configuration out of issues and pull requests. Use the [private reporting channel](SECURITY.md) for security findings. Package publication and marketplace configuration are maintainer changes.
