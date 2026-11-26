---
description: Asked from another session about Claude desktop, where Vektor was set up but its tools are gone. Give the Customize > Connectors sign-in path for an existing connector before any steps that add one, without checking this session's connection.
expected_outcome: No identity call; open Customize > Connectors and, if Vektor is listed, connect and sign in rather than adding it again; add it only if it is not listed.
tags: [setup, reconnect]
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

I set up the Vektor connector in the Claude desktop app last week, but today Claude there says it has no Vektor tools. How do I get them back?
