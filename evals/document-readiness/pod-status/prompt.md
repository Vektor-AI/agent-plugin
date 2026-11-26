---
description: One load has an attached POD and the other only a requested POD row. Classify from metadata without opening files.
expected_outcome: DEMO-402 POD recorded, DEMO-403 POD missing (requested, nothing attached), no signed URL or file name in the reply.
tags: [document-readiness, paperwork]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

Do loads DEMO-402 and DEMO-403 have their POD recorded?
