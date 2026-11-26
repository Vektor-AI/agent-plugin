# Vektor TMS for your assistant

Check whether a delivery is on track, find the equipment assigned to a manifest, see which delivered loads still need paperwork, and ask for totals such as weekly deliveries. The Vektor plugin gives your assistant workflows for each task. It uses the connection and company access you authorize in Vektor TMS.

## Get started

You’ll need a Vektor TMS account with access to the company you want to work in. Add the plugin for the workflows and the Vektor connection for your records.

### Claude on the web or desktop

1. Open [Customize > Plugins](https://claude.ai/customize/plugins), select **Add > Add marketplace** and enter `Vektor-AI/agent-plugin`. Then add the **Vektor TMS** plugin, and turn on **Sync automatically** for the marketplace so new versions arrive on their own.
2. Open [Customize > Connectors](https://claude.ai/customize/connectors), select **Add > Add custom connector**, name it Vektor and enter `https://mcp.vektortms.com/mcp`. On a Team or Enterprise plan, an Owner adds the connector in **Organization settings > Connectors**.
3. Connect Vektor, sign in and choose your company.

Plugins you add here also load in Claude Code when you start a session signed in to the same account, and they update automatically there too.

### Claude Code

1. In Claude Code 2.1.275 or newer, follow the [Vektor connection guide](https://mcp.vektortms.com/) from the directory where you use Claude Code. If Vektor already appears in `/mcp`, you can reuse that connection.

2. Run this in Claude Code:

   ```text
   /plugin install vektor --marketplace Vektor-AI/agent-plugin
   ```

3. Confirm the marketplace source and choose where to install the plugin. Run `/reload-plugins` if prompted, then check `/mcp`. Sign in and choose your company.

4. Turn on updates: run `/plugin`, open **Marketplaces**, select `vektor-plugins` and enable auto-update. Claude Code then installs each new version within a few minutes of starting a session; run `/reload-plugins` when it reports an update.

To set this up for a team, add the marketplace with auto-update and the plugin to the project's `.claude/settings.json`, or to managed settings for the whole organization:

```json
{
  "extraKnownMarketplaces": {
    "vektor-plugins": {
      "source": { "source": "github", "repo": "Vektor-AI/agent-plugin" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": { "vektor@vektor-plugins": true }
}
```

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

4. To update, run `codex plugin marketplace upgrade vektor-plugins` and open a new session.

### Other assistants

Use `https://mcp.vektortms.com/mcp` in assistants that support remote MCP and OAuth. This source preview’s install instructions cover Claude, Claude Code and Codex CLI. Host directories have their own publishing and installation steps.

## Data and permissions

- The plugin contains instructions only. It runs no code on your computer and collects no data.
- The workflows use read-only Vektor tools and stop before changing a record, sending a message or opening a file.
- You approve the connection inside one company. Your Vektor permissions decide which records the assistant can see.
- Records the assistant reads become part of your conversation with that assistant.
- Revoke access at any time from MCP settings in Vektor.

## Try a task

Ask in your own words. To pick a skill yourself, run a Claude Code command below or type `@` in Codex and search for its name.

| Ask your assistant | Claude Code command |
| --- | --- |
| How many orders did we deliver last full week? | `/vektor:analytics` |
| Is load DEMO-101 still on track for delivery? | `/vektor:dispatch-exceptions` |
| What truck is assigned to manifest DEMO-M301? | `/vektor:manifest-fleet-context` |
| Which loads delivered this week still need a POD? | `/vektor:document-readiness` |
| What delivery exceptions should the next shift know about? | `/vektor:dispatch-exceptions` |
| Which Vektor company are you connected to? | `/vektor:setup` |

Replace the example IDs with references from your company. A typical answer includes the source records and what still needs checking. The workflows use read-only tools. Your Vektor permissions determine which records the assistant can see.

## Troubleshoot

- **Vektor is missing or signed out.** Check **Customize > Connectors** in Claude or `/mcp` in Claude Code and Codex CLI. Use the exact URL `https://mcp.vektortms.com/mcp` when connecting. You can also ask the assistant to check the Vektor connection.
- **The assistant asks about a company.** Check which company you selected at sign-in. Use the [connection guide](https://mcp.vektortms.com/) to authorize another company.
- **The assistant can’t find a load or document.** Check the reference, date range, and your permissions in Vektor.
- **You used an earlier preview.** Install `vektor` and replace any saved `/vektor-tms:…` commands with `/vektor:…`. You can reuse your Vektor connection.
- **A workflow from the [changelog](CHANGELOG.md) is missing.** In Claude, select **Check for updates** for the marketplace in **Customize > Plugins**. In Claude Code, run `claude plugin marketplace update vektor-plugins`, then `claude plugin update vektor@vektor-plugins`. In Codex CLI, run `codex plugin marketplace upgrade vektor-plugins`. Start a new session after updating.

## Share feedback

If a task took too many steps, a tool was missing, or an answer was hard to use, try this prompt:

> Draft feedback about this Vektor task. Include what I tried, what I expected, and what happened. Use synthetic examples and leave out customer, load, and account details. Show me the draft.

Review the draft and send it through [Vektor support](https://vektortms.com/contact). For a reproducible plugin issue with synthetic data, you can also use [GitHub Issues](https://github.com/Vektor-AI/agent-plugin/issues).

## Contribute

The skills are open source under [Apache-2.0](LICENSE). To improve a workflow, start with the [contribution guide](CONTRIBUTING.md). Report security findings through the [private reporting instructions](SECURITY.md).

Access to hosted Vektor TMS services is governed by the [Vektor TMS Terms](https://vektortms.com/terms).
