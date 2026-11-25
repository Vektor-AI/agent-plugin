# Vektor TMS Agent Plugin

Workflow skills for freight operators using Vektor TMS with an AI assistant. The source preview covers dispatch exceptions, manifest and equipment context, and document readiness. It uses the Vektor connection and permissions you already have in your assistant. Grant only the access you need for the work you want to do.

## Try the source preview

In Claude Code, load this checkout for the current session:

```sh
claude --plugin-dir .
```

Use `/vektor-tms:dispatch-exceptions`, `/vektor-tms:manifest-fleet-context`, or `/vektor-tms:document-readiness`. You can also ask in ordinary language:

| Ask | What to expect |
| --- | --- |
| Is load DEMO-101 still on track for its delivery appointment? | The appointment, latest available ETA or status, and anything the records leave uncertain. |
| What truck is assigned to manifest DEMO-M301? | The current assignment from Vektor, with the relevant stop and timestamp when available. |
| Which delivered loads still need a POD this week? | Loads with a missing recorded proof of delivery and any gaps in coverage. |

The examples use synthetic identifiers. For a connected account, the assistant works with the tools your connection exposes. When a required tool or record is unavailable, the skill identifies the missing information and gives you the next step. The preview contains skills only. [Vektor’s connection guide](https://mcp.vektortms.com/) provides setup and the exact MCP address for existing connections.

The same `skills/` directory is used by the portable [Agent Plugins](https://agent-plugins.org/specification) manifest and the Claude Code manifest. The supported host and marketplace list will follow testing of the connected release.

## Develop

Run `python3 scripts/check_package.py` from the repository root. Claude Code authors can also run `claude plugin validate --strict .`. Use the [synthetic cases](evals/cases.json) to exercise workflow activation, available data, and partial or missing results. Follow the [contribution guide](CONTRIBUTING.md) and [private reporting instructions](SECURITY.md).

The source is licensed under [Apache-2.0](LICENSE). Access to hosted Vektor TMS services requires an authorized account and is governed by the [Vektor TMS Terms](https://vektortms.com/terms).
