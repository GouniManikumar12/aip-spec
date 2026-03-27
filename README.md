# Agentic Intent Protocol (AIP) Specification

**Version:** 0.1.0  
**Status:** Public Specification  
**Last Updated:** 2026-03-27

## Overview

The **Agentic Intent Protocol (AIP)** is an open protocol for AI advertising, commercial delegation, and outcome-based settlement inside AI platforms. It standardizes how Platforms, Operators, and Brand Agents exchange intent-safe auction context, run selection, verify lifecycle events, and settle the highest-value outcome per `serve_token`.

This repository contains:

- JSON Schemas for the public wire surface
- Narrative specification chapters
- Reference examples
- Conformance fixtures

Primary docs: [https://aip.mintlify.app](https://aip.mintlify.app)

## What v1.0 standardizes

- **Platform ingress** through `platform-request.json`
- **Operator fanout** through `context-request.json`
- **Brand Agent bids** through `bid.json`
- **Platform responses** through `auction-result.json`
- **Lifecycle events** across exposure, interaction, delegation, and outcome
- **Final settlement records** through `ledger-record.json`

Canonical public identifiers in v1.0:

- `request_id`
- `context_id`
- `bid_id`
- `response_id`
- `auction_id`
- `serve_token`

Canonical decision phases in v1.0:

- `awareness`
- `research`
- `consideration`
- `decision`
- `action`
- `post_purchase`
- `support`

## Billing and lifecycle model

AIP separates **selection logic** from **settlement semantics**.

- Operators define ranking and selection.
- Settlement paths describe what may be billed after a winner is chosen.

Canonical settlement paths:

- External click-out flow: `CPX -> CPC -> CPA`
- Delegated session flow: `CPX -> CPE -> CPA`

Only the highest-value verified event is billable per `serve_token`.

### Event types

| Event | `event_type` | Settlement |
| --- | --- | --- |
| Exposure shown | `exposure_shown` | `CPX` |
| Interaction started | `interaction_started` | `CPC` or `CPE` |
| Delegation started | `delegation_started` | Non-billable |
| Delegation activity | `delegation_activity` | Non-billable |
| Delegation expired | `delegation_expired` | Non-billable |
| Task completed | `task_completed` | `CPA` |

### Delegated sessions

Delegation in v1.0 uses a hybrid model:

- The Operator mediates session authorization and startup.
- After `delegation_started`, live task turns may flow directly between Platform and Brand Agent.
- The Operator remains the governance, scoping, audit, and settlement layer.
- `session_timeout_seconds` is an **inactivity timeout**.
- Platform and Brand Agent both emit `delegation_activity`.
- The Operator records `delegation_expired` when the inactivity timer elapses.

## Repository structure

```text
aip-spec/
├── schemas/
│   ├── platform-request.json
│   ├── context-request.json
│   ├── bid.json
│   ├── auction-result.json
│   ├── event-exposure-shown.json
│   ├── event-interaction-started.json
│   ├── event-delegation-started.json
│   ├── event-delegation-activity.json
│   ├── event-delegation-expired.json
│   ├── event-task-completed.json
│   ├── ledger-record.json
│   └── common.json
├── examples/
├── docs/
├── tests/
└── governance and policy files
```

## Quick start

Inspect the core schemas:

```bash
cat schemas/platform-request.json
cat schemas/context-request.json
cat schemas/bid.json
cat schemas/auction-result.json
```

Inspect the lifecycle schemas:

```bash
cat schemas/event-exposure-shown.json
cat schemas/event-interaction-started.json
cat schemas/event-delegation-started.json
cat schemas/event-delegation-activity.json
cat schemas/event-delegation-expired.json
cat schemas/event-task-completed.json
```

Review the examples:

```bash
cat examples/platform-request.example.json
cat examples/context-request.example.json
cat examples/bid.example.json
cat examples/auction-result.example.json
cat examples/event-task-completed.example.json
```

## Relationship to external commerce protocols

AIP covers intent, selection, delegation, attribution, and settlement. Downstream commerce execution may hand off to an external protocol such as **Universal Commerce Protocol (UCP)**, but that handoff is outside the core AIP wire model. In those flows, AIP remains the attribution and settlement layer, while the downstream commerce protocol provides transaction proof.
