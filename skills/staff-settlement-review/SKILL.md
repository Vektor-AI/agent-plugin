---
name: staff-settlement-review
description: Review staff or agent settlements in a carrier or broker company's Vektor TMS account. Use for my own staff pay statement, a finance user's review of one staff statement, or a staff-cycle pay run's approval, blockers, payroll and payout routes. Driver and vendor freight settlements have separate workflows.
license: Apache-2.0
---

# Staff settlement review

Determine whether the user wants their own statement, one staff statement they review in finance, or the summary of a staff pay run.

1. **Confirm the connection.** Use the protected finance catalog. Call `finance_ReviewContext_Get` by itself and wait for the result. Use the authorized CARRIER, BROKER or HYBRID company for staff pay. When the requested company differs or names collide, ask the user to select the connection or verify the company reference. Make no staff lookup until the company matches. Continue on the same connection and use the capability for the requested path.
2. **For the user's own statement.** With `SELF_STAFF_PAY_REVIEW`, call `finance_StaffStatement_List` for the requested company-local ISO `periodStart` and `periodEnd`. This read is tied to the signed-in person. Use the same query's `nextCursor` when needed, and never include a person's ID or try a finance lookup as a fallback. If the user has no linked payee, explain the link issue and direct them to their Vektor payroll contact. If the amount is absent or the calculation is pending, say so.
3. **For a finance user's review of one staff statement.** With `STAFF_PAY_STATEMENT_REVIEW`, pass the exact statement `reference` to `finance_StaffPayStatement_Retrieve`, with `periodStart` and `periodEnd` if necessary. Use a returned `statementKey` only to resolve explicitly selected matches from the same connection, when the tool schema supports that selector. Ask for a period or verified reference on an unresolved match. Report its classification, period, status and approved earnings or deductions needed to explain the statement.
4. **For a staff pay run.** With `STAFF_PAY_RUN_REVIEW`, use `finance_StaffPayRun_Get` with the exact period dates and `cycleName` when known. Preserve the full cycle name as given, including words that can also describe the workflow, such as “staff” or “weekly.” Resolve relative dates in the verified company timezone. When two cycles could match, request the exact one and use an authorized cycle/period key returned by the same connection if available. Summarize OPEN, LOCKED or APPROVED, the relevant blocker counts, pay date if present, and verified totals by currency and route. Use this summary without browsing employee records.
5. **State what happened.** Distinguish employee gross for payroll, contractor net, and held pay. Approval confirms workflow state. A payroll export or planned payout route does not prove money moved. Use the actual classification and recorded evidence. For an unconfigured finance role or missing staff-run tools, direct finance users to Settings → Settlements → Staff cycles → Periods → Pay Run. For own-pay access, direct the person to their payroll contact.

Use only the protected staff reads. Stop before creating a PDF, exporting payroll, changing approval, posting or recording payment, recalculating, or initiating a payout.
