# 04 · Auction

Each AIP auction starts from a `PlatformRequest`, is normalized into a `ContextRequest`, collects `Bid` responses from eligible Brand Agents, and ends with a `PlatformResponse`.

## Core rule

Selection logic is **operator-defined**.

Pricing vectors influence operator scoring, but settlement ladders are not themselves a normative ranking algorithm. In particular:

- External click-out flows may settle as `CPX -> CPC -> CPA`
- Delegated flows may settle as `CPX -> CPE -> CPA`

Those are billing semantics, not a mandated sort order.

## Auction window

AIP uses a short, time-bounded asynchronous auction window.

1. The Platform sends `platform-request.json` to the Operator.
2. The Operator evaluates eligibility, policy, and intent.
3. The Operator derives `context-request.json` and fans it out only to eligible Brand Agents.
4. Brand Agents return `bid.json` payloads before the response window closes.
5. The Operator applies operator-defined ranking and returns `auction-result.json`.

If no eligible response arrives before the window closes, the Operator returns a valid `PlatformResponse` with `status = "no_match"`.

## Request surfaces

| Stage | Schema | Direction | Purpose |
| --- | --- | --- | --- |
| Ingress | `platform-request.json` | Platform -> Operator | Raw interaction or provided-signal input, consent state, and monetization hints |
| Fanout | `context-request.json` | Operator -> Brand Agents | Intent-safe, operator-derived auction context |
| Response | `bid.json` | Brand Agent -> Operator | Pricing, targeting, recommendation payload, and optional delegation capability |
| Result | `auction-result.json` | Operator -> Platform | Winner, render payload, delegation availability, and `serve_token` |

## No-match behavior

`no_match` means the auction completed without a fill. It is not an error, and no billable lifecycle begins.

## Delegation in auction results

When the selected Brand Agent supports delegated execution, the `PlatformResponse` may surface a `delegation` object. That object indicates availability and activation semantics, but delegation does not begin until:

1. the user explicitly consents, and
2. the Operator confirms session creation and records `delegation_started`.
