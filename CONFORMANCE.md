# AIP Conformance

This document defines what it means to conform to the current AIP specification surface in this repository.

## Scope

Conformance in this repo is schema-level and fixture-level.

An implementation is conformant when it can:

- produce payloads that validate against the canonical schemas in `schemas/`
- reject payloads that violate those schemas
- preserve the current lifecycle vocabulary and settlement semantics
- implement the authentication and replay rules in [03-transport-and-auth.md](docs/03-transport-and-auth.md)

This document does not certify business quality, auction performance, fraud quality, or uptime by itself.

## Canonical schema set

The current conformance surface is the schema list in [tests/conformance-manifest.json](tests/conformance-manifest.json):

- `platform-request.json`
- `context-request.json`
- `bid.json`
- `auction-result.json`
- `event-exposure-shown.json`
- `event-interaction-started.json`
- `event-delegation-started.json`
- `event-delegation-activity.json`
- `event-delegation-expired.json`
- `event-task-completed.json`
- `ledger-record.json`

## Lifecycle and settlement rules

Conformant implementations must preserve the v1.0 lifecycle vocabulary:

- `exposure_shown`
- `interaction_started`
- `delegation_started`
- `delegation_activity`
- `delegation_expired`
- `task_completed`

Conformant implementations must also preserve these normative semantics:

- only the highest-value verified event is billable per `serve_token`
- external click-out flows may settle as `CPX -> CPC -> CPA`
- delegated flows may settle as `CPX -> CPE -> CPA`
- `delegation_started`, `delegation_activity`, and `delegation_expired` are non-billable control events
- `session_timeout_seconds` in the winning bid is an inactivity timeout
- each verified `delegation_activity` resets that timeout
- `no_match` is the canonical empty auction outcome

Selection logic remains operator-defined and is not tested by this suite.

## Conformance suite

The conformance suite validates four things:

1. Every schema listed in `tests/conformance-manifest.json` is structurally valid.
2. Every file in `examples/` validates against its canonical schema.
3. Every file in `tests/valid/` validates against its canonical schema.
4. Every file in `tests/invalid/` fails validation against its canonical schema.

## Running the suite

From the repository root:

```bash
npm test
```

The test command runs:

```bash
python3 tools/run_conformance.py
```

The runner writes a machine-readable report to:

```text
tests/conformance-results.json
```

## Current suite shape

As of March 27, 2026, the repository suite contains:

- 11 schema checks
- 13 example payload checks
- 10 valid fixture checks
- 6 invalid fixture checks

## Required behavior for conformant implementations

An implementation claiming AIP conformance should be able to demonstrate all of the following:

- it accepts payloads shaped like the repository examples and valid fixtures
- it rejects malformed payloads shaped like the repository invalid fixtures
- it uses the current event vocabulary and identifier family
- it enforces the request-signing, timestamp, nonce, and replay rules from the transport/auth chapter
- it does not emit deprecated public outcomes such as `no_fill`, `no_bid`, `cpx_exposure`, `cpc_click`, or `cpa_conversion`

## What conformance does not prove

Passing this suite does not by itself prove:

- production security maturity
- auction quality
- fraud detection quality
- payout correctness
- latency SLOs
- interoperability with undocumented private extensions

Those require implementation review and bilateral integration testing in addition to schema conformance.

## Publishing results

When sharing conformance results externally, publish at minimum:

- the commit or version tested
- the exact `tests/conformance-manifest.json` used
- the pass/fail counts by category
- any skipped checks
- the generated `tests/conformance-results.json` artifact
