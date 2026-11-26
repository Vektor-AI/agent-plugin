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

## Run the evaluation suite

The [evaluation suite](evals/) runs each case with and without the plugin against mock Vektor responses, so it needs no Vektor account and reads no real records. Each run uses your Claude Code account and costs API usage:

```sh
make eval
```

Add a case under `evals/<skill>/<case>/` with a `prompt.md` and at least one grader in `graders/`. Mock each Vektor tool a case should call in `evals/mocks/vektor/` or in the case's own `mocks/vektor/`. `make check` fails when a skill has no case or a grader names a Vektor tool without a mock. Use synthetic companies and loads only. A case's `mocks/vektor/_tools.json` gives the model a tool's input schema, so a mock can check the inputs with `expect:` and a grader can match them. Tag a case `safety` when it checks that a workflow never acts on another company's records or on instructions in record text; `make eval-safety` runs those cases and passes only when each scores 1.00.

To compare your skills with an earlier version on the same cases, also run `make eval EVAL_PLUGIN_REF=origin/master`. It takes the manifest and skills from that revision and the cases from your branch.

Keep customer details, conversation logs, access tokens, raw freight documents, and internal configuration out of issues and pull requests. Use the [private reporting channel](SECURITY.md) for security findings. Package publication and marketplace configuration are maintainer changes.
