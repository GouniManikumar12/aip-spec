# 11 · Complete Flow

This chapter maps the full AIP lifecycle from platform ingress to final settlement.

## Flow overview

```text
Platform -> PlatformRequest -> Operator -> ContextRequest -> Brand Agents
Brand Agents -> Bid -> Operator -> PlatformResponse -> Platform
Platform / Operator / Brand Agent -> Lifecycle Events -> LedgerRecord
```

## 1. Platform ingress

The Platform starts by sending `platform-request.json`.

That request carries:

- `request_id`
- platform identity and software metadata
- effective consent state
- exactly one classification input form
- either a live interaction payload or provided signals

In v1.0, raw query text and message history are used for operator-side classification only. They are not authorized for unrestricted downstream replay.

## 2. Operator normalization

The Operator evaluates policy, consent, and monetization eligibility, then derives `context-request.json`.

`ContextRequest` is the downstream-safe auction surface. It contains:

- `context_id`
- `source_request_id`
- operator and platform identity
- session and surface metadata
- normalized intent and decision phase
- operator-generated summary
- allowed render formats

It must not contain raw upstream queries or raw transcript replay.

## 3. Brand Agent bidding

Eligible Brand Agents respond with `bid.json`.

A bid may contain:

- targeting constraints
- pricing in micros
- budget controls
- recommendation content
- optional delegation capability

Supported billing models in v1.0 are:

- `CPX`
- `CPC`
- `CPE`
- `CPA`

## 4. Operator selection

The Operator applies operator-defined ranking and emits `auction-result.json`.

Key result semantics:

- `status = "filled"` means a winner exists
- `status = "no_match"` means the auction completed without a fill
- the result includes `serve_token` for event stitching
- delegation availability may be surfaced, but delegation has not started yet

## 5. Recommend flow

Recommend mode is used when the user remains in the Platform experience and the Brand Agent contributes recommendation content without taking over the session.

Typical lifecycle:

1. Platform receives `PlatformResponse`
2. Platform renders the commercial response
3. Platform emits `exposure_shown`
4. If the user engages, Platform emits `interaction_started`
5. If the user later completes the target action, Brand Agent or another verified downstream source emits `task_completed`

Canonical settlement path:

`CPX -> CPC -> CPA`

## 6. Delegate flow

Delegate mode is used when the Brand Agent can execute the task directly after explicit user consent.

Typical lifecycle:

1. Platform receives `PlatformResponse` with delegation availability
2. Platform asks the user to consent
3. Platform confirms consent to the Operator
4. Operator checks Brand Agent availability and initiates the delegated session
5. Operator records `delegation_started`
6. After session start, live task turns may flow directly between Platform and Brand Agent
7. Platform and Brand Agent emit `delegation_activity` while the session remains active
8. If the user completes the task, `task_completed` is emitted
9. If the session becomes inactive before completion, the Operator records `delegation_expired`

Canonical settlement path:

`CPX -> CPE -> CPA`

## 7. Operator role during delegation

The Operator remains:

- the authorization layer for session creation
- the enforcement point for the declared handoff scope
- the audit and settlement authority
- the verifier for `delegation_started`, `delegation_activity`, `delegation_expired`, and `task_completed`

The Operator does not need to inspect full delegated turn content by default in v1.0.

## 8. Scope and session data

Delegation scope is limited to what is declared for session initiation. In-session data collected after handoff is session-bound by default and must not be reused for training, profiling, or future outreach without separate consent.

## 9. Optional downstream commerce handoff

If the Brand Agent uses an external commerce protocol such as **Universal Commerce Protocol (UCP)** to execute checkout or order management, AIP still remains the attribution and settlement layer.

Recommended join keys:

- `serve_token`
- `session_id`
- `delegation_session_id` when delegation exists

The downstream commerce system proves transaction completion. AIP records the verified business outcome through `task_completed`.
