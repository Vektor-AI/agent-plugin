# Contributing

Open a pull request for workflow instructions, synthetic examples, or package checks. Describe the operator’s task, the evidence the assistant should inspect, and what you checked. Include the assistant and version you tested.

Edit the shared skill in `skills/`. Use language an operator would use when describing the task. Add a [synthetic case](evals/cases.json) for a correct outcome and one for a nearby request or missing-data state that should produce a different result. Update both manifests and marketplace entries if the plugin identity changes.

## Check your changes

Install [uv](https://docs.astral.sh/uv/) and [actionlint 1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12). Run the same source checks used by GitHub Actions:

```sh
make check
```

The checks cover manifest and marketplace consistency, skill frontmatter, local links, synthetic case definitions, and workflow configuration. The synthetic case definitions also give you prompts and outcomes to try in your assistant. To see which skills Claude Code loads, run `claude plugin validate --strict .`.

Keep customer details, conversation logs, access tokens, raw freight documents, and internal configuration out of issues and pull requests. Use the [private reporting channel](SECURITY.md) for security findings. Package publication and marketplace configuration are maintainer changes.
