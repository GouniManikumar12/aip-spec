# 07 · Security & Fraud

This chapter defines the minimum security and fraud controls required to operate AIP responsibly.

## 1. Security objectives

AIP security controls are designed to protect:

- request authenticity
- message integrity
- replay resistance
- settlement correctness
- delegated-session governance

## 2. Baseline controls

Implementations MUST:

- sign requests using the rules in [03-transport-and-auth.md](03-transport-and-auth.md)
- use TLS 1.3 or better
- rotate and revoke shared secrets
- validate payloads against the current schemas
- log authentication failures and replay attempts

## 3. Event-integrity controls

Operators MUST treat lifecycle events as settlement-relevant evidence.

At minimum, Operators SHOULD verify:

- `exposure_shown` came from an authorized Platform source
- `interaction_started` is consistent with the selected flow and allowed settlement unit
- `delegation_started` reflects explicit user consent and confirmed session initiation
- `delegation_activity` is attributable to either the Platform or the Brand Agent and references a known delegated session
- `delegation_expired` is generated only by the Operator or an Operator-controlled system
- `task_completed` is backed by a trusted downstream outcome source

## 4. Fraud detection by event type

### Exposure fraud

Operators SHOULD detect:

- impossible exposure rates
- repeated exposures without matching session context
- low-visibility or synthetic display events
- bursty exposure patterns from a single source

Primary signal: `exposure_shown`

### Interaction fraud

Operators SHOULD detect:

- anomalous click or engagement spikes
- interaction events that arrive without a plausible prior exposure
- implausible interaction timing
- repeated automated interaction patterns

Primary signal: `interaction_started`

### Delegation abuse

Operators SHOULD detect:

- delegated sessions started without matching consent
- fake liveness heartbeats
- activity streams that continue after expiry
- excessive delegated-session creation with no downstream outcomes

Primary signals:

- `delegation_started`
- `delegation_activity`
- `delegation_expired`

### Outcome fraud

Operators SHOULD detect:

- `task_completed` events without a valid upstream lifecycle
- duplicate outcomes for the same `serve_token`
- suspicious outcome velocity or value inflation
- unverifiable downstream order or signup references

Primary signal: `task_completed`

## 5. Settlement protection

To prevent double billing or lifecycle corruption, Operators MUST enforce:

- one final billable settlement per `serve_token`
- monotonic lifecycle reconciliation
- deduplication of repeated event submissions
- explicit handling of invalid, late, or contradictory events

Recommended reconciliation checks:

- ignore lower-value billable events after a higher-value billable outcome is finalized
- reject delegated-session activity for unknown or expired `delegation_session_id`
- flag task outcomes that arrive after the Operator has finalized a conflicting settlement state

## 6. Quarantine and invalid traffic handling

Operators SHOULD support a quarantine process for suspicious traffic.

When suspicious traffic is detected, the Operator SHOULD be able to:

- mark the lifecycle as under review
- withhold settlement temporarily
- downgrade trust for the reporting source
- revoke or rotate compromised credentials
- produce an audit trail for dispute resolution

## 7. Logging and auditability

At minimum, Operators SHOULD retain an audit trail linking:

- `serve_token`
- `auction_id`
- `response_id`
- `session_id`
- `delegation_session_id` when present
- event timestamps
- auth verification results

The audit trail should be sufficient to explain why a lifecycle was accepted, rejected, expired, or settled.

## 8. Incident response

If a key is compromised or a source is actively abusive, Operators MUST be able to:

- revoke the affected `keyId`
- reject future requests signed with that key
- quarantine recent traffic associated with the compromised issuer
- investigate impacted `serve_token` lifecycles

## 9. Recommended controls beyond the minimum

Recommended, but not strictly required by the schema suite:

- per-key and per-IP rate limiting
- anomaly scoring
- source trust tiers
- IP allowlisting for high-trust integrations
- mTLS for bilateral private integrations
- settlement review workflows for high-value `task_completed` events
