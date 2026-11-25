---
name: document-readiness
description: Check Vektor TMS freight paperwork status for a load or bounded set of loads. Use for missing or recorded POD, proof of delivery, BOL, bill of lading, or rate confirmation. This workflow checks document metadata and stops before opening files, extracting documents, or creating orders.
license: Apache-2.0
---

# Document readiness

Identify whether requested paperwork is recorded, missing, or still unknown.

1. **Resolve the loads and document types.** Use the authorized Vektor company and match the exact load ID or a disambiguated reference. For a queue such as delivered loads this week, use the requested status, time range and timezone. If the user asks whether a load is ready without specifying paperwork, use a documented requirement visible for that load or ask which document types to check.
2. **Read metadata only.** Select an available Vektor read tool for document presence, type and status. Check that its declared operation can return metadata without retrieving the file. Use the current tool schema and load association. Follow available pagination for the requested scope. Leave file contents, attachment links, signed URLs and extracted personal details out of the workflow.
3. **Classify each required type.** `Recorded` requires evidence that the requested paperwork is attached or recorded against the correct load. A row created to request a document does not establish that the paperwork arrived. `Missing` requires an explicit missing or unattached state, or a complete authorized check with no matching recorded item. Use `Unknown` for a row whose attachment status is unavailable, an incomplete lookup, denied access, or unresolved identity. Recorded paperwork can still require review or a signature before billing.
4. **Report the next task.** For a single load, show the type and status with the source record reference or timestamp when available. For a group, show the checked range, loads with missing items, and any gaps in coverage. Identify the next check for unknown items. Stop at the status report.

Keep uploads, file retrieval, sharing, and order changes in separate authorized workflows. If the connector is unavailable or only exposes file retrieval, explain the missing metadata access and stop.
