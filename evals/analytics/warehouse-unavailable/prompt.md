---
description: The Analytics warehouse is not provisioned. Stop after the first schema error, run no query and invent no count.
expected_outcome: One schema call, no validate or execute call, and a reply that Analytics is not available for this company without a number.
tags: [analytics, errors]
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

How many orders did we deliver last full week?
