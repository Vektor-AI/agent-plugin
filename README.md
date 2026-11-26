# Vektor TMS for your assistant

Check whether a delivery is on track, find the equipment assigned to a manifest, and see which delivered loads still need paperwork. The Vektor plugin gives your assistant workflows for each task. It uses the connection and company access you authorize in Vektor TMS.

## Get started

Use **Claude Code** or **Codex CLI** with plugin support. You’ll need a Vektor TMS account with access to the company you want to work in.

### Claude Code

1. In Claude Code 2.1.275 or newer, follow the [Vektor connection guide](https://mcp.vektortms.com/) from the directory where you use Claude Code. If Vektor already appears in `/mcp`, you can reuse that connection.

2. Run this in Claude Code:

   ```text
   /plugin install vektor --marketplace Vektor-AI/agent-plugin
   ```

3. Confirm the marketplace source and choose where to install the plugin. Run `/reload-plugins` if prompted, then check `/mcp`. Sign in and choose your company.

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

Ask in your own words. To choose a skill directly, run a Claude Code command below or type `$` in Codex CLI and select the skill by name.

| Ask your assistant | Claude Code command |
| --- | --- |
| How many orders did we deliver last full week? | `/vektor:analytics` |
| Is load DEMO-101 still on track for delivery? | `/vektor:dispatch-exceptions` |
| What truck is assigned to manifest DEMO-M301? | `/vektor:manifest-fleet-context` |
| Which loads delivered this week still need a POD? | `/vektor:document-readiness` |
| What delivery exceptions should the next shift know about? | `/vektor:dispatch-exceptions` |

Replace the example IDs with references from your company. A typical answer includes the source records and what still needs checking. The workflows use read-only tools. Your Vektor permissions determine which records the assistant can see.

## Finance review preview

These workflows use existing Vektor MCP tools and are in preview. Choose the separate finance connection approved by your organization for the company you want to review. If your assistant only shows the standard Vektor connection, open Bill IQ or Settlements in Vektor. The examples use fictional references.

| Ask your assistant | Claude Code command | Company |
| --- | --- | --- |
| Why is driver settlement STL-301 still being recalculated? | `/vektor:truck-settlement-review` | Carrier or hybrid |
| Is carrier bill AP-401 approved and what does the broker still owe? | `/vektor:carrier-payable-review` | Broker or hybrid |
| Can you explain my own staff pay statement for the last pay period? | `/vektor:staff-settlement-review` | Carrier, broker or hybrid |
| What is blocking approval for the Office staff pay run? | `/vektor:staff-settlement-review` | Carrier, broker or hybrid with staff finance access |

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
