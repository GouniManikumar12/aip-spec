# AMXP v0.1 - Executive Summary

**AdMesh Exchange Protocol (AMXP)** is an open-source protocol for conversational and agentic advertising.

---

## What is AMXP?

AMXP enables:
- **AI Platforms** to monetize high-intent moments in conversations
- **Advertisers** to reach users expressing purchase intent
- **Ad Networks** to operate transparent, performance-based marketplaces

---

## Core Innovation

### 3 Billing Units, 1 Charge

**CPX** (Cost Per Exposure) → **CPC** (Cost Per Click) → **CPA** (Cost Per Acquisition)

Only the highest-value event is charged:
- If user converts → charge CPA ($5-$200)
- Else if user clicks → charge CPC ($0.50-$10)
- Else if user sees ad → charge CPX ($0.10-$2)

### Time-Windowed Attribution

- **CPX → CPC:** 30 minutes
- **CPC → CPA:** 24 hours (primary) or 7 days (fallback)

### Revenue Split

- **Platform:** 70%
- **Network:** 30%

---

## How It Works

### 1. User Intent
```
User: "What are the best running shoes for marathons?"
```

### 2. Platform Requests Recommendation
```http
POST /v1/context
{
  "query": "best running shoes for marathons",
  "categories": ["sports", "footwear"],
  "geography": "US"
}
```

### 3. Network Runs Auction (<20ms)
- Query eligible advertisers
- Calculate Expected Value (EV) for each
- Select winner (highest EV)
- Reserve CPX in winner's wallet

### 4. Platform Renders Ad
- Display recommendation with "Ad" label
- Show "Why this ad?" tooltip
- Track exposure when visible

### 5. Events Tracked
- **Exposure:** Ad shown → CPX reserved
- **Click:** User clicks (within 30 min) → CPX released, CPC reserved
- **Conversion:** User purchases (within 24h) → CPC released, CPA charged

### 6. Monthly Settlement
- Platform receives 70% of charges
- Network keeps 30%
- Payout via ACH (Net-7)

---

## Key Features

### ✅ Open Standard
- Network-agnostic protocol
- Any network can implement and certify
- AdMesh is reference implementation

### ✅ Performance-Based
- Pay only for verified events
- Real-time auctions (<20ms)
- Transparent EV-based ranking

### ✅ Fraud-Resistant
- HMAC signatures on all events
- Nonce validation (60s TTL)
- Trust scoring (0.0-1.0)
- Duplicate detection

### ✅ Privacy-First
- No PII storage
- Contextual signals only
- GDPR/CCPA compliant

### ✅ Developer-Friendly
- Simple SDKs (JavaScript, Python)
- 5-minute integration
- Pre-built React components

---

## Auction Logic

### Expected Value (EV) Formula

```
EV = CPX + (CTR_est × CPC) + (CVR_est × CPA) × TrustMultiplier
```

**Example:**
```
Advertiser A:
  CPX = $1.50
  CPC = $5.00, CTR = 5%
  CPA = $50.00, CVR = 2%
  Trust = 0.9 → Multiplier = 1.1

EV = 1.50 + (0.05 × 5.00) + (0.02 × 50.00) × 1.1
   = 1.50 + 0.25 + 1.10
   = $2.85
```

### Second-Price CPX Auction

Winner pays the **second-highest CPX bid**, not their own.

**Rationale:** Encourages truthful bidding, prevents inflation.

---

## Event State Machine

```
AUCTION_WON
    ↓ exposure
EXPOSURE_PENDING (CPX reserved)
    ↓ click (30 min)          ↓ timeout
CLICK_PENDING (CPC reserved)  FINALIZED (CPX charged)
    ↓ conversion (24h/7d)     ↓ timeout
CONVERSION_PENDING (CPA)      FINALIZED (CPC charged)
    ↓ verified
FINALIZED (CPA charged)
```

---

## Security

### 6 Layers of Protection

1. **Transport:** HTTPS/TLS 1.3+, mTLS recommended
2. **Authentication:** API keys (pk_live_..., ak_live_...)
3. **Request Signing:** HMAC-SHA256 signatures
4. **Replay Protection:** Nonce validation (60s TTL)
5. **Fraud Detection:** Anomaly detection, duplicate rejection
6. **Trust Scoring:** 0.0-1.0 range, minimum 0.6 for auction

---

## Integration

### Platform (5 Minutes)

```typescript
import { AdMeshPlatform } from '@admesh/platform-sdk';

const platform = new AdMeshPlatform({
  apiKey: 'pk_live_...',
  environment: 'production'
});

// Fetch recommendation
const rec = await platform.fetchRecommendation({
  query: 'best running shoes',
  categories: ['sports', 'footwear']
});

// Track events automatically
<AdMeshRecommendation recommendation={rec} autoTrack={true} />
```

### Advertiser (5 Minutes)

```typescript
import { AdMeshAgent } from '@admesh/agent-sdk';

const agent = new AdMeshAgent({
  apiKey: 'ak_live_...',
  environment: 'production'
});

// Fund wallet
await agent.fundWallet({ amount: 500 });

// Create campaign
await agent.createCampaign({
  name: 'Marathon Shoes Q4',
  categories: ['sports', 'footwear'],
  bids: { cpx: 1.50, cpc: 5.00, cpa: 50.00 },
  recommendation: {
    title: 'UltraRun Pro',
    url: 'https://example.com/ultrarun-pro'
  }
});
```

---

## Economics

### Minimum Balances
- **Advertiser Wallet:** $100
- **Platform Payout:** $50

### Payment Terms
- **Advertiser:** Immediate (credit card, ACH)
- **Platform:** Net-7 (monthly payout)

### Fees
- **Integration:** Free
- **Transactions:** None (revenue split covers costs)
- **Payouts:** ACH free, Wire $25, PayPal 2%

---

## SLOs (Service Level Objectives)

| Metric | Target |
|--------|--------|
| Auction Latency | ≤20ms (p95) |
| Event Ingest | ≤50ms (p95) |
| API Uptime | 99.9% |
| Duplicate Rate | <0.01% |
| Wallet Errors | <1% |

---

## Privacy & Compliance

### Data Minimization
- **Store:** Query text, categories, geography
- **Do NOT Store:** User ID, email, IP (beyond fraud detection)

### Retention
- **Raw Logs:** 90 days
- **Analytics:** 2 years
- **Ledger:** 7 years (financial compliance)

### Compliance
- **GDPR:** Right to access, deletion, portability
- **CCPA:** Do not sell, opt-out mechanisms
- **COPPA:** Not for users under 13

---

## Governance

### Protocol Maintainer
**AdMesh Network** (reference implementation)

### Change Process
- **Minor Changes:** 14-day public comment
- **Major Changes:** 60-day RFC process

### Community
- **GitHub:** [github.com/admesh/amxp-spec](https://github.com/admesh/amxp-spec)
- **Discord:** [discord.gg/admesh](https://discord.gg/admesh)
- **Email:** spec@admesh.network

---

## Roadmap

### v0.1 (Current) - Foundation
- ✅ Core auction mechanics
- ✅ Event state machine
- ✅ Platform & Agent SDKs
- ✅ Wallet & settlement

### v0.2 (Q1 2026) - Enhanced
- Multi-currency support
- Auto-bidding strategies
- ML-based fraud detection
- Go & Ruby SDKs

### v1.0 (Q3 2026) - Maturity
- Community advisory board
- Multi-network federation
- Cross-network attribution
- Advanced privacy controls

---

## Certification

Networks can obtain **"AMXP Compatible"** certification by:

1. Passing all acceptance tests (13 tests)
2. Maintaining SLOs
3. Implementing security measures
4. Publishing API documentation
5. Providing SDK support

**Contact:** certification@admesh.network

---

## Documentation

| Document | Purpose |
|----------|---------|
| [PRD.md](./PRD.md) | Complete specification (1,403 lines) |
| [README.md](./README.md) | Quick start |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |
| [CONFORMANCE.md](./CONFORMANCE.md) | Certification requirements |
| [GOVERNANCE.md](./GOVERNANCE.md) | Decision-making process |
| [SECURITY.md](./SECURITY.md) | Security policy |
| [VERSIONING.md](./VERSIONING.md) | Version management |
| [LICENSE](./LICENSE) | Apache 2.0 or MIT |

---

## Get Started

**Platforms:** [Sign up](https://admesh.network/platform/signup) → Integrate SDK → Monetize

**Advertisers:** [Sign up](https://admesh.network/advertiser/signup) → Fund wallet → Create campaign

**Networks:** [Apply](https://admesh.network/certification) → Implement AMXP → Get certified

---

## Contact

**General:** hello@admesh.network  
**Support:** support@admesh.network  
**Security:** security@admesh.network  
**Certification:** certification@admesh.network  
**Specification:** spec@admesh.network

**Website:** [admesh.network](https://admesh.network)  
**GitHub:** [github.com/admesh/amxp-spec](https://github.com/admesh/amxp-spec)  
**Discord:** [discord.gg/admesh](https://discord.gg/admesh)

---

**Version:** AMXP v0.1  
**Last Updated:** 2025-11-11  
**License:** Apache 2.0 or MIT

---

*AMXP establishes the intent-monetization layer for the agent economy. Open, transparent, and performance-based advertising for conversational AI.*

