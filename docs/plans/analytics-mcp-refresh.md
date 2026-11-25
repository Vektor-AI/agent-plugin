---
task: analytics-mcp-refresh
tier: task
status: in-progress
owner: Vadim
executor: Codex
approval: "Vadim, 2026-11-25, approved the analytics skill, a refresh pilot after measuring the window, and a PGO review in the task thread"
created: 2026-11-25
updated: 2026-11-25
---

# Answer Vektor Analytics questions and shorten warehouse refresh intervals

## Outcome

Customers already run ClickHouse queries through the Vektor OAuth gateway. Give them a repeatable workflow for interpreting those results and a second refresh after measuring production headroom.

Acceptance criteria:

- AC1 [open]: The plugin guides an authorized company through a bounded warehouse analysis and handles incomplete data and identity failures. Proof: package checks, Claude plugin validation, synthetic assistant evaluations.
- AC2 [open]: A measured quiet window supports adding a second refresh to the existing CronJob. Proof: Cloud Monitoring and gateway audit baseline, production Helm render and scheduled-run verification after merge.
- AC3 [proven 2026-11-25: https://github.com/Vektor-AI/spanner-clickhouse-ingestor/actions/runs/44239306461]: The ingestor build and collection path are traced to deployed source, with observed resource demand and an evidence-based PGO recommendation. Proof: profile repository inventory, release build logs, pinned entrypoint and Cloud Monitoring.

Non-goals: new connector or tool APIs, changing tenant access, automated publishing to host directories, production profiling or deployment from this task.

## Context and design

**Decided:** Use the existing Vektor OAuth connection and its Analytics Database schema, validation and execution tools. Disable exports and bound the business scope and returned rows. The skill verifies tenant scope before data retrieval and reports the distinction among no matching rows, unavailable warehouse and unverified freshness. This uses the existing tenant authorization and read-only SQL guard. The in-app preview flow can persist analysis artifacts.

**Decided:** Measure the 11:00 UTC hour before changing the production GitOps schedule. The recurring ClickHouse burst at the top of the hour supports starting at 11:05 UTC. Move the overnight run to 02:05 UTC so the two slots share the same minute and one CronJob. The current full per-company load, retries and timeouts continue to govern both slots. One resource lets Kubernetes enforce Forbid across both slots. Roll back by removing the second slot if observed warehouse load, application read latency, or refresh health worsens compared with baseline.

Production Spanner gateway audit, indexed by tool and UTC timestamp from October 28 through November 24 UTC, confirmed that customers use the hosted Database tools. Warehouse-not-provisioned was the main schema error. Analytics Spanner saved-run records and PostHog browser SQL events cover separate parts of the workflow. Production load measurements are recorded with the environment change.

Sources: agent-plugin base 0330b32, production analytics-service v0.6.1, mcp-service v0.10.0, spanner-clickhouse-ingestor v0.5.0 and go-pgo-profiles 201754e. Use Go handbook 0c0556b with the plugin's CONTRIBUTING and the environment repo's render checks. The Go PGO guide requires representative CPU workload profiles. Compare the currently deployed batch with available fleet profiling before proposing a profile. The Kubernetes CronJob spec scopes concurrency to jobs from the same resource.

## Reviews

Review 1 (requirements and evidence, 2026-11-25, Codex): The gateway audit proves the tools exist, including real ad hoc SQL that saved-query records do not cover. An identity mismatch must stop data retrieval. Require evidence before reporting warehouse freshness.

Review 2 (revised design and proof, 2026-11-25, Codex): Same-agent design review. The preview tool can write saved artifacts and the Database RPC has optional exports. Bind the workflow to the OAuth Database path with export off and synthetic checks for absent warehouse, partial rows and tenant collision. Forbid needs both times in one resource. Profile inspection must distinguish missing PGO from actual resource pressure.

Plan gate (P1–P9): plan-ready on 2026-11-25. The seven-day Cloud Monitoring baseline showed a recurring ClickHouse spike at 11:00–11:04 UTC. The 11:05 UTC slot avoids that burst. Both slots use minute 05 to keep one CronJob. Production usage, exact gateways and validation are defined above. Go L1–L5 have no service-code boundary in this plugin and Helm change.

## Milestones

| ID | Milestone | Rows | Criteria | Target |
| --- | --- | --- | --- | --- |
| M1 | Tool-guided analysis | PR 1 | AC1 | none |
| M2 | Second daily warehouse refresh | PR 2 | AC2 | none |

## Items

| ID | Outcome | Repo | Proof | State |
| --- | --- | --- | --- | --- |
| 1.1 | Discoverable Analytics skill and success and failure cases | agent-plugin | make check, Claude plugin strict validation, assistant tool trace | in progress |
| 2.1 | An 11:05 UTC refresh pilot with measured baseline | platform-envs | production metrics, before/after Helm render, Environment PR validation | in progress |
| 3.1 | Ingestor PGO and resource review | spanner-clickhouse-ingestor | deployed build logs, profile source, CPU and memory baseline | done (read-only review of v0.5.0) |

## PR plan

| PR | Repo | Items | Proof | Waits on | Size | State |
| --- | --- | --- | --- | --- | --- | --- |
| PR 1 | agent-plugin | 1.1 | package and assistant behavior proof | none | S | draft <https://github.com/Vektor-AI/agent-plugin/pull/5> |
| PR 2 | platform-envs | 2.1, 3.1 | measured baseline, profile review and rendered production config | none | S | draft <https://github.com/Vektor-AI/platform-envs/pull/2649> |

## Decisions

| ID | Decision | Recommendation | Meanwhile | Status |
| --- | --- | --- | --- | --- |
| D1 | Add Analytics guidance and measure before scheduling a second job | Extend the existing skill package and GitOps CronJob | Run read-only measurements and profile inspection | taken 2026-11-25 (Vadim, approved in task thread) |

## As built

Pending verification and merge.
