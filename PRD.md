# Agentic Intent Protocol (AIP) v0.1 - Product Requirements Document

**Product Name:** Agentic Intent Protocol (AIP)  
**Owner:** AdMesh Network — Reference Operator and Protocol Maintainer  
**Version:** v0.1 (Foundational Implementation)  
**Status:** Public Specification  
**Last Updated:** 2025-11-11

---

## Table of Contents

1. [Purpose & Vision](#1-purpose--vision)
2. [Core Problem Statement](#2-core-problem-statement)
3. [Roles & Actors](#3-roles--actors)
4. [Value Flow Overview](#4-value-flow-overview)
5. [Billing Units](#5-billing-units)
6. [Event Windows](#6-event-windows)
7. [Auction Logic](#7-auction-logic)
8. [Event State Machine](#8-event-state-machine)
9. [Wallet & Payout Logic](#9-wallet--payout-logic)
10. [Interoperability & Open Standard](#10-interoperability--open-standard)
11. [Security & Trust](#11-security--trust)
12. [Observability & SLOs](#12-observability--slos)
13. [Privacy & Retention](#13-privacy--retention)
14. [Versioning & Governance](#14-versioning--governance)
15. [SDK Deliverables](#15-sdk-deliverables)
16. [Economics & Defaults](#16-economics--defaults)
17. [Acceptance Tests](#17-acceptance-tests)
18. [Governance Summary](#18-governance-summary)

**Appendices:**
- [Appendix A: Glossary](#appendix-a-glossary)
- [Appendix B: API Reference](#appendix-b-api-reference)
- [Appendix C: State Transition Table](#appendix-c-state-transition-table)
- [Appendix D: Trust Score Calculation](#appendix-d-trust-score-calculation)
- [Appendix E: Contact Information](#appendix-e-contact-information)

---

## 1. Purpose & Vision

### 1.1 What is AIP?

The **Agentic Intent Protocol (AIP)** is a universal, open-source protocol for **agentic and conversational advertising**. It defines:

- **Standard interfaces** for context requests, auctions, event tracking, and settlement
- **Billing semantics** (CPX, CPC, CPA) with time-windowed attribution
- **Trust and security** mechanisms to prevent fraud
- **Interoperability** so any ad network can implement AIP and join the ecosystem

### 1.2 Vision

**"Enable transparent, performance-based advertising in the agent economy."**

As AI agents and conversational interfaces become primary user touchpoints, traditional display advertising breaks down. AIP provides:

- **For Platforms:** A standardized way to monetize high-intent moments without building ad infrastructure
- **For Advertisers:** Direct access to users expressing purchase intent in natural language
- **For Networks:** A common protocol to operate transparent, auditable marketplaces

### 1.3 Design Principles

1. **Open & Interoperable:** Network-agnostic protocol, not a proprietary platform
2. **Performance-Based:** Advertisers pay only for verified events (exposure, click, conversion)
3. **Privacy-First:** No PII storage, contextual signals only
4. **Transparent:** Immutable event logs, auditable ledger, clear revenue splits
5. **Developer-Friendly:** Simple SDKs, clear documentation, fast integration

---

## 2. Core Problem Statement

### 2.1 The Shift to Conversational Interfaces

Users increasingly interact with AI through:
- **Chatbots** (ChatGPT, Claude, Gemini)
- **Voice assistants** (Alexa, Siri, Google Assistant)
- **AI agents** (autonomous shopping, research, booking)

Traditional advertising (banners, search ads) doesn't fit these interfaces.

### 2.2 Challenges

**For Platforms:**
- No standard way to monetize conversational interactions
- Building ad infrastructure is complex and expensive
- Risk of degrading user experience with intrusive ads

**For Advertisers:**
- Can't reach users in AI conversations
- No performance-based pricing for conversational ads
- Lack of transparency in attribution

**For Networks:**
- No common protocol for conversational advertising
- Each platform requires custom integration
- Fraud prevention is ad-hoc and inconsistent

### 2.3 AIP Solution

AIP solves these problems by providing:

1. **Standard Protocol:** Platforms integrate once, access all AIP-compatible networks
2. **Performance Pricing:** CPX → CPC → CPA billing with verifiable attribution
3. **Built-in Fraud Prevention:** HMAC signatures, nonce validation, trust scoring
4. **Transparent Settlement:** 70/30 revenue split, immutable ledger, monthly payouts

---

## 3. Roles & Actors

### 3.1 Platform

**Definition:** An AI application, chatbot, or agent that serves users and integrates AIP to monetize high-intent moments.

**Examples:**
- Conversational AI (ChatGPT, Claude, Perplexica)
- Voice assistants (Alexa, Google Assistant)
- Shopping agents (autonomous purchase assistants)

**Responsibilities:**
- Detect high-intent moments (purchase queries, research, comparisons)
- Request recommendations from AIP network
- Render ads with required disclosure ("Ad" label, "Why this ad?" tooltip)
- Track events (exposure, click, conversion)
- Receive 70% revenue share

**API Keys:** `pk_test_...` (sandbox), `pk_live_...` (production)

### 3.2 Advertiser Agent

**Definition:** A brand or agency that creates campaigns and bids for relevant contexts.

**Examples:**
- E-commerce brands (Nike, Amazon, Shopify merchants)
- Service providers (Uber, Airbnb, DoorDash)
- B2B companies (Salesforce, HubSpot, Stripe)

**Responsibilities:**
- Fund wallet (minimum $100)
- Create campaigns with targeting (categories, geography)
- Set bids (CPX, CPC, CPA)
- Provide creative assets (title, description, image, URL)
- Monitor performance and optimize bids

**API Keys:** `ak_test_...` (sandbox), `ak_live_...` (production)

### 3.3 Ad Network

**Definition:** An operator that implements AIP to run auctions, track events, and settle payments.

**Examples:**
- AdMesh Network (reference implementation)
- Other AIP-compatible networks (future)

**Responsibilities:**
- Run real-time auctions (<20ms latency)
- Validate events (HMAC, nonce, time windows)
- Manage wallets (reservations, captures, refunds)
- Settle payments (70% platform, 30% network)
- Maintain immutable ledger
- Provide analytics and reporting

**Revenue:** 30% of all transactions

---

## 4. Value Flow Overview

### 4.1 High-Level Flow

```
User Intent → Platform → AIP Network → Auction → Ad Served → Events → Settlement
```

### 4.2 Detailed Flow

1. **User expresses intent:** "What are the best running shoes for marathons?"

2. **Platform detects high-intent moment** and calls AIP network:
   ```
   POST /v1/context
   {
     "session_id": "sess_123",
     "query": "best running shoes for marathons",
     "categories": ["sports", "footwear"],
     "geography": "US"
   }
   ```

3. **Network runs auction:**
   - Query eligible advertisers (category + geo match, trust score ≥0.6)
   - Calculate Expected Value (EV) for each advertiser
   - Select winner (highest EV)
   - Determine CPX charge (second-price auction)
   - Reserve CPX amount in winner's wallet

4. **Network returns recommendation:**
   ```
   {
     "serve_token": "st_abc123",
     "recommendation": {
       "title": "UltraRun Pro - Marathon Edition",
       "description": "Engineered for long-distance performance",
       "url": "https://example.com/ultrarun-pro",
       "image_url": "https://cdn.example.com/images/ultrarun.jpg"
     }
   }
   ```

5. **Platform renders ad** with disclosure ("Ad" label, "Why this ad?" tooltip)

6. **User sees ad** → Platform tracks **exposure event**

7. **User clicks ad** (within 30 min) → Platform tracks **click event**
   - Network releases CPX reservation
   - Network reserves CPC amount

8. **User converts** (within 24h) → Platform tracks **conversion event**
   - Network releases CPC reservation
   - Network captures CPA amount
   - Network credits platform (70%) and network (30%)

9. **Monthly settlement:** Platform requests payout, receives ACH transfer

---

## 5. Billing Units

AIP supports three billing units, charged in priority order (CPA > CPC > CPX).

### 5.1 CPX (Cost Per Exposure)

**Definition:** Charge when ad is displayed to user (viewable impression).

**Trigger:** Exposure event tracked (ad visible in viewport for ≥1 second)

**Typical Range:** $0.10 - $2.00

**Use Case:** Brand awareness, top-of-funnel

**Example:**
- Advertiser bids CPX = $1.50
- Ad shown to user
- Advertiser charged $1.50 (if no click/conversion)

### 5.2 CPC (Cost Per Click)

**Definition:** Charge when user clicks ad.

**Trigger:** Click event tracked (within 30-minute window after exposure)

**Typical Range:** $0.50 - $10.00

**Use Case:** Traffic generation, mid-funnel

**Example:**
- Advertiser bids CPX = $1.50, CPC = $5.00
- Ad shown (CPX reserved)
- User clicks within 30 min
- CPX released, CPC charged
- Advertiser charged $5.00 (not $1.50)

### 5.3 CPA (Cost Per Acquisition)

**Definition:** Charge when user completes desired action (purchase, signup, etc.).

**Trigger:** Conversion event tracked (within 24-hour primary or 7-day fallback window after click)

**Typical Range:** $5.00 - $200.00

**Use Case:** Performance marketing, bottom-funnel

**Example:**
- Advertiser bids CPX = $1.50, CPC = $5.00, CPA = $50.00
- Ad shown (CPX reserved)
- User clicks (CPX released, CPC reserved)
- User converts within 24h (CPC released, CPA charged)
- Advertiser charged $50.00 (not $5.00 or $1.50)

### 5.4 Billing Priority

**Only one billing unit is charged per serve_token:**

```
CPA > CPC > CPX
```

**Logic:**
- If conversion occurs → charge CPA
- Else if click occurs → charge CPC
- Else if exposure occurs → charge CPX
- Else (no events) → no charge

---

## 6. Event Windows

Event windows define the maximum time between events for attribution.

### 6.1 CPX → CPC Window

**Duration:** 30 minutes

**Logic:**
- Click event MUST occur within 30 minutes of exposure event
- If click occurs after 30 minutes → CPX is charged, click is rejected

**Rationale:** Conversational sessions typically complete within 30 minutes. Longer windows increase fraud risk.

### 6.2 CPC → CPA Window

**Primary Window:** 24 hours  
**Fallback Window:** 7 days

**Logic:**
- Conversion event SHOULD occur within 24 hours of click (primary attribution)
- If conversion occurs 24h-7d after click → fallback attribution (lower trust multiplier)
- If conversion occurs after 7 days → CPC is charged, conversion is rejected

**Rationale:** Most conversions happen within 24 hours. 7-day fallback captures delayed purchases while maintaining fraud protection.

### 6.3 Window Enforcement

**Implementation:**
```typescript
function validateClickWindow(exposureTimestamp: number, clickTimestamp: number): boolean {
  const elapsed = clickTimestamp - exposureTimestamp;
  const maxWindow = 30 * 60 * 1000; // 30 minutes in ms
  return elapsed <= maxWindow;
}

function validateConversionWindow(clickTimestamp: number, conversionTimestamp: number): 'primary' | 'fallback' | 'expired' {
  const elapsed = conversionTimestamp - clickTimestamp;
  const primaryWindow = 24 * 60 * 60 * 1000; // 24 hours
  const fallbackWindow = 7 * 24 * 60 * 60 * 1000; // 7 days
  
  if (elapsed <= primaryWindow) return 'primary';
  if (elapsed <= fallbackWindow) return 'fallback';
  return 'expired';
}
```

---

## 7. Auction Logic

### 7.1 Auction Trigger

Auction runs when platform calls `POST /v1/context`.

### 7.2 Advertiser Eligibility

Advertisers are eligible if:
1. **Category match:** Campaign targets at least one category in context request
2. **Geography match:** Campaign targets user's geography
3. **Trust score ≥0.6:** Advertiser has sufficient trust score
4. **Active campaign:** Campaign status is "active"
5. **Sufficient wallet balance:** Balance ≥ CPX bid

### 7.3 Expected Value (EV) Calculation

For each eligible advertiser, calculate EV:

```
EV = CPX + (CTR_est × CPC) + (CVR_est × CPA) × TrustMultiplier
```

**Where:**
- `CPX` = Cost Per Exposure bid
- `CTR_est` = Estimated click-through rate (historical performance)
- `CPC` = Cost Per Click bid
- `CVR_est` = Estimated conversion rate (historical performance)
- `CPA` = Cost Per Acquisition bid
- `TrustMultiplier` = Trust score multiplier (0.5 - 1.2)

**Example:**
```
Advertiser A:
  CPX = $1.50
  CPC = $5.00, CTR_est = 0.05 (5%)
  CPA = $50.00, CVR_est = 0.02 (2%)
  TrustScore = 0.9 → TrustMultiplier = 1.1

EV_A = 1.50 + (0.05 × 5.00) + (0.02 × 50.00) × 1.1
     = 1.50 + 0.25 + 1.10
     = $2.85
```

### 7.4 Winner Selection

1. **Sort by EV** (descending)
2. **Select highest EV** as winner
3. **Tie-breaking:** If multiple advertisers have same EV:
   - Higher trust score wins
   - If still tied, random selection

### 7.5 Second-Price Auction (CPX Only)

**Winner pays the second-highest CPX bid**, not their own bid.

**Rationale:** Encourages truthful bidding, prevents bid inflation.

**Example:**
```
Advertiser A: CPX = $1.50, EV = $2.85 (winner)
Advertiser B: CPX = $1.20, EV = $2.60 (second)

Winner: Advertiser A
CPX Charged: $1.20 (Advertiser B's CPX bid)
```

**Note:** CPC and CPA are charged at bid price, not second-price.

### 7.6 Auction Latency SLO

**Target:** ≤20ms (p95)

**Optimization Strategies:**
- Pre-filter advertisers by category/geo (indexed queries)
- Cache CTR/CVR estimates
- Parallel EV calculation
- Connection pooling

---

## 8. Event State Machine

### 8.1 States

1. **AUCTION_WON:** Auction completed, serve_token generated
2. **EXPOSURE_PENDING:** Exposure event received, CPX reserved
3. **CLICK_PENDING:** Click event received (within 30 min), CPC reserved
4. **CONVERSION_PENDING:** Conversion event received (within 24h/7d), CPA reserved
5. **FINALIZED:** Final billing unit captured, ledger updated

### 8.2 State Transitions

```
AUCTION_WON
    ↓ (exposure event)
EXPOSURE_PENDING
    ↓ (click within 30 min)        ↓ (30 min timeout)
CLICK_PENDING                    FINALIZED (CPX charged)
    ↓ (conversion within 24h/7d)    ↓ (24h/7d timeout)
CONVERSION_PENDING               FINALIZED (CPC charged)
    ↓ (verification)
FINALIZED (CPA charged)
```

### 8.3 State Diagram (ASCII)

```
┌─────────────┐
│ AUCTION_WON │
└──────┬──────┘
       │ exposure
       ↓
┌──────────────────┐
│ EXPOSURE_PENDING │ (CPX reserved)
└────┬─────────┬───┘
     │         │ timeout (30 min)
     │         ↓
     │    ┌───────────┐
     │    │ FINALIZED │ (CPX charged)
     │    └───────────┘
     │ click (within 30 min)
     ↓
┌─────────────────┐
│  CLICK_PENDING  │ (CPC reserved)
└────┬────────┬───┘
     │        │ timeout (24h/7d)
     │        ↓
     │   ┌───────────┐
     │   │ FINALIZED │ (CPC charged)
     │   └───────────┘
     │ conversion (within 24h/7d)
     ↓
┌────────────────────┐
│ CONVERSION_PENDING │ (CPA reserved)
└─────────┬──────────┘
          │ verification
          ↓
     ┌───────────┐
     │ FINALIZED │ (CPA charged)
     └───────────┘
```

### 8.4 Wallet Operations by State

| State | Wallet Operation |
|-------|------------------|
| AUCTION_WON | Reserve CPX (second-price) |
| EXPOSURE_PENDING | CPX reserved |
| CLICK_PENDING | Release CPX, Reserve CPC |
| CONVERSION_PENDING | Release CPC, Reserve CPA |
| FINALIZED | Capture final billing unit |

---

## 9. Wallet & Payout Logic

### 9.1 Advertiser Wallet

**Purpose:** Pre-funded balance for ad spend.

**Minimum Balance:** $100 (initial funding)

**Funding Methods:**
- Credit card (via Stripe)
- ACH transfer
- Wire transfer

**Wallet Operations:**
1. **Reserve:** Hold funds for pending events (CPX, CPC, CPA)
2. **Capture:** Charge reserved funds when event finalizes
3. **Release:** Return reserved funds when higher-priority event occurs

**Example Flow:**
```
Initial Balance: $1,000

Auction Won (CPX = $1.50):
  Reserved: $1.50
  Available: $998.50

Click Event (CPC = $5.00):
  Released: $1.50 (CPX)
  Reserved: $5.00 (CPC)
  Available: $995.00

Conversion Event (CPA = $50.00):
  Released: $5.00 (CPC)
  Reserved: $50.00 (CPA)
  Available: $950.00

Finalized:
  Captured: $50.00 (CPA)
  Final Balance: $950.00
```

### 9.2 Platform Payout

**Revenue Share:** 70% of all charges

**Payout Frequency:** Monthly (Net-7)

**Minimum Payout:** $50

**Payout Methods:**
- ACH transfer (5-7 business days)
- Wire transfer (1-3 business days, $25 fee)
- PayPal (1-2 business days, 2% fee)

**Payout Eligibility:**
- Events must be ≥7 days old (fraud review period)
- Platform must have valid bank account on file
- Minimum $50 accumulated

**Example:**
```
Month: November 2025
Total Charges: $10,000
Platform Share (70%): $7,000
Network Share (30%): $3,000

Payout Request: December 7, 2025
ACH Transfer: December 14, 2025
```

### 9.3 Revenue Split

**Platform:** 70%  
**Network:** 30%

**Rationale:**
- Platforms generate high-intent traffic and own user relationships
- Networks provide infrastructure, fraud prevention, and advertiser acquisition
- 70/30 split aligns incentives and is competitive with industry standards

**Applied to:**
- All billing units (CPX, CPC, CPA)
- All events (exposure, click, conversion)

**Example:**
```
CPA Charge: $50.00
Platform Revenue: $35.00 (70%)
Network Revenue: $15.00 (30%)
```

---

## 10. Interoperability & Open Standard

### 10.1 Network-Agnostic Protocol

AIP is **not** a proprietary platform. It's an open protocol that any ad network can implement.

**Benefits:**
- **For Platforms:** Integrate once, access multiple networks
- **For Advertisers:** Reach users across all AIP-compatible platforms
- **For Networks:** Join ecosystem without custom integrations

### 10.2 AdMesh as Reference Implementation

**AdMesh Network** is the reference implementation and protocol maintainer, but:
- Other networks can implement AIP
- Networks can obtain "AIP Compatible" certification
- AdMesh does not control or gatekeep the protocol

### 10.3 Certification Program

**Purpose:** Verify that networks correctly implement AIP.

**Requirements:**
1. Pass all acceptance tests (see Section 17)
2. Maintain SLOs (see Section 12)
3. Implement security measures (see Section 11)
4. Publish API documentation
5. Provide SDK support

**Process:**
1. Submit application to certification@admesh.network
2. Run conformance test suite
3. Complete security audit
4. Receive "AIP Compatible" designation
5. Listed on admesh.network/certified-networks

**Renewal:** Annual recertification required

### 10.4 Governance

**Protocol Maintainer:** AdMesh Network

**Change Process:**
- Minor changes (backward-compatible): AdMesh decision
- Major changes (breaking): RFC process with 60-day public comment period

**Community Input:**
- GitHub discussions
- Discord community
- Quarterly governance calls

See [Section 14: Versioning & Governance](#14-versioning--governance) for details.

---

## 11. Security & Trust

### 11.1 Transport Security

**Requirement:** All API communication MUST use HTTPS with TLS 1.3+

**Mutual TLS (mTLS):** Recommended for production environments

**Certificate Requirements:**
- Minimum 2048-bit RSA or 256-bit ECDSA
- Valid for ≤365 days
- Issued by trusted CA

### 11.2 Authentication

**API Keys:**
- Platform keys: `pk_test_...` (sandbox), `pk_live_...` (production)
- Advertiser keys: `ak_test_...` (sandbox), `ak_live_...` (production)

**Key Management:**
- Rotate every 90 days
- Store in environment variables, never in code
- Revoke immediately if compromised

### 11.3 Request Signing (HMAC)

**Requirement:** All event tracking requests MUST include HMAC-SHA256 signature.

**Algorithm:**
```typescript
function generateHMAC(payload: object, secret: string): string {
  const message = JSON.stringify(payload);
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(message);
  return hmac.digest('hex');
}
```

**Header:**
```
X-AIP-Signature: <hmac_hex>
```

**Validation:**
- Network recomputes HMAC using shared secret
- Compares with provided signature using timing-safe comparison
- Rejects request if mismatch

### 11.4 Replay Protection (Nonce)

**Requirement:** Each event request MUST include a unique nonce.

**Format:** UUID v4

**TTL:** 60 seconds

**Validation:**
- Network checks if nonce has been used
- Rejects duplicate nonces
- Expires nonces after 60 seconds

### 11.5 Trust Scoring

**Purpose:** Prevent fraud and incentivize quality.

**Range:** 0.0 (untrusted) to 1.0 (fully trusted)

**Minimum for Auction:** 0.6

**Factors:**
- Account age
- Payment history
- Event quality (fraud rate)
- Compliance violations

**Trust Multiplier in EV:**
```
TrustScore → TrustMultiplier
0.0-0.5   → 0.5 (penalty)
0.6-0.7   → 0.8
0.8-0.9   → 1.0 (neutral)
0.9-1.0   → 1.2 (bonus)
```

**Penalties:**
- First violation: -0.1 (warning)
- Second violation: -0.3 (probation)
- Third violation: 0.0 (suspension)

**Recovery:** +0.1 per 30 days of clean activity

See [Appendix D: Trust Score Calculation](#appendix-d-trust-score-calculation) for details.

### 11.6 Fraud Detection

**Duplicate Events:**
- Track serve_token + event_type combinations
- Reject duplicates with 409 Conflict

**Anomaly Detection:**
- Monitor for unusual patterns (spike in events, abnormal CTR/CVR)
- Flag for manual review
- Automatic throttling if fraud score exceeds threshold

**Session Binding:**
- Validate session_id consistency across events
- Reject events with mismatched session_id

---

## 12. Observability & SLOs

### 12.1 Service Level Objectives (SLOs)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Auction Latency | ≤20ms (p95) | Time from context request to response |
| Event Ingest Latency | ≤50ms (p95) | Time from event submission to acknowledgment |
| API Uptime | 99.9% | Monthly uptime percentage |
| Duplicate Event Rate | <0.01% | Percentage of duplicate events detected |
| Wallet Error Rate | <1% | Percentage of wallet operations that fail |

### 12.2 Monitoring

**Required Metrics:**
- Request rate (per endpoint)
- Error rate (per endpoint, per error code)
- Latency (p50, p95, p99)
- Auction participation rate
- Event state transitions
- Wallet balance changes

**Alerting:**
- SLO violations
- Fraud detection triggers
- Low wallet balance
- Payment failures

### 12.3 Logging

**Event Logs:**
- All API requests (timestamp, endpoint, API key, IP, user agent)
- All event tracking (serve_token, event_type, timestamp, HMAC)
- All wallet operations (transaction_id, amount, type, timestamp)

**Retention:**
- Raw logs: 90 days
- Aggregated metrics: 2 years
- Ledger: 7 years (immutable)

**Format:** JSON structured logs

**Example:**
```json
{
  "timestamp": "2025-11-11T14:30:00.000Z",
  "event_type": "context_request",
  "platform_id": "plt_abc123",
  "session_id": "sess_xyz789",
  "categories": ["sports", "footwear"],
  "auction_winner": "adv_def456",
  "auction_latency_ms": 18,
  "serve_token": "st_ghi789"
}
```

### 12.4 Analytics

**Platform Dashboard:**
- Revenue (daily, monthly, lifetime)
- Event counts (exposure, click, conversion)
- Top categories
- Geographic distribution

**Advertiser Dashboard:**
- Spend (daily, monthly, lifetime)
- Campaign performance (impressions, clicks, conversions)
- CTR, CVR, CPA
- Trust score history

---

## 13. Privacy & Retention

### 13.1 Privacy Principles

1. **No PII Storage:** AIP does not store personally identifiable information
2. **Contextual Signals Only:** Use query text, categories, geography—not user profiles
3. **User Consent:** Platforms must obtain user consent before tracking
4. **Transparency:** Users must see "Ad" label and "Why this ad?" tooltip

### 13.2 Data Minimization

**Context Requests:**
- Store: query text, categories, geography, timestamp
- Do NOT store: user ID, email, name, IP address (beyond fraud detection)

**Event Tracking:**
- Store: serve_token, event_type, timestamp, session_id
- Do NOT store: user ID, device ID, cookies

### 13.3 Retention Policies

| Data Type | Retention Period | Rationale |
|-----------|------------------|-----------|
| Raw context requests | 90 days | Fraud detection, debugging |
| Event logs | 90 days | Fraud detection, debugging |
| Aggregated analytics | 2 years | Performance analysis |
| Ledger records | 7 years | Financial compliance, audits |
| User consent records | 3 years | Legal compliance (GDPR) |

### 13.4 Compliance

**GDPR (EU):**
- Right to access: Platforms can query their own data via API
- Right to deletion: Contact support@admesh.network
- Data portability: Export via API or CSV

**CCPA (California):**
- Do Not Sell: AIP does not sell user data
- Opt-out: Platforms must provide opt-out mechanisms

**COPPA (Children):**
- AIP is not intended for users under 13
- Platforms must verify user age before tracking

---

## 14. Versioning & Governance

### 14.1 Semantic Versioning

AIP follows [Semantic Versioning 2.0.0](https://semver.org/):

**Format:** `MAJOR.MINOR.PATCH`

**Examples:**
- `0.1.0` - Initial release (current)
- `0.2.0` - Backward-compatible features
- `1.0.0` - First stable release
- `2.0.0` - Breaking changes

### 14.2 API Versioning

**URL Versioning:**
```
https://api.admesh.network/v1/context
https://api.admesh.network/v2/context (future)
```

**Header Versioning:**
```
X-AIP-Version: 0.1
```

**Deprecation Policy:**
- Announce deprecation 90 days before removal
- Support old version for 180 days after new version release
- Dual-stack support during transition

### 14.3 Change Process

**Minor Changes (Backward-Compatible):**
- New optional fields
- New endpoints
- Performance improvements
- Bug fixes

**Process:**
1. AdMesh proposes change
2. 14-day public comment period
3. AdMesh makes final decision
4. Update specification and SDKs

**Major Changes (Breaking):**
- Required field changes
- Endpoint removal
- Schema changes
- Behavioral changes

**Process:**
1. Submit RFC (Request for Comments)
2. 60-day public comment period
3. Community feedback incorporated
4. AdMesh core team makes final decision
5. Publish final specification 30 days before implementation
6. Dual-stack support for 180 days

### 14.4 Governance Structure

**Protocol Maintainer:** AdMesh Network

**Core Team:**
- Technical Lead
- Product Manager
- Security Lead
- Community Manager

**Community Advisory Board (Planned for v1.0):**
- Representatives from platforms, advertisers, networks
- Quarterly meetings
- Input on major changes

**Communication Channels:**
- GitHub: [github.com/admesh/aip-spec](https://github.com/admesh/aip-spec)
- Discord: [discord.gg/admesh](https://discord.gg/admesh)
- Email: spec@admesh.network

---

## 15. SDK Deliverables

### 15.1 Platform SDK

**Purpose:** Simplify AIP integration for platforms.

**Languages:**
- JavaScript/TypeScript (Node.js, browser)
- Python (3.8+)

**Features:**
- Context request API wrapper
- Event tracking with automatic HMAC signing
- Nonce generation
- Revenue analytics
- Payout management

**Example (TypeScript):**
```typescript
import { AdMeshPlatform } from '@admesh/platform-sdk';

const platform = new AdMeshPlatform({
  apiKey: process.env.ADMESH_PLATFORM_KEY,
  environment: 'production'
});

// Fetch recommendation
const recommendation = await platform.fetchRecommendation({
  sessionId: 'sess_123',
  query: 'best running shoes',
  categories: ['sports', 'footwear'],
  geography: 'US'
});

// Track exposure
await platform.trackExposure(recommendation.serveToken);

// Track click
await platform.trackClick(recommendation.serveToken);

// Track conversion
await platform.trackConversion(recommendation.serveToken, {
  conversionValue: 129.99,
  conversionType: 'purchase'
});
```

### 15.2 Agent SDK

**Purpose:** Simplify campaign management for advertisers.

**Languages:**
- JavaScript/TypeScript
- Python

**Features:**
- Wallet management (fund, check balance)
- Campaign creation and management
- Performance analytics
- Webhook handling

**Example (TypeScript):**
```typescript
import { AdMeshAgent } from '@admesh/agent-sdk';

const agent = new AdMeshAgent({
  apiKey: process.env.ADMESH_AGENT_KEY,
  environment: 'production'
});

// Fund wallet
await agent.fundWallet({
  amount: 500.00,
  paymentMethodId: 'pm_card_visa'
});

// Create campaign
const campaign = await agent.createCampaign({
  name: 'Marathon Shoes Q4',
  categories: ['sports', 'footwear'],
  geography: ['US'],
  bids: {
    cpx: 1.50,
    cpc: 5.00,
    cpa: 50.00
  },
  recommendation: {
    title: 'UltraRun Pro',
    description: 'Engineered for marathons',
    url: 'https://example.com/ultrarun-pro',
    imageUrl: 'https://cdn.example.com/images/ultrarun.jpg'
  }
});

// Get performance
const performance = await agent.getCampaignPerformance(campaign.campaignId);
console.log(`Conversions: ${performance.conversions}`);
```

### 15.3 React Components (Platform SDK)

**Purpose:** Pre-built UI components for rendering ads.

**Components:**
- `<AdMeshRecommendation>` - Render recommendation with disclosure
- `<AdMeshProvider>` - Context provider for SDK initialization

**Example:**
```tsx
import { AdMeshProvider, AdMeshRecommendation } from '@admesh/platform-sdk/react';

function App() {
  return (
    <AdMeshProvider apiKey="pk_live_..." environment="production">
      <ChatInterface />
    </AdMeshProvider>
  );
}

function ChatMessage({ recommendation }) {
  return (
    <div>
      <p>{message.text}</p>
      {recommendation && (
        <AdMeshRecommendation
          recommendation={recommendation}
          onExposure={() => console.log('Exposed')}
          onClick={() => console.log('Clicked')}
        />
      )}
    </div>
  );
}
```

---

## 16. Economics & Defaults

### 16.1 Currency

**Default:** USD (United States Dollar)

**Future:** Multi-currency support planned for v0.2

### 16.2 Minimum Balances

**Advertiser Wallet:** $100 (initial funding)

**Platform Payout:** $50 (minimum payout amount)

### 16.3 Default Bids

**Suggested Starting Bids:**
- CPX: $1.00
- CPC: $3.00
- CPA: $30.00

**Rationale:** Conservative starting point, advertisers can optimize based on performance.

### 16.4 Payment Terms

**Advertiser Wallet Funding:** Immediate (credit card, ACH)

**Platform Payout:** Net-7 (7 days after month end)

**Example:**
- November 2025 revenue: $5,000
- Payout request: December 7, 2025
- ACH transfer: December 14, 2025

### 16.5 Fees

**Platform Integration:** Free (no setup fees, no monthly fees)

**Advertiser Account:** Free (no setup fees, no monthly fees)

**Transaction Fees:** None (revenue split covers network costs)

**Payout Fees:**
- ACH: Free
- Wire transfer: $25
- PayPal: 2% of payout amount

---

## 17. Acceptance Tests

Networks seeking "AIP Compatible" certification must pass all acceptance tests.

### 17.1 Functional Tests

**Test 1: Context Request & Auction**
- **Given:** Platform sends context request with valid API key
- **When:** Network runs auction
- **Then:** Network returns recommendation with serve_token within 20ms (p95)

**Test 2: Exposure Event Tracking**
- **Given:** Platform tracks exposure event with valid HMAC signature
- **When:** Network validates and processes event
- **Then:** Event state transitions to EXPOSURE_PENDING, CPX reserved

**Test 3: Click Event Tracking (Within Window)**
- **Given:** Platform tracks click event within 30 minutes of exposure
- **When:** Network validates time window
- **Then:** CPX released, CPC reserved, state transitions to CLICK_PENDING

**Test 4: Click Event Rejection (Outside Window)**
- **Given:** Platform tracks click event 31 minutes after exposure
- **When:** Network validates time window
- **Then:** Event rejected with 422 error, CPX captured, state finalized

**Test 5: Conversion Event Tracking (Primary Window)**
- **Given:** Platform tracks conversion within 24 hours of click
- **When:** Network validates time window
- **Then:** CPC released, CPA reserved, state transitions to CONVERSION_PENDING

**Test 6: Conversion Event Tracking (Fallback Window)**
- **Given:** Platform tracks conversion 25 hours after click (within 7 days)
- **When:** Network validates fallback window
- **Then:** CPC released, CPA reserved with lower trust multiplier

**Test 7: Duplicate Event Rejection**
- **Given:** Platform submits same event twice (same serve_token + event_type)
- **When:** Network detects duplicate
- **Then:** Second event rejected with 409 Conflict

**Test 8: HMAC Signature Validation**
- **Given:** Platform submits event with invalid HMAC signature
- **When:** Network validates signature
- **Then:** Event rejected with 401 Unauthorized

**Test 9: Nonce Validation**
- **Given:** Platform submits event with reused nonce
- **When:** Network checks nonce uniqueness
- **Then:** Event rejected with 400 Bad Request

**Test 10: Wallet Reservation & Capture**
- **Given:** Advertiser has $100 balance, wins auction with CPX = $1.50
- **When:** Exposure event tracked
- **Then:** Available balance = $98.50, Reserved = $1.50
- **When:** Event finalizes
- **Then:** Available balance = $98.50, Reserved = $0, Charged = $1.50

### 17.2 Security Tests

**Test 11: API Key Authentication**
- **Given:** Platform sends request with invalid API key
- **When:** Network validates API key
- **Then:** Request rejected with 401 Unauthorized

**Test 12: Rate Limiting**
- **Given:** Platform exceeds 1,000 context requests per minute
- **When:** Network enforces rate limit
- **Then:** Requests rejected with 429 Too Many Requests

### 17.3 Performance Tests

**Test 13: Auction Latency SLO**
- **Given:** 1,000 concurrent context requests
- **When:** Network processes auctions
- **Then:** p95 latency ≤20ms

---

## 18. Governance Summary

### 18.1 Protocol Ownership

**Maintainer:** AdMesh Network

**License:** Apache 2.0 or MIT (dual-licensed)

**Open Source:** Full specification published on GitHub

### 18.2 Decision-Making

**Minor Changes:** AdMesh core team decision after 14-day public comment

**Major Changes:** RFC process with 60-day public comment, community input

**Emergency Changes:** Immediate implementation for critical security issues

### 18.3 Community Participation

**Channels:**
- GitHub Discussions: Feature requests, questions
- Discord: Real-time chat, community support
- Quarterly Calls: Governance updates, roadmap discussion

**Contribution:**
- Bug reports: GitHub Issues
- Feature proposals: GitHub Discussions
- RFCs: Formal proposals for breaking changes

### 18.4 Roadmap

**v0.1 (Current):** Foundational implementation
- Core auction mechanics
- Event state machine
- Platform and Agent SDKs
- Wallet and settlement

**v0.2 (Q1 2026):** Enhanced features
- Multi-currency support
- Auto-bidding strategies
- Enhanced fraud detection
- Go and Ruby SDKs

**v1.0 (Q3 2026):** Ecosystem maturity
- Community advisory board
- Multi-network federation
- Cross-network attribution
- Advanced privacy controls

---

## Appendix A: Glossary

**AIP:** Agentic Intent Protocol

**CPX:** Cost Per Exposure (billing unit)

**CPC:** Cost Per Click (billing unit)

**CPA:** Cost Per Acquisition (billing unit)

**EV:** Expected Value (auction ranking metric)

**HMAC:** Hash-based Message Authentication Code (request signing)

**mTLS:** Mutual Transport Layer Security (authentication)

**Nonce:** Number used once (replay protection)

**Serve Token:** Unique identifier for ad serving instance

**Trust Score:** Advertiser quality metric (0.0-1.0)

**SLO:** Service Level Objective (performance target)

---

## Appendix B: API Reference

See [api-schemas.md](./api-schemas.md) for complete API documentation.

**Core Endpoints:**
- `POST /v1/context` - Context request and auction
- `POST /v1/events` - Event tracking
- `GET /v1/wallet/balance` - Wallet balance query
- `POST /v1/wallet/fund` - Wallet funding
- `POST /v1/payouts/request` - Platform payout request
- `POST /v1/campaigns` - Campaign creation
- `GET /v1/campaigns/{id}` - Campaign details

---

## Appendix C: State Transition Table

| Current State | Event | Condition | Next State | Wallet Operation |
|---------------|-------|-----------|------------|------------------|
| AUCTION_WON | exposure | Valid HMAC | EXPOSURE_PENDING | Reserve CPX |
| EXPOSURE_PENDING | click | Within 30 min | CLICK_PENDING | Release CPX, Reserve CPC |
| EXPOSURE_PENDING | timeout | 30 min elapsed | FINALIZED | Capture CPX |
| CLICK_PENDING | conversion | Within 24h | CONVERSION_PENDING | Release CPC, Reserve CPA |
| CLICK_PENDING | conversion | 24h-7d | CONVERSION_PENDING | Release CPC, Reserve CPA (lower trust) |
| CLICK_PENDING | timeout | 7d elapsed | FINALIZED | Capture CPC |
| CONVERSION_PENDING | verification | Verified | FINALIZED | Capture CPA |

---

## Appendix D: Trust Score Calculation

**Initial Score:** 0.6 (new accounts)

**Factors:**

1. **Account Age:**
   - 0-30 days: 0.6
   - 30-90 days: 0.8
   - 90+ days: 1.0

2. **Payment History:**
   - On-time payments: +0.1
   - Late payments: -0.1
   - Chargebacks: -0.3

3. **Event Quality:**
   - Fraud rate <0.1%: +0.1
   - Fraud rate 0.1-1%: 0.0
   - Fraud rate >1%: -0.2

4. **Compliance:**
   - No violations: 0.0
   - First violation: -0.1
   - Second violation: -0.3
   - Third violation: -1.0 (suspension)

**Trust Multiplier:**
```
TrustScore → TrustMultiplier (used in EV calculation)
0.0-0.5   → 0.5
0.6-0.7   → 0.8
0.8-0.9   → 1.0
0.9-1.0   → 1.2
```

**Recovery:** +0.1 per 30 days of clean activity (max 1.0)

---

## Appendix E: Contact Information

**General Inquiries:** hello@admesh.network

**Technical Support:** support@admesh.network

**Security Issues:** security@admesh.network

**Certification:** certification@admesh.network

**Specification Questions:** spec@admesh.network

**GitHub:** [github.com/admesh/aip-spec](https://github.com/admesh/aip-spec)

**Discord:** [discord.gg/admesh](https://discord.gg/admesh)

**Website:** [admesh.network](https://admesh.network)

---

**Document Version:** 1.0  
**Specification Version:** AIP v0.1  
**Last Updated:** 2025-11-11  
**Next Review:** 2026-02-11

**Copyright:** © 2025 AdMesh Network  
**License:** Apache 2.0 or MIT (dual-licensed)

---

*This Product Requirements Document defines the Agentic Intent Protocol (AIP) v0.1. Together with the API schemas, event flow diagrams, and integration guides, it establishes the foundational specification for agentic and conversational advertising. AdMesh Network operates the reference implementation, but any compliant ad network can adopt AIP to power its own marketplace. Together they establish the intent-monetization layer for the agent economy.*

