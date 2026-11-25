# Vektor TMS for your assistant

Check whether a delivery is on track, find the equipment assigned to a manifest, and see which delivered loads still need paperwork. The Vektor plugin gives your assistant workflows for each task. It uses the connection and company access you authorize in Vektor TMS.

## Get started

Use **Claude Code** or **Codex CLI** with plugin support. You’ll need a Vektor TMS account with access to the company you want to work in.

### Claude Code

1. Follow the [Vektor connection guide](https://mcp.vektortms.com/) from the directory where you use Claude Code. If Vektor already appears in `/mcp`, you can reuse that connection.

2. Run this in Claude Code:

   ```text
   /plugin install vektor --marketplace Vektor-AI/agent-plugin
   ```

3. Run `/reload-plugins` if prompted, then check `/mcp`. Sign in and choose the company you want to work in.

### Codex CLI

1. Install the skills:

   ```sh
   codex plugin marketplace add Vektor-AI/agent-plugin
   codex plugin add vektor@vektor-plugins
   ```

2. If you haven’t connected Vektor yet, add the remote server:

   ```sh
   codex mcp add vektor --url https://mcp.vektortms.com/mcp
   ```

3. Follow the sign-in prompt and choose your company. If the connection needs sign-in later, run `codex mcp login vektor`. Open a new Codex session to use the skills.

### Other assistants

Use `https://mcp.vektortms.com/mcp` in assistants that support remote MCP and OAuth. This source preview’s install instructions cover Claude Code and Codex CLI. Host directories have their own publishing and installation steps.

## Try a task

Ask in your own words. To pick a skill yourself, run a Claude Code command below or type `@` in Codex and search for its name.

| Ask your assistant | Claude Code command |
| --- | --- |
| Is load DEMO-101 still on track for delivery? | `/vektor:dispatch-exceptions` |
| What truck is assigned to manifest DEMO-M301? | `/vektor:manifest-fleet-context` |
| Which loads delivered this week still need a POD? | `/vektor:document-readiness` |
| What delivery exceptions should the next shift know about? | `/vektor:dispatch-exceptions` |

Replace the example IDs with references from your company. A typical answer includes the source records and what still needs checking. The workflows use read-only tools. Your Vektor permissions determine which records the assistant can see.

## Troubleshoot

- **Vektor is missing or signed out.** Check `/mcp` in your assistant. Use the exact URL `https://mcp.vektortms.com/mcp` when connecting.
- **The assistant asks about a company.** Check which company you selected at sign-in. Use the [connection guide](https://mcp.vektortms.com/) to authorize another company.
- **The assistant can’t find a load or document.** Check the reference, date range, and your permissions in Vektor.
- **You used an earlier preview.** Install `vektor` and replace any saved `/vektor-tms:…` commands with `/vektor:…`. You can reuse your Vektor connection.

## Share feedback

If a task took too many steps, a tool was missing, or an answer was hard to use, try this prompt:

> Draft feedback about this Vektor task. Include what I tried, what I expected, and what happened. Use synthetic examples and leave out customer, load, and account details. Show me the draft.

Review the draft and send it through [Vektor support](https://vektortms.com/contact). For a reproducible plugin issue with synthetic data, you can also use [GitHub Issues](https://github.com/Vektor-AI/agent-plugin/issues).

## Contribute

The skills are open source under [Apache-2.0](LICENSE). To improve a workflow, start with the [contribution guide](CONTRIBUTING.md) and the [synthetic cases](evals/cases.json). Report security findings through the [private reporting instructions](SECURITY.md).

Access to hosted Vektor TMS services is governed by the [Vektor TMS Terms](https://vektortms.com/terms).
