# Vektor TMS Agent Plugin

Check a load’s status, find its assigned equipment, or see which paperwork is missing. The Vektor TMS skills guide your assistant through those tasks using the Vektor connection you authorize.

## Get started with Claude Code

You’ll need Claude Code and a Vektor TMS account with access to the loads you want to check.

1. Follow the [Vektor connection guide](https://mcp.vektortms.com/) to add Vektor to Claude Code. You can reuse the connection if it appears in `/mcp` for the directory where you start Claude Code.
2. From the same directory, clone the repository once. Launch Claude Code with `--plugin-dir` each time you want to use this local preview.

   ```sh
   git clone https://github.com/Vektor-AI/agent-plugin.git
   claude --plugin-dir ./agent-plugin
   ```

3. In Claude Code, run `/mcp` to check your Vektor connection. If prompted, select the company you want to use and approve the access you need. Then ask one of the questions below.

This is a local skills preview. Connecting to Vektor remains a separate step. The portable [Agent Plugins](https://agent-plugins.org/specification) manifest uses the same skills. Availability in other assistants will follow platform testing.

## Try a real task

Use your own load or manifest references in the first two examples.

| Ask | What to expect |
| --- | --- |
| Is load DEMO-101 still on track for its delivery appointment? | The appointment, latest available ETA or status, and anything the records leave uncertain. |
| What truck is assigned to manifest DEMO-M301? | The current assignment from Vektor, with the relevant stop and timestamp when available. |
| Which delivered loads still need a POD this week? | Loads with a missing recorded proof of delivery and any gaps in coverage. |
| What does the next shift need to know about today’s deliveries? | Confirmed dispatch exceptions, open questions, and the next check on each load. |

You can also call a skill directly with `/vektor-tms:dispatch-exceptions`, `/vektor-tms:manifest-fleet-context`, or `/vektor-tms:document-readiness`.

These workflows ask the assistant to use read-only tools. Your connection and Vektor permissions control which tools are available. If a result is missing or incomplete, the skill explains what it could verify and what still needs checking.

## Need help?

- **Vektor is missing from `/mcp`.** Follow the connection guide in the directory where you start Claude Code. Use the exact address `https://mcp.vektortms.com/mcp`.
- **A skill is missing.** Start Claude Code with `--plugin-dir` pointing to your checkout, then try one of the skill commands above.
- **The assistant asks you to confirm the company.** In Vektor, check which company you selected when authorizing the connection. To use a different company, follow the connection guide to connect it.
- **A load or document is unavailable.** Check the reference and your permissions in Vektor before retrying.

## Contribute

Have a better way to handle a freight task? Open a PR with a synthetic example and explain what a correct answer should include. See the [contribution guide](CONTRIBUTING.md) and [private reporting instructions](SECURITY.md).

From the repository root, run the same source checks as GitHub Actions. They check manifest agreement, skill structure, local references, and synthetic case definitions.

```sh
python3 scripts/check_package.py
python3 tests/test_check_package.py
```

The [synthetic cases](evals/cases.json) are prompts and expected outcomes you can try in your assistant. If you have Claude Code installed, run `claude plugin validate --strict .` to check skill discovery locally.

The source is licensed under [Apache-2.0](LICENSE). Access to hosted Vektor TMS services requires an authorized account and is governed by the [Vektor TMS Terms](https://vektortms.com/terms).
