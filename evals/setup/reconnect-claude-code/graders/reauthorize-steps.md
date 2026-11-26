---
type: llm
weight: 2
---

PASS if the reply says the Vektor connection needs to be signed in again and tells the user to run /mcp in Claude Code, choose Vektor and authorize it in the browser, without asking for any password, token, code or callback URL. Saying not to add the server again is fine, and so is saying to sign in again to choose another company.
FAIL if the reply tells the user to add the Vektor server, including as a fallback, asks for credentials, or gives no way to sign in again.
Formatting, tone and length do not affect the verdict.
