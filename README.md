# Agentic Intent Protocol (AIP) Specification

**Version:** 0.1.0
**Status:** Public Specification
**Last Updated:** 2025-11-13

---

## Overview

The **Agentic Intent Protocol (AIP)** is an open standard for intent monetization in AI-powered and agentic environments. AIP enables platforms, advertisers, and ad networks to participate in a transparent, performance-based advertising ecosystem designed specifically for conversational AI and autonomous agents.

This repository contains the **formal protocol specification**, including:

- **JSON Schemas** - Formal definitions for all protocol entities
- **Documentation** - Complete technical specification across 10 chapters
- **Examples** - Reference implementations of protocol messages
- **Conformance Tests** - Validation suite for protocol compliance

📖 **Full Documentation:** [https://aip.mintlify.app](https://aip.mintlify.app)

---

## Why AIP?

Traditional advertising protocols (OpenRTB, VAST, etc.) were designed for web pages and mobile apps. AIP is purpose-built for:

- **AI Conversations** - Monetize intent expressed in natural language
- **Agentic Environments** - Support autonomous agents making decisions
- **Performance-Based Billing** - Progressive pricing (CPX → CPC → CPA)
- **Transparent Attribution** - Verifiable event tracking and billing

---

## Protocol Features

### Core Capabilities

- ✅ **Real-Time Bidding** - Sub-100ms auction mechanics for contextual recommendations
- ✅ **Progressive Billing** - Three-tier pricing model (CPX, CPC, CPA) with single-charge settlement
- ✅ **Event Verification** - Signed, timestamped events for exposure, click, and conversion tracking
- ✅ **Fraud Prevention** - HMAC signatures, nonce validation, and trust scoring
- ✅ **Privacy-First** - GDPR/CCPA compliant, no PII required for basic operations
- ✅ **Interoperable** - Open standard that any network can implement

### Event Types

| Event Type | Event Name | Trigger | Billing Unit |
|------------|------------|---------|--------------|
| **Exposure** | `cpx_exposure` | User sees an ad or recommendation | Cost per Exposure (CPX) |
| **Click** | `cpc_click` | User clicks or engages with ad | Cost per Click (CPC) |
| **Conversion** | `cpa_conversion` | User completes purchase/signup | Cost per Action (CPA) |

### State Machine

Ledger records transition through states: `PENDING` → `EXPOSED` → `CLICKED` → `CONVERTED` → `FINALIZED`

Only the highest-value event is charged per `serve_token`.

---

## Repository Structure

```
aip-spec/
├── schemas/              # JSON Schema definitions (Draft 2020-12)
│   ├── context-request.json
│   ├── bid.json
│   ├── auction-result.json
│   ├── event-cpx-exposure.json
│   ├── event-cpc-click.json
│   ├── event-cpa-conversion.json
│   ├── ledger-record.json
│   └── common.json
├── examples/             # Reference payload examples
│   ├── context-request.example.json
│   ├── bid.example.json
│   ├── auction-result.example.json
│   ├── event-cpx-exposure.example.json
│   ├── event-cpc-click.example.json
│   ├── event-cpa-conversion.example.json
│   └── ledger-record.example.json
├── docs/                 # Technical specification (10 chapters)
│   ├── 01-overview.md
│   ├── 02-roles.md
│   ├── 03-transport-and-auth.md
│   ├── 04-auction.md
│   ├── 05-events-and-states.md
│   ├── 06-wallets-and-payouts.md
│   ├── 07-security-and-fraud.md
│   ├── 08-observability.md
│   ├── 09-compliance.md
│   └── 10-versioning-and-conformance.md
├── tests/                # Conformance test suite
│   ├── valid/           # Valid test cases
│   ├── invalid/         # Invalid test cases
│   └── conformance-manifest.json
├── CONFORMANCE.md        # Certification requirements
├── GOVERNANCE.md         # Protocol governance
├── SECURITY.md           # Security policy
├── VERSIONING.md         # Version strategy
├── CONTRIBUTING.md       # Contribution guidelines
├── CODE_OF_CONDUCT.md   # Community standards
├── CHANGELOG.md          # Version history
└── LICENSE               # CC BY 4.0 license
```

---

## Quick Start

### 1. Explore the Schemas

All protocol entities are defined using [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema):

```bash
# View the CPX exposure event schema
cat schemas/event-cpx-exposure.json

# View the auction result schema
cat schemas/auction-result.json
```

Each schema includes:
- `$id` - Canonical URI for the schema
- `$schema` - JSON Schema version
- `required` - Required fields
- `properties` - Field definitions with types, descriptions, and examples
- `examples` - Complete example payloads

### 2. Validate Against Schemas

```bash
# Install dependencies
npm ci

# Run conformance tests (validates all examples against schemas)
npm test
```

### 3. Read the Specification

Start with the documentation chapters in order:

1. **[Overview](docs/01-overview.md)** - Protocol introduction and key concepts
2. **[Roles](docs/02-roles.md)** - Platform, Advertiser, Network responsibilities
3. **[Transport & Auth](docs/03-transport-and-auth.md)** - HTTP/REST and authentication
4. **[Auction](docs/04-auction.md)** - Real-time bidding mechanics
5. **[Events & States](docs/05-events-and-states.md)** - Event tracking lifecycle
6. **[Wallets & Payouts](docs/06-wallets-and-payouts.md)** - Financial operations
7. **[Security & Fraud](docs/07-security-and-fraud.md)** - Protection measures
8. **[Observability](docs/08-observability.md)** - Monitoring and logging
9. **[Compliance](docs/09-compliance.md)** - Privacy and legal requirements
10. **[Versioning & Conformance](docs/10-versioning-and-conformance.md)** - Version management

### 4. Review Examples

See the `examples/` directory for complete, valid payload examples:

```bash
# View a complete auction flow
cat examples/context-request.example.json
cat examples/bid.example.json
cat examples/auction-result.example.json

# View event tracking examples
cat examples/event-cpx-exposure.example.json
cat examples/event-cpc-click.example.json
cat examples/event-cpa-conversion.example.json

# View final ledger record
cat examples/ledger-record.example.json
```

---

## Documentation

### Primary Documentation Site

📖 **[https://aip.mintlify.app](https://aip.mintlify.app)** - Complete implementation guides, tutorials, and API reference

The Mintlify documentation site provides:
- **Getting Started Guides** - Quick integration tutorials
- **Platform Integration** - How to integrate AIP into your platform
- **Advertiser Guides** - How to participate as an advertiser
- **API Reference** - Complete endpoint documentation
- **Schema Reference** - Interactive schema explorer
- **Best Practices** - Implementation patterns and recommendations

### Specification Repository (This Repo)

This repository contains the **formal protocol specification**:
- **Authoritative Schemas** - JSON Schema definitions (source of truth)
- **Technical Specification** - Detailed protocol documentation
- **Conformance Tests** - Validation suite for compliance
- **Governance Documents** - Protocol evolution and decision-making

**Relationship:**
- **This repo** = Formal specification and schemas
- **aip.mintlify.app** = Implementation guides and developer documentation

---

## Conformance & Certification

To become **"AIP Compatible"**, implementations must:

1. ✅ **Implement Core Schemas** - Support all required protocol entities
2. ✅ **Pass Conformance Tests** - Validate against the test suite in `tests/`
3. ✅ **Meet Performance SLOs** - p95 auction latency < 100ms
4. ✅ **Security Audit** - Complete security review
5. ✅ **Submit Certification** - Apply for official certification

See **[CONFORMANCE.md](CONFORMANCE.md)** for detailed requirements.

---

## Reference Implementation

The **AdMesh Ad Network** serves as the reference implementation of AIP. The implementation demonstrates:

- Complete auction mechanics
- Event tracking and verification
- Wallet and payout operations
- Fraud prevention measures
- Privacy-compliant data handling

Any ad network can implement AIP and claim compatibility after passing the conformance suite.

---

## Contributing

We welcome contributions to the AIP specification! Please see:

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards
- **[GOVERNANCE.md](GOVERNANCE.md)** - Decision-making process

### How to Contribute

1. **Report Issues** - [Open an issue](https://github.com/admesh/aip-spec/issues) for bugs or feature requests
2. **Propose Changes** - Submit pull requests with schema or documentation improvements
3. **Join Discussions** - Participate in protocol evolution discussions
4. **Implement & Test** - Build implementations and share feedback

---

## Versioning

AIP follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** - Incompatible API changes
- **MINOR** - Backward-compatible functionality additions
- **PATCH** - Backward-compatible bug fixes

**Current Version:** 0.1.0 (Initial Public Specification)

See **[VERSIONING.md](VERSIONING.md)** for the complete version strategy and **[CHANGELOG.md](CHANGELOG.md)** for version history.

---

## Security

Security is a top priority for AIP. The protocol includes:

- **HMAC Signatures** - Request/response authentication
- **Nonce Validation** - Replay attack prevention
- **Trust Scoring** - Fraud detection and prevention
- **Privacy Controls** - GDPR/CCPA compliance

To report security vulnerabilities, please see **[SECURITY.md](SECURITY.md)**.

---

## License

AIP is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You are free to share and adapt this specification for any purpose, even commercially, as long as you provide appropriate attribution. See **[LICENSE](LICENSE)** for full text.

---

## Community & Support

- **Documentation:** [https://aip.mintlify.app](https://aip.mintlify.app)
- **GitHub:** [github.com/admesh/aip-spec](https://github.com/admesh/aip-spec)
- **Issues:** [Report bugs or request features](https://github.com/admesh/aip-spec/issues)
- **Discussions:** [Join the conversation](https://github.com/admesh/aip-spec/discussions)

---

## Acknowledgments

AIP is developed and maintained by the AdMesh team with contributions from the open-source community. Special thanks to all contributors who have helped shape this protocol.

---

**AIP** - The intent monetization layer for the agent economy.
