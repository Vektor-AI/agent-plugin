---
description: The user asks whether a load is ready without saying what kind of readiness. Ask a focused question before any lookup.
expected_outcome: A clarifying question about which readiness is meant (paperwork, dispatch or billing) and no freight or document calls.
tags: [document-readiness, near-miss, clarify]
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

Is DEMO-405 ready?
