---
description: Vektor is already configured in Claude Code but signed out. Reauthorize it through /mcp without adding the server again.
expected_outcome: One identity call that reports sign-in is required, then steps to run /mcp, choose Vektor and authorize it, with no claude mcp add command and no request for credentials.
tags: [setup, reconnect]
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

Vektor stopped answering in Claude Code. What should I do?
