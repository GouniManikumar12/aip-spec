# Complete AIP Flow: Platform Request to Final Response

This document maps the complete flow from when an AI platform sends a request through every schema and JSON structure in the AIP protocol.

## Flow Overview

```
AI Platform → PlatformRequest → Operator → ContextRequest → Brand Agents
                                                                    ↓
                                                              Bid (with CreativeInput)
                                                                    ↓
AI Platform ← AuctionResult (with Creative) ← Operator ← Auction Selection
                                                                    ↓
                                                              Events (CPX/CPC/CPA)
                                                                    ↓
                                                              Ledger/Wallet Records
```

## 1. Platform Request (AI Platform → Operator)

**Schema:** [`platform-request.json`](../schemas/platform-request.json)

The AI platform initiates an ad auction by sending a `PlatformRequest` to the operator.

### Key Fields:
- `request_id`: Unique identifier for this auction request
- `session_id`: Conversation or interaction session ID
- `message_id`: **Strongly recommended** - Unique identifier for this message in the conversation. Used for deduplication across platforms.
- `platform_id`: Identifier of the AI platform
- `query_text`: User's raw query text
- `locale`: User locale (BCP 47 format, e.g., "en-US")
- `geo`: User country code (ISO 3166-1 alpha-2, e.g., "US")
- `cpx_floor`: Minimum CPX (USD) required by the platform
- `latency_budget_ms`: Optional latency budget from platform in milliseconds
- `device_type`: Device type (mobile, desktop, tablet)
- `auth`: Authentication with nonce and signature

### Example:
```json
{
  "request_id": "req_92fA1",
  "session_id": "sess_001",
  "message_id": "msg_sess_001_1234567890_abc123",
  "platform_id": "openai_chat",
  "model": "gpt-4.3-mini",
  "query_text": "best CRM for small teams",
  "messages": [
    { "role": "user", "content": "best CRM tools?" },
    { "role": "assistant", "content": "HubSpot, Zoho, Salesforce…" }
  ],
  "locale": "en-US",
  "geo": "US",
  "platform_surface": "ai_chat",
  "cpx_floor": 0.05,
  "device_type": "desktop",
  "user_id": "user_hash_abc123",
  "timestamp": "2025-11-14T18:22:00Z",
  "latency_budget_ms": 500,
  "auth": {
    "nonce": "nonce_12345",
    "sig": "sig_d41d8cd98f00b204e9800998ecf8427e"
  },
  "metadata": {
    "openai": { "model": "gpt-4.3-mini", "conversation_mode": "assistant" }
  }
}
```

---

## 2. Context Request (Operator → Brand Agents)

**Schema:** [`context-request.json`](../schemas/context-request.json)

The operator normalizes the platform request and enriches it with intent analysis, then sends a `ContextRequest` to brand agents.

**Important**: The operator automatically fetches `allowed_formats` from the platform's configuration (set during onboarding). Platforms do not need to specify formats in requests.

### Key Fields:
- `context_id`: Unique ID for this auction request (maps to `request_id`)
- `operator_id`: Identifier of the operator
- `platform_type`: Platform type retrieved from agents collection (not sent by platform)
- `query_text`: Normalized query text
- `intent`: Operator-generated semantic understanding
  - `type`: "informational" | "commercial" | "transactional"
  - `decision_phase`: "research" | "compare" | "decide" | "act"
  - `context_summary`: Short summary of conversation context
  - `turn_index`: How many turns into the session
- `verticals`: Normalized topical verticals (e.g., ["crm", "smb_software"])
- `allowed_formats`: Creative formats allowed (automatically fetched from platform config). Supports: ["weave", "tail", "product_card", "bridge"]

### Example:
```json
{
  "context_id": "ctx_92fA1",
  "session_id": "sess_001",
  "operator_id": "admesh_operator",
  "platform_id": "openai_chat",
  "platform_surface": "ai_chat",
  "model": "gpt-4.3-mini",
  "query_text": "best CRM for small teams",
  "messages": [],
  "locale": "en-US",
  "geo": "US",
  "verticals": ["crm", "smb_software"],
  "intent": {
    "type": "commercial",
    "decision_phase": "compare",
    "context_summary": "User is evaluating CRM tools and narrowing down options.",
    "turn_index": 3
  },
  "allowed_formats": ["weave", "tail", "product_card"],
  "platform_type": "ai_chat_platform",
  "timestamp": "2025-11-14T18:22:00Z",
  "latency_budget_ms": 500,
  "user_id": "user_hash_abc123",
  "conversation_id": "conv_xyz789",
  "device_type": "desktop",
  "auth": {
    "nonce": "nonce_123",
    "sig": "sig_hmac_123abc"
  },
  "metadata": {
    "admesh": { "operator_relevance_score": 0.87 }
  }
}
```

---

## 3. Bid (Brand Agents → Operator)

**Schema:** [`bid.json`](../schemas/bid.json)

Brand agents evaluate the context request and submit bids containing pricing and creative input.

### Key Fields:
- `bid_id`: Unique identifier for this bid
- `brand_agent_id`: Identifier of the brand agent
- `context_id`: ID of the ContextRequest being bid on
- `wallet_id`: Wallet to debit if the bid wins
- `pricing`: Pricing vector
  - `cpx`: Price per exposure (USD, required)
  - `cpc`: Price per click (USD, optional)
  - `cpa`: Price per conversion (USD, optional)
  - `preferred_pricing_model`: Preferred billing model
- `offer.creative_input`: Unified creative input structure (see CreativeInput schema below)
- `auth`: Nonce and signature for replay protection

### Example:
```json
{
  "bid_id": "bid_7823",
  "brand_agent_id": "brand_agent_123",
  "context_id": "ctx_92f",
  "wallet_id": "wallet_890",
  "pricing": {
    "cpx": "0.05",
    "cpc": "0.45",
    "cpa": "10.00",
    "currency": "USD",
    "preferred_pricing_model": "CPA"
  },
  "offer": {
    "creative_input": {
      "brand_name": "Nimbus",
      "product_name": "Nimbus CRM Pro",
      "short_description": "CRM built for growing teams, with AI-assisted workflows.",
      "long_description": "Nimbus CRM Pro is designed for teams of 5-50 people who need intelligent pipeline management. It includes automated follow-ups, collaborative forecasting, and embedded AI copilots that help close deals faster.",
      "value_props": [
        "Automated pipeline insights",
        "Collaborative forecasting",
        "AI-powered deal recommendations"
      ],
      "context_snippet": "For startups needing higher limits and automated expense workflows.",
      "cta_label": "Start Free Trial",
      "cta_url": "https://nimbus.example.com/signup",
      "assets": {
        "logo_url": "https://cdn.example.com/nimbus/logo.png",
        "image_urls": ["https://cdn.example.com/nimbus/crm.png"],
        "resource_urls": ["https://nimbus.example.com/signup"]
      },
      "product_id": "prod_nimbus_001",
      "categories": ["crm", "saas"],
      "fallback_formats": ["tail", "product_card"],
      "offer_summary": "Special offer: 50% off first year for teams"
    }
  },
  "timestamp": "2025-11-11T18:00:01Z",
  "auth": {
    "nonce": "nonce_456",
    "signature": "sig_789"
  },
  "processing_latency_ms": 42
}
```

---

## 4. Creative Input (Part of Bid)

**Schema:** [`creative-input.json`](../schemas/creative-input.json)

The unified creative input structure that brand agents generate. Contains all fields needed for any ad format.

### Key Fields:
- `brand_name`: Brand or advertiser name
- `product_name`: Product or offer name
- `short_description`: 1-2 sentence summary (max 200 chars)
- `long_description`: 2-4 sentence expanded description (max 500 chars)
- `value_props`: Short value propositions or bullet points
- `context_snippet`: 60-100 character contextual hint for weave format
- `cta_label`: Call-to-action label
- `cta_url`: Call-to-action URL
- `assets`: Creative assets
  - `logo_url`: Product or brand logo URL
  - `image_urls`: Creative image URLs
  - `resource_urls`: Destination or tracking URLs
- `offer_summary`: Optional special offer summary (e.g., discounts, promotions)

### Example:
```json
{
  "brand_name": "Nimbus",
  "product_name": "Nimbus CRM Pro",
  "short_description": "CRM built for growing teams, with AI-assisted workflows.",
  "long_description": "Nimbus CRM Pro is designed for teams of 5-50 people who need intelligent pipeline management. It includes automated follow-ups, collaborative forecasting, and embedded AI copilots that help close deals faster.",
  "value_props": [
    "Automated pipeline insights",
    "Collaborative forecasting",
    "AI-powered deal recommendations"
  ],
  "context_snippet": "For startups needing higher limits and automated expense workflows.",
  "cta_label": "Start Free Trial",
  "cta_url": "https://nimbus.example.com/signup",
  "assets": {
    "logo_url": "https://cdn.example.com/nimbus/logo.png",
    "image_urls": ["https://cdn.example.com/nimbus/crm.png"],
    "resource_urls": ["https://nimbus.example.com/signup"]
  },
  "product_id": "prod_nimbus_001",
  "categories": ["crm", "saas"],
  "fallback_formats": ["tail", "product_card"],
  "offer_summary": "Special offer: 50% off first year for teams"
}
```

---

## 5. Auction Result (Operator → AI Platform)

**Schema:** [`auction-result.json`](../schemas/auction-result.json)

The operator selects the winning bid, generates format-specific creative, and returns the result to the AI platform.

### Key Fields:
- `auction_id`: Unique identifier for this auction
- `serve_token`: Token used to track downstream events
- `winner`: Winning bid info
  - `brand_agent_id`: Winning Brand Agent
  - `preferred_unit`: Requested billing unit (CPX, CPC, or CPA)
  - `reserved_amount_cents`: Amount placed on hold at auction time
- `render`: Format-specific creative content (see Creative schema below)
- `ttl_ms`: Time-to-live in milliseconds (1000-300000)
- `no_bid`: Set to true when no bidder responded

### Example:
```json
{
  "auction_id": "auc_981",
  "serve_token": "stk_abcxyz123",
  "winner": {
    "brand_agent_id": "ba_451",
    "preferred_unit": "CPA",
    "reserved_amount_cents": 500
  },
  "render": {
    "format": "weave",
    "weave_content": "[Ad] For startups needing higher limits and automated expense workflows. CRM built for growing teams, with AI-assisted workflows. Learn more: https://admesh.click/stk_abcxyz123"
  },
  "ttl_ms": 60000
}
```

---

## 6. Creative (Part of Auction Result)

**Schema:** [`creative.json`](../schemas/creative.json)

Format-specific creative content generated by the operator from CreativeInput. Supports four formats: weave, tail, product_card, and bridge.

### Format 1: Weave
Short, inline, contextual text to insert into assistant response.

```json
{
  "format": "weave",
  "weave_content": "[Ad] For startups needing higher limits and automated expense workflows. CRM built for growing teams, with AI-assisted workflows. Learn more: https://admesh.click/stk_abcxyz123"
}
```

### Format 2: Tail
Paragraph-level block ad to show after organic response.

```json
{
  "format": "tail",
  "tail_content": "Nimbus CRM Pro is designed for teams of 5-50 people who need intelligent pipeline management. It includes automated follow-ups, collaborative forecasting, and embedded AI copilots that help close deals faster.\n\nStart Free Trial: https://admesh.click/stk_abcxyz123"
}
```

### Format 3: Product Card
Structured card data with title, description, value props, and assets.

```json
{
  "format": "product_card",
  "product_card": {
    "title": "Nimbus CRM Pro",
    "subtitle": "Nimbus",
    "description": "CRM built for growing teams, with AI-assisted workflows.",
    "value_props": [
      "Automated pipeline insights",
      "Collaborative forecasting",
      "AI-powered deal recommendations"
    ],
    "assets": {
      "logo_url": "https://cdn.example.com/nimbus/logo.png",
      "primary_image_url": "https://cdn.example.com/nimbus/crm.png",
      "image_urls": ["https://cdn.example.com/nimbus/crm.png"]
    },
    "admesh_url": "https://admesh.click/stk_abcxyz123"
  }
}
```

### Format 4: Bridge
Setup prompt or configuration instructions for AI agents. Used primarily for Vibe Coding Platforms and AI IDEs.

```json
{
  "format": "bridge",
  "bridge_content": "To set up Nimbus CRM Pro, install the package using npm install @nimbus/crm-pro. Then configure your API key in the environment variables. See the documentation for detailed setup instructions.",
  "documentation_url": "https://docs.nimbus.com/getting-started"
}
```

---

## 7. Events (Platform → Operator)

After the ad is served, the platform sends events to track user engagement.

### 7.1 CPX Exposure Event

**Schema:** [`event-cpx-exposure.json`](../schemas/event-cpx-exposure.json)

Sent when the user sees the ad.

```json
{
  "event_id": "evt_cpx_001",
  "serve_token": "stk_abcxyz123",
  "event_type": "cpx_exposure",
  "timestamp": "2025-11-14T18:22:05Z",
  "platform_id": "openai_chat",
  "session_id": "sess_001",
  "user_id": "user_hash_abc123",
  "geo": "US",
  "device_type": "desktop",
  "auth": {
    "nonce": "nonce_exposure_123",
    "sig": "sig_exposure_456"
  }
}
```

### 7.2 CPC Click Event

**Schema:** [`event-cpc-click.json`](../schemas/event-cpc-click.json)

Sent when the user clicks the ad.

```json
{
  "event_id": "evt_cpc_001",
  "serve_token": "stk_abcxyz123",
  "event_type": "cpc_click",
  "timestamp": "2025-11-14T18:22:10Z",
  "platform_id": "openai_chat",
  "session_id": "sess_001",
  "user_id": "user_hash_abc123",
  "geo": "US",
  "device_type": "desktop",
  "click_url": "https://admesh.click/stk_abcxyz123",
  "auth": {
    "nonce": "nonce_click_123",
    "sig": "sig_click_456"
  }
}
```

### 7.3 CPA Conversion Event

**Schema:** [`event-cpa-conversion.json`](../schemas/event-cpa-conversion.json)

Sent when the user completes a conversion action (e.g., signup, purchase).

```json
{
  "event_id": "evt_cpa_001",
  "serve_token": "stk_abcxyz123",
  "event_type": "cpa_conversion",
  "timestamp": "2025-11-14T18:25:00Z",
  "platform_id": "openai_chat",
  "session_id": "sess_001",
  "user_id": "user_hash_abc123",
  "geo": "US",
  "device_type": "desktop",
  "conversion_type": "signup",
  "conversion_value_cents": 0,
  "conversion_window_hours": 168,
  "auth": {
    "nonce": "nonce_conversion_123",
    "sig": "sig_conversion_456"
  }
}
```

---

## 8. Ledger Record

**Schema:** [`ledger-record.json`](../schemas/ledger-record.json)

Records all financial transactions for billing and reconciliation.

```json
{
  "ledger_id": "ledger_001",
  "timestamp": "2025-11-14T18:22:05Z",
  "transaction_type": "debit",
  "amount_cents": 5,
  "currency": "USD",
  "entity_type": "brand_agent",
  "entity_id": "brand_agent_123",
  "wallet_id": "wallet_890",
  "context_id": "ctx_92f",
  "bid_id": "bid_7823",
  "serve_token": "stk_abcxyz123",
  "event_type": "cpx_exposure",
  "event_id": "evt_cpx_001",
  "description": "CPX exposure charge for auction auc_981",
  "metadata": {
    "platform_id": "openai_chat",
    "session_id": "sess_001"
  }
}
```

---

## 9. Wallet Record

**Schema:** [`wallet-record.json`](../schemas/wallet-record.json)

Tracks wallet balances and transactions for brand agents.

```json
{
  "wallet_id": "wallet_890",
  "brand_agent_id": "brand_agent_123",
  "balance_cents": 995,
  "currency": "USD",
  "last_transaction_at": "2025-11-14T18:22:05Z",
  "last_transaction_id": "ledger_001",
  "created_at": "2025-11-01T00:00:00Z",
  "updated_at": "2025-11-14T18:22:05Z",
  "metadata": {
    "status": "active",
    "auto_recharge": true
  }
}
```

---

## Complete Flow Diagram

```
┌─────────────────┐
│  AI Platform    │
│  (OpenAI, etc.) │
└────────┬────────┘
         │
         │ 1. PlatformRequest
         │    (request_id, query_text, locale, geo, cpx_floor)
         │
         ▼
┌─────────────────┐
│    Operator     │
│  (AdMesh, etc.) │
└────────┬────────┘
         │
         │ 2. ContextRequest
         │    (context_id, intent, verticals, allowed_formats)
         │
         ▼
┌─────────────────┐
│  Brand Agents   │
│  (Nimbus, etc.) │
└────────┬────────┘
         │
         │ 3. Bid
         │    (bid_id, pricing, offer.creative_input)
         │
         ▼
┌─────────────────┐
│    Operator     │
│  (Selects winner│
│   & generates   │
│    creative)    │
└────────┬────────┘
         │
         │ 4. AuctionResult
         │    (auction_id, serve_token, winner, render)
         │
         ▼
┌─────────────────┐
│  AI Platform    │
│  (Displays ad)  │
└────────┬────────┘
         │
         │ 5. Events
         │    (CPX exposure → CPC click → CPA conversion)
         │
         ▼
┌─────────────────┐
│    Operator      │
│  (Processes     │
│   events &      │
│   updates       │
│   ledger/wallet)│
└─────────────────┘
```

---

## Schema Relationships

| Schema | Used In | Purpose |
|--------|---------|---------|
| `platform-request.json` | AI Platform → Operator | Initial auction request |
| `context-request.json` | Operator → Brand Agents | Normalized request with intent |
| `creative-input.json` | Part of `bid.json` | Unified creative structure |
| `bid.json` | Brand Agents → Operator | Bid submission with pricing |
| `creative.json` | Part of `auction-result.json` | Format-specific creative |
| `auction-result.json` | Operator → AI Platform | Winning bid response |
| `event-cpx-exposure.json` | AI Platform → Operator | Exposure tracking |
| `event-cpc-click.json` | AI Platform → Operator | Click tracking |
| `event-cpa-conversion.json` | AI Platform → Operator | Conversion tracking |
| `ledger-record.json` | Operator internal | Financial transactions |
| `wallet-record.json` | Operator internal | Wallet balance tracking |

---

## Key Identifiers Flow

```
request_id (PlatformRequest)
    ↓
context_id (ContextRequest) ← maps to request_id
    ↓
bid_id (Bid) ← references context_id
    ↓
auction_id (AuctionResult) ← references context_id
    ↓
serve_token (AuctionResult) ← used in all events
    ↓
event_id (Events) ← references serve_token
    ↓
ledger_id (LedgerRecord) ← references event_id, bid_id, context_id
```

---

## Common Patterns

### Authentication
All requests include an `auth` object with:
- `nonce`: One-time nonce for replay protection
- `sig` or `signature`: HMAC signature of the request

### Timestamps
All timestamps use ISO 8601 / RFC 3339 format:
- Format: `YYYY-MM-DDTHH:mm:ssZ`
- Example: `2025-11-14T18:22:00Z`

### Money/Currency
- Prices in `pricing` object: Decimal strings (e.g., `"0.05"`)
- Amounts in events/ledger: Integer cents (e.g., `5` for $0.05)
- Currency: ISO 4217 code (e.g., `"USD"`)

### IDs
- Platform-generated: `req_*`, `sess_*`, `user_*`
- Operator-generated: `ctx_*`, `auc_*`, `stk_*`
- Brand Agent-generated: `bid_*`
- Event-generated: `evt_*`
- System-generated: `ledger_*`, `wallet_*`

---

## Next Steps

- See individual schema documentation for detailed field descriptions
- Review [Auction Flow](./04-auction.md) for auction mechanics
- Review [Events and States](./05-events-and-states.md) for event lifecycle
- Review [Wallets and Payouts](./06-wallets-and-payouts.md) for billing details

