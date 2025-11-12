# AIP Conformance & Certification

This document defines the requirements for obtaining **"AIP Compatible"** certification.

## Table of Contents

1. [Overview](#overview)
2. [Certification Requirements](#certification-requirements)
3. [Conformance Test Suite](#conformance-test-suite)
4. [Performance Requirements](#performance-requirements)
5. [Security Requirements](#security-requirements)
6. [Documentation Requirements](#documentation-requirements)
7. [Certification Process](#certification-process)
8. [Maintenance & Renewal](#maintenance--renewal)

---

## Overview

### What is AIP Certification?

**"AIP Compatible"** certification verifies that an ad network correctly implements the Agentic Intent Protocol (AIP) v0.1 specification.

### Benefits of Certification

**For Networks:**
- Listed on admesh.network/certified-networks
- Use "AIP Compatible" badge in marketing
- Access to AIP developer community
- Technical support from AdMesh team

**For Platforms & Advertisers:**
- Confidence in network compliance
- Guaranteed interoperability
- Consistent API behavior
- Verified security standards

---

## Certification Requirements

To obtain AIP Compatible certification, networks must meet ALL of the following requirements:

### 1. Schema Validation

✅ **Requirement:** Support JSON payloads that validate against all base schemas in `schemas/`.

**Schemas to Support:**
- `ContextRequest.json` - Context request payload
- `ContextResponse.json` - Auction result with recommendation
- `Event.json` - Event tracking payload (exposure, click, conversion)
- `Campaign.json` - Campaign creation payload
- `WalletBalance.json` - Wallet balance response
- `PayoutRequest.json` - Payout request payload
- `LedgerRecord.json` - Ledger entry format

**Validation:**
- All request payloads must validate against schemas
- All response payloads must validate against schemas
- Invalid payloads must return appropriate error codes

### 2. Conformance Test Suite

✅ **Requirement:** Pass the conformance suite with 100% success rate.

**Test Categories:**
- **Valid Tests:** All files in `tests/valid/` must validate and process correctly
- **Invalid Tests:** All files in `tests/invalid/` must fail validation with appropriate errors
- **State Machine Tests:** Event state transitions must follow specification
- **Time Window Tests:** Event windows must be enforced correctly
- **Billing Tests:** Only one billing unit charged per serve_token

**Run Tests:**
```bash
npm install
npm test
```

**Expected Output:**
```
✓ Schema validation (7/7 schemas)
✓ Valid payloads (25/25 tests)
✓ Invalid payloads (15/15 tests)
✓ State machine (10/10 tests)
✓ Time windows (8/8 tests)
✓ Billing logic (12/12 tests)

Total: 77/77 tests passed (100%)
```

### 3. Event State Rules

✅ **Requirement:** Implement event state machine correctly.

**Rules:**
1. **Single Settlement:** Only one final settlement per `serve_token`
2. **Billing Priority:** CPA > CPC > CPX (highest value wins)
3. **Time Windows:** Enforce 30-min (CPX→CPC) and 24h/7d (CPC→CPA) windows
4. **State Transitions:** Follow state machine diagram (see PRD.md Section 8)
5. **Wallet Operations:** Reserve → Release → Capture correctly

**Example:**
```
serve_token: st_abc123

Exposure event → CPX reserved ($1.50)
Click event (within 30 min) → CPX released, CPC reserved ($5.00)
Conversion event (within 24h) → CPC released, CPA captured ($50.00)

Final charge: $50.00 (CPA only, not CPX or CPC)
```

### 4. API Endpoints

✅ **Requirement:** Implement all required API endpoints.

**Required Endpoints:**
- `POST /v1/context` - Context request and auction
- `POST /v1/events` - Event tracking
- `GET /v1/wallet/balance` - Wallet balance query
- `POST /v1/wallet/fund` - Wallet funding
- `POST /v1/payouts/request` - Platform payout request
- `GET /v1/payouts/history` - Payout history
- `POST /v1/campaigns` - Campaign creation
- `GET /v1/campaigns/{id}` - Campaign details
- `PATCH /v1/campaigns/{id}` - Campaign updates

**Version Header:**
All endpoints must support:
```
X-AIP-Version: 0.1
```

### 5. Performance SLOs

✅ **Requirement:** Meet or exceed all Service Level Objectives.

| Metric | Target | Measurement Period |
|--------|--------|-------------------|
| Auction Latency | ≤20ms (p95) | 30 days |
| Event Ingest Latency | ≤50ms (p95) | 30 days |
| API Uptime | ≥99.9% | 30 days |
| Duplicate Event Rate | <0.01% | 30 days |
| Wallet Error Rate | <1% | 30 days |

**Monitoring:**
- Provide Prometheus/Grafana dashboard
- Share SLO metrics with certification team
- Alert on SLO violations

### 6. Security Implementation

✅ **Requirement:** Implement all security measures.

**Required Security Controls:**
- HTTPS/TLS 1.3+ for all endpoints
- API key authentication (pk_*, ak_* format)
- HMAC-SHA256 signature validation on events
- Nonce validation (60-second TTL)
- Rate limiting (per API key and per IP)
- Trust scoring (0.0-1.0 range)

**Optional (Recommended):**
- Mutual TLS (mTLS)
- IP allowlisting
- Anomaly detection
- Fraud scoring

### 7. Documentation

✅ **Requirement:** Publish comprehensive API documentation.

**Required Documentation:**
- API reference (all endpoints with examples)
- Authentication guide
- Integration guide for platforms
- Integration guide for advertisers
- Error code reference
- Changelog

**Format:** OpenAPI 3.0 specification + human-readable docs

**Example:** https://docs.your-network.com/aip/v1

### 8. SDK Support

✅ **Requirement:** Provide SDKs for at least 2 languages.

**Minimum Languages:**
- JavaScript/TypeScript (Node.js)
- Python 3.8+

**SDK Features:**
- Context request wrapper
- Event tracking with automatic HMAC signing
- Wallet management
- Campaign management
- Error handling

**Optional Languages:**
- Go
- Ruby
- Java
- PHP

---

## Conformance Test Suite

### Installation

```bash
git clone https://github.com/admesh/aip-spec.git
cd aip-spec
npm install
```

### Configuration

Create `.env` file:
```bash
AIP_BASE_URL=https://api.your-network.com/v1
AIP_PLATFORM_KEY=pk_test_your_key
AIP_AGENT_KEY=ak_test_your_key
```

### Running Tests

**Full Suite:**
```bash
npm test
```

**Specific Category:**
```bash
npm test -- --grep "schema validation"
npm test -- --grep "state machine"
npm test -- --grep "time windows"
```

**Generate Report:**
```bash
npm test -- --reporter json > conformance-report.json
```

### Test Categories

#### 1. Schema Validation (7 tests)
- ✅ ContextRequest validates
- ✅ ContextResponse validates
- ✅ Event (exposure) validates
- ✅ Event (click) validates
- ✅ Event (conversion) validates
- ✅ Campaign validates
- ✅ LedgerRecord validates

#### 2. Valid Payloads (25 tests)
- ✅ Context request with all fields
- ✅ Context request with minimal fields
- ✅ Exposure event with valid HMAC
- ✅ Click event within 30-min window
- ✅ Conversion event within 24h window
- ✅ Conversion event within 7d fallback window
- ✅ Campaign with all billing units
- ✅ Wallet funding with valid payment method
- ... (18 more tests)

#### 3. Invalid Payloads (15 tests)
- ❌ Context request missing required field
- ❌ Event with invalid HMAC signature
- ❌ Event with reused nonce
- ❌ Click event outside 30-min window
- ❌ Conversion event outside 7d window
- ❌ Duplicate event (same serve_token + type)
- ❌ Campaign with negative bid
- ❌ Wallet funding with insufficient amount
- ... (7 more tests)

#### 4. State Machine (10 tests)
- ✅ AUCTION_WON → EXPOSURE_PENDING
- ✅ EXPOSURE_PENDING → CLICK_PENDING (within window)
- ✅ EXPOSURE_PENDING → FINALIZED (timeout)
- ✅ CLICK_PENDING → CONVERSION_PENDING (within window)
- ✅ CLICK_PENDING → FINALIZED (timeout)
- ✅ CONVERSION_PENDING → FINALIZED (verified)
- ✅ Invalid state transition rejected
- ✅ Duplicate state transition rejected
- ✅ Out-of-order events rejected
- ✅ Final state immutable

#### 5. Time Windows (8 tests)
- ✅ Click within 30 min accepted
- ❌ Click at 31 min rejected
- ✅ Conversion within 24h (primary window)
- ✅ Conversion at 25h (fallback window)
- ❌ Conversion at 8 days rejected
- ✅ Multiple events within windows
- ✅ Timestamp validation (±60s tolerance)
- ❌ Future timestamp rejected

#### 6. Billing Logic (12 tests)
- ✅ CPX charged when no click/conversion
- ✅ CPC charged when click but no conversion
- ✅ CPA charged when conversion occurs
- ✅ Only one billing unit charged per serve_token
- ✅ Second-price CPX auction
- ✅ Wallet reservation on auction win
- ✅ Wallet release on higher-priority event
- ✅ Wallet capture on finalization
- ✅ Revenue split (70/30) calculated correctly
- ✅ Insufficient balance prevents auction participation
- ✅ Low balance alert triggered
- ✅ Payout eligibility (≥7 days, ≥$50)

---

## Performance Requirements

### Load Testing

**Requirement:** Network must handle production-level load.

**Test Scenarios:**

1. **Sustained Load:**
   - 1,000 context requests/second
   - 10,000 event tracking requests/second
   - Duration: 1 hour
   - p95 latency: ≤20ms (context), ≤50ms (events)

2. **Burst Load:**
   - 5,000 context requests/second
   - 50,000 event tracking requests/second
   - Duration: 5 minutes
   - p95 latency: ≤30ms (context), ≤75ms (events)

3. **Concurrent Auctions:**
   - 10,000 simultaneous auctions
   - 100 eligible advertisers per auction
   - p95 latency: ≤20ms

**Tools:**
- Apache JMeter
- k6
- Gatling

**Report:**
Submit load test report showing:
- Request rate over time
- Latency percentiles (p50, p95, p99)
- Error rate
- Resource utilization (CPU, memory, network)

---

## Security Requirements

### Security Audit

**Requirement:** Complete third-party security audit.

**Scope:**
- API endpoint security
- Authentication & authorization
- HMAC signature validation
- Nonce management
- Rate limiting
- SQL injection prevention
- XSS prevention
- CSRF protection

**Deliverable:** Security audit report from recognized firm

### Penetration Testing

**Requirement:** Pass penetration testing.

**Test Areas:**
- API authentication bypass
- HMAC signature forgery
- Nonce replay attacks
- Rate limit bypass
- SQL injection
- Event fraud (fake events)
- Wallet manipulation

**Deliverable:** Penetration test report with all critical/high issues resolved

### Vulnerability Disclosure

**Requirement:** Publish security policy.

**Required Information:**
- Security contact email
- Responsible disclosure process
- Expected response time
- Bug bounty program (optional)

**Example:** https://your-network.com/security

---

## Documentation Requirements

### API Documentation

**Requirement:** Publish OpenAPI 3.0 specification.

**Required Sections:**
- Authentication
- All endpoints with request/response examples
- Error codes and messages
- Rate limits
- Versioning

**Example:**
```yaml
openapi: 3.0.0
info:
  title: Your Network AIP API
  version: 0.1.0
  description: AIP v0.1 compatible ad network
servers:
  - url: https://api.your-network.com/v1
paths:
  /context:
    post:
      summary: Request recommendation
      ...
```

### Integration Guides

**Requirement:** Provide step-by-step integration guides.

**For Platforms:**
1. Account setup
2. API key generation
3. SDK installation
4. Context request example
5. Event tracking example
6. Revenue analytics
7. Payout request

**For Advertisers:**
1. Account setup
2. Wallet funding
3. Campaign creation
4. Bid optimization
5. Performance monitoring
6. Webhook setup

---

## Certification Process

### Step 1: Application

**Submit application to:** certification@admesh.network

**Include:**
- Company name and contact
- Base URL for AIP endpoints
- API documentation URL
- SDK repository URLs
- Estimated certification date

**Response time:** 3 business days

### Step 2: Self-Assessment

**Run conformance tests:**
```bash
npm test -- --reporter json > conformance-report.json
```

**Submit:**
- Conformance test report (100% pass rate required)
- Load test report
- Security audit report
- Penetration test report

### Step 3: Technical Review

**AdMesh team reviews:**
- Conformance test results
- API documentation
- SDK quality
- Performance metrics
- Security implementation

**Duration:** 2-4 weeks

**Outcome:** Pass, Conditional Pass (with remediation), or Fail

### Step 4: Production Verification

**AdMesh team tests production environment:**
- Run conformance tests against production API
- Verify SLO metrics
- Test SDK integration
- Review monitoring dashboards

**Duration:** 1 week

### Step 5: Certification Issued

**Upon successful verification:**
- Receive "AIP Compatible v0.1" certification
- Listed on admesh.network/certified-networks
- Receive certification badge for marketing
- Access to AIP developer community

**Certification valid for:** 12 months

---

## Maintenance & Renewal

### Annual Renewal

**Requirement:** Recertify every 12 months.

**Renewal Process:**
1. Submit renewal application
2. Run latest conformance tests
3. Provide updated SLO metrics
4. Confirm security audit is current (<12 months old)
5. Update documentation if needed

**Renewal fee:** None (free)

### Continuous Monitoring

**Requirement:** Maintain SLOs during certification period.

**Monitoring:**
- Monthly SLO reports submitted to AdMesh
- Quarterly performance reviews
- Incident reports for SLO violations

**Consequences of SLO Violations:**
- First violation: Warning
- Second violation: Probation (30 days to remediate)
- Third violation: Certification suspended

### Version Updates

**When AIP specification updates:**
- Networks have 180 days to upgrade
- Dual-stack support during transition
- Recertification required for new version

---

## Contact

**Certification Team:** certification@admesh.network
**Technical Support:** support@admesh.network
**Security Issues:** security@admesh.network

**GitHub:** [github.com/admesh/aip-spec](https://github.com/admesh/aip-spec)
**Discord:** [discord.gg/admesh](https://discord.gg/admesh)

---

**Document Version:** 1.0
**Specification Version:** AIP v0.1
**Last Updated:** 2025-11-11

