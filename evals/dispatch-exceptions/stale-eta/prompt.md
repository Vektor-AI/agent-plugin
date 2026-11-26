---
description: The only ETA was computed hours ago and falls after the appointment window. Lead with unconfirmed risk, label the ETA as last known with its computed time and recommend a fresh ETA.
expected_outcome: "Opens with 'Current delivery risk is unconfirmed.', labels 4:20 PM Central as the last known ETA computed at 9:05 AM Central, compares it with the 2:00 PM appointment and recommends a fresh ETA."
tags: [dispatch-exceptions, eta]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Skill]
disallowed_tools: [AskUserQuestion, Agent]
---

It is 1:30 PM Central (UTC-6) on 2026-11-26. Will load DEMO-118 make its delivery appointment today?
