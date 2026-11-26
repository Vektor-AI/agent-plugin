---
description: A writing request that needs no Vektor data. No Vektor skill fires and no freight lookup runs.
expected_outcome: A short thank-you note with no Skill call and no Vektor lookup.
tags: [near-miss, near-miss]
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

Draft a short thank-you note to a carrier partner for their on-time deliveries this week.
