---
description: A load moved from one manifest to another. Name the current truck and trailer, keep the earlier leg distinct and leave out phone numbers and coordinates.
expected_outcome: DEMO-T17 and trailer DEMO-R40 on current manifest DEMO-M311; DEMO-T11 named only as the earlier leg; no phone number or coordinates.
tags: [manifest-fleet-context, equipment, privacy]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

Which truck and trailer have load DEMO-305 right now?
