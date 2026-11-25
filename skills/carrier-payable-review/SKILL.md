---
name: carrier-payable-review
description: Read and explain a broker's carrier payable invoices in Vektor TMS Bill IQ. Use for a carrier bill, a bounded due-date queue, a linked manifest, a billed-versus-expected variance, or an invoice's approval and payment status. Payment-only requests and driver or staff settlements are outside this review.
license: Apache-2.0
---

# Carrier payable review

Find what a broker owes the carrier on a specific bill and explain any verified discrepancy.

1. **Confirm the broker connection.** Use the protected finance catalog. Call `finance_ReviewContext_Get` by itself and wait for the result before reading bills. Use a BROKER connection or a HYBRID connection with `BROKER_PAYABLE_REVIEW`. Require that capability for every company type. The carrier on the bill is the broker's payee. If a named broker differs, or several connections may match, ask the user to select the broker connection or verify the company reference. Continue on that same connection. If the protected tools or capability are unavailable, direct the user to Bill IQ in Vektor.
2. **Find the bill.** Use `finance_CarrierPayableInvoice_List` with one selector. Pass the exact bill `reference` and known `carrier`, a verified `manifestId` or exact `manifestReference`, or a bounded `dueFrom` and `dueTo` in company-local ISO dates. If the user gives only an order number with no verified bill or manifest association, ask for the bill or manifest reference. Compare the returned bill's own manifest link and carrier. A manifest can have more than one bill. If several records could match, ask for the carrier, manifest or invoice date. Follow only the same authorized query's `nextCursor`, and report partial coverage when a page is missing.
3. **Review one bill.** Pass its exact `invoiceId` to `finance_CarrierPayableInvoice_Retrieve`. Report approval, bill status and recorded payment state separately. Use the owning bill's verified `billed`, `expected`, and `remaining` amounts and currency. Read `varianceKnown` before using `variance`. True with a verified zero means no recorded variance. False means the comparison is unavailable. An absent flag leaves comparability unreported. If expected pay or currency is unavailable, say what needs checking in Bill IQ. Use applicable source totals only for complete same-currency coverage.
4. **Give the next check.** Lead with the bill and linked manifest, the kind of blocker supported by the record, and the next accounting check. A bill can be approved and partially paid. Report paid or outstanding as recorded and leave bank clearance unverified without separate approved evidence.

Use only the named protected reads. Keep remittance instructions, banking information, addresses, contact details, original invoice files, customer revenue, and margins out of the result. Stop before creating, aligning, changing, approving, exporting, or paying a carrier bill.
