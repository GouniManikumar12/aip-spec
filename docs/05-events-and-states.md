# 05 · Events & States

Every measurable action in AIP is recorded as an event. Events are how the protocol proves participation, interaction, delegation, and outcome for fair settlement.

## Lifecycle events

| Event | `event_type` | Trigger | Settlement | Typical reporter |
| --- | --- | --- | --- | --- |
| Exposure shown | `exposure_shown` | Commercial response is surfaced | `CPX` | Platform |
| Interaction started | `interaction_started` | User engages with the response | `CPC` or `CPE` | Platform |
| Delegation started | `delegation_started` | User consented and delegated session was initiated | Non-billable | Operator |
| Delegation activity | `delegation_activity` | Platform or Brand Agent proves the session is active | Non-billable | Platform or Brand Agent |
| Delegation expired | `delegation_expired` | Operator marks session inactive before outcome | Non-billable | Operator |
| Task completed | `task_completed` | User finishes signup, purchase, or another billable task | `CPA` | Brand Agent or Operator-verified downstream source |

Only the highest-value verified event is billable per `serve_token`.

## Settlement semantics

AIP separates event verification from ranking:

- Operators define ranking and auction logic.
- Event ladders define what may settle after a result is shown.

Canonical billing paths:

- External click-out: `CPX -> CPC -> CPA`
- Delegated session: `CPX -> CPE -> CPA`

## Recommend mode

```text
PlatformResponse -> exposure_shown -> interaction_started -> task_completed
```

If no higher event occurs, settlement remains at the highest verified lower event.

## Delegate mode

```text
PlatformResponse -> exposure_shown -> delegation_started
                                     -> delegation_activity (0..n)
                                     -> delegation_expired | task_completed
```

`delegation_started` proves session initiation only. It does not mean the Operator transports or inspects every later delegated turn.

## Inactivity and liveness

Delegated sessions are governed by inactivity timeout:

- `session_timeout_seconds` is an inactivity timer declared in the winning bid
- each verified `delegation_activity` resets that timer
- both Platform and Brand Agent may emit `delegation_activity`
- if the timer elapses before `task_completed`, the Operator records `delegation_expired`

## Ledger states

Ledger records summarize the lifecycle at settlement time:

| State | Meaning |
| --- | --- |
| `PENDING` | Auction completed and a result exists |
| `EXPOSED` | Exposure was verified |
| `CLICKED` | Interaction was verified in a click-out flow |
| `CONVERTED` | Final task outcome was verified |
| `FINALIZED` | Final settlement completed |
| `REFUNDED` | Finalized settlement was later adjusted or refunded |

The ledger record stores timestamps for exposure, interaction, delegation start, delegation liveness, expiry, and final outcome so the Operator can reconcile the lifecycle without double-billing.

## Verification principles

Every event must include:

- `event_type`
- `serve_token`
- `ts`

Event-specific fields then provide the actor identity, settlement metadata, or delegation session metadata required for verification.

Operators are responsible for deduplication, event ordering, trust checks, and final settlement. AIP standardizes the event vocabulary and lifecycle semantics, not a single universal verification implementation.
