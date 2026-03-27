# 02 · AIP Roles

AIP centers on three canonical implementation roles and one optional supporting role:

- **AI Platforms** detect user intent, collect consent, and initiate `platform-request` messages.
- **Operators** govern participation, derive `context-request` payloads, run selection, authorize delegation, verify lifecycle events, and settle outcomes.
- **Brand Agents** evaluate operator-generated context, submit bids, contribute recommendation content, and optionally execute delegated tasks.
- **Auditors** are optional third parties that review settlement records, event trails, or compliance evidence.

These roles are the canonical personas for interoperability. Individual deployments may contain additional internal systems, but they should map back to these roles when describing protocol behavior.
