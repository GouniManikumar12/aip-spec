---
layout: default
title: AIP Specification
---

# AIP Spec

AIP is an open protocol for intent monetization in AI and agentic environments.
This repository hosts the public specification, JSON Schemas, examples, and conformance tests.

## Quick Links

- 📖 [Documentation](docs/) - Complete specification chapters
- 🔧 [Schemas](schemas/) - JSON schemas for protocol entities
- 💡 [Examples](examples/) - Real-world payload examples
- ✅ [Conformance](CONFORMANCE) - Certification requirements
- 📋 [PRD](PRD) - Product Requirements Document
- 🔒 [Security](SECURITY) - Security policy

## What is AIP?

The **Agentic Intent Protocol (AIP)** is an open standard for monetizing user intent in AI-powered and agentic environments. It enables:

- **Platforms** to monetize AI conversations and agent interactions
- **Advertisers** to reach users at the moment of intent
- **Ad Networks** to operate compliant, interoperable marketplaces

## Key Features

- ✅ **Real-time Bidding** - Sub-100ms auction mechanics
- ✅ **Event Tracking** - CPX (exposure), CPC (click), CPA (conversion)
- ✅ **Fraud Prevention** - HMAC signatures, nonce validation, trust scoring
- ✅ **Privacy-First** - GDPR/CCPA compliant, no PII required
- ✅ **Interoperable** - Any network can implement AIP

## Documentation

### Core Specification

1. [Overview](docs/01-overview) - Protocol introduction
2. [Roles](docs/02-roles) - Platform, Advertiser, Network
3. [Transport & Auth](docs/03-transport-and-auth) - HTTP/REST, API keys
4. [Auction](docs/04-auction) - Real-time bidding mechanics
5. [Events & States](docs/05-events-and-states) - Tracking lifecycle
6. [Wallets & Payouts](docs/06-wallets-and-payouts) - Financial operations
7. [Security & Fraud](docs/07-security-and-fraud) - Protection measures
8. [Observability](docs/08-observability) - Monitoring and logging
9. [Compliance](docs/09-compliance) - Privacy and legal
10. [Versioning & Conformance](docs/10-versioning-and-conformance) - Version management

### Governance

- [CONFORMANCE](CONFORMANCE) - Certification process
- [GOVERNANCE](GOVERNANCE) - Decision-making
- [SECURITY](SECURITY) - Security policy
- [VERSIONING](VERSIONING) - Version strategy
- [CONTRIBUTING](CONTRIBUTING) - How to contribute
- [CODE_OF_CONDUCT](CODE_OF_CONDUCT) - Community standards

## Schemas

AIP defines JSON schemas for all protocol entities:

- [Context Request](schemas/context-request.json) - Platform request for recommendations
- [Bid](schemas/bid.json) - Advertiser bid submission
- [Auction Result](schemas/auction-result.json) - Network auction decision
- [CPX Exposure Event](schemas/event-cpx-exposure.json) - Impression tracking
- [CPC Click Event](schemas/event-cpc-click.json) - Click tracking
- [CPA Conversion Event](schemas/event-cpa-conversion.json) - Conversion tracking
- [Ledger Record](schemas/ledger-record.json) - Financial ledger entry

## Examples

See the [examples/](examples/) directory for real-world payload examples:

- Context requests with user intent
- Bid submissions with pricing
- Event tracking payloads
- Ledger records

## Conformance Testing

The [tests/](tests/) directory contains:

- **Valid test cases** - Passing examples
- **Invalid test cases** - Failing examples
- **Conformance manifest** - Test suite definition

## Quick Start

```bash
# Clone the repository
git clone https://github.com/GouniManikumar12/aip-spec.git
cd aip-spec

# Install dependencies
npm ci

# Run conformance tests
npm test

# Read the specification
open docs/01-overview.md
```

## Reference Implementation

The **AdMesh Ad Network** is the reference implementation of AIP. Any ad network can implement AIP and claim compatibility after passing the conformance suite.

## Certification

To become **"AIP Compatible"**:

1. Implement the specification
2. Pass the conformance test suite
3. Meet performance SLOs (p95 < 100ms)
4. Complete security audit
5. Submit certification application

See [CONFORMANCE.md](CONFORMANCE) for details.

## License

Dual-licensed under:
- Apache License 2.0
- MIT License

See [LICENSE](LICENSE) for full text.

## Community

- **GitHub**: [github.com/GouniManikumar12/aip-spec](https://github.com/GouniManikumar12/aip-spec)
- **Issues**: [Report bugs or request features](https://github.com/GouniManikumar12/aip-spec/issues)
- **Discussions**: [Join the conversation](https://github.com/GouniManikumar12/aip-spec/discussions)

## Version

**Current Version**: v0.1.0  
**Status**: Public Specification  
**Last Updated**: 2025-11-11

---

**AIP** - The intent monetization layer for the agent economy.

