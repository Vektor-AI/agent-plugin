---
type: llm
weight: 2
---

PASS if the reply tells the user to open Customize, then Connectors, in Claude desktop, and, when Vektor is listed there, to connect it and sign in instead of adding it again. Mentioning the Add custom connector steps only for the case where Vektor is not listed is fine.
FAIL if the reply's only fix is to add a new custom connector, asks for a password, token, code or callback URL, or says it checked the desktop app's connection from this session.
Formatting, tone and length do not affect the verdict.
