# 03 · Transport & Authentication

This chapter defines the normative transport and request-authentication rules for AIP message exchange.

## 1. Transport requirements

All AIP HTTP endpoints:

- MUST use HTTPS
- MUST require TLS 1.3 or better
- MUST reject plaintext HTTP
- MUST return UTF-8 JSON bodies

The protocol standardizes payloads and signing behavior, not a single global endpoint layout. Parties may choose their own endpoint paths, but they MUST document them clearly.

## 2. Required request metadata

Every signed AIP request MUST include:

- `Authorization`
- `Content-Digest`
- `X-AIP-Timestamp`
- `X-AIP-Nonce`
- `Content-Type: application/json`

### `Authorization`

Format:

```text
Authorization: AIP-HMAC keyId="<key-id>", algorithm="hmac-sha256", headers="@method @path content-digest x-aip-timestamp x-aip-nonce", signature="<base64url-signature>"
```

Rules:

- `keyId` identifies the shared secret used to verify the signature
- `algorithm` MUST be `hmac-sha256`
- `headers` MUST list the covered components in the exact order shown above
- `signature` MUST be an unpadded base64url-encoded HMAC-SHA256 output

### `Content-Digest`

Format:

```text
Content-Digest: sha-256=:<base64-standard-sha256-of-raw-body-bytes>:
```

Rules:

- the digest MUST be computed over the exact raw request body bytes
- receivers MUST verify the digest before verifying the signature

### `X-AIP-Timestamp`

Format:

```text
X-AIP-Timestamp: 2026-03-27T18:22:00Z
```

Rules:

- MUST be RFC 3339 in UTC
- receivers MUST reject timestamps more than 120 seconds away from server time

### `X-AIP-Nonce`

Rules:

- MUST be unique per signed request
- SHOULD be at least 16 bytes of entropy after encoding
- receivers MUST treat a repeated nonce within the replay window as a replay attempt

## 3. Canonical signing string

The signature input MUST be the UTF-8 encoding of the following canonical string, with newline separators and no trailing newline:

```text
@method: <lowercase-http-method>
@path: <path-and-query-as-sent>
content-digest: <exact Content-Digest header value>
x-aip-timestamp: <exact X-AIP-Timestamp header value>
x-aip-nonce: <exact X-AIP-Nonce header value>
```

Example:

```text
@method: post
@path: /v1/context
content-digest: sha-256=:m4w7mB0gq9T4qkzJm8Z0v9zM6k3uW7mM+8nW0mQ8n8E=:
x-aip-timestamp: 2026-03-27T18:22:00Z
x-aip-nonce: 4f7e2e90f28f4aa69e0f1a1c0a9cb6d2
```

The HMAC key is then applied to that canonical string with SHA-256.

## 4. Verification order

Receivers MUST verify signed requests in this order:

1. confirm TLS and `Content-Type`
2. parse and validate required authentication headers
3. validate timestamp window
4. validate nonce freshness
5. validate `Content-Digest`
6. reconstruct canonical signing string
7. verify HMAC signature using the secret identified by `keyId`
8. only then parse and process the AIP payload semantically

If any step fails, the request MUST be rejected before protocol processing.

## 5. Replay protection

Receivers MUST implement replay protection per `keyId`.

Minimum rules:

- maintain a nonce cache for at least 10 minutes
- reject any request reusing the same nonce within that cache window
- reject any request whose timestamp is outside the 120-second drift window
- bind replay checks to both `keyId` and nonce

Recommended:

- also bind replay detection to the request digest
- log replay attempts with client identity, timestamp, and source IP

## 6. Key management and discovery

Shared HMAC secrets MUST be exchanged out of band over a secure channel.

Each party that accepts AIP-signed requests MUST expose key metadata through one of these mechanisms:

1. a bilateral configuration channel, or
2. `/.well-known/aip-auth.json`

If `/.well-known/aip-auth.json` is used, it SHOULD expose:

- `issuer`
- `supported_schemes`
- `keys`

Each key metadata object SHOULD include:

- `key_id`
- `algorithm`
- `status`
- `created_at`
- `expires_at`
- `operations`

The discovery document MUST NOT expose secret material.

Minimum key-management rules:

- `keyId` values MUST be unique per issuer
- secrets MUST be rotatable without downtime
- compromised keys MUST be revocable immediately
- long-lived shared secrets SHOULD rotate at least every 90 days

## 7. Error handling

Receivers SHOULD return these status codes and machine-readable error codes:

| HTTP | Code | Meaning |
| --- | --- | --- |
| `400` | `AIP_AUTH_MALFORMED` | Missing or malformed auth header fields |
| `400` | `AIP_DIGEST_INVALID` | `Content-Digest` missing or malformed |
| `401` | `AIP_AUTH_REQUIRED` | Signed auth required but absent |
| `401` | `AIP_KEY_UNKNOWN` | `keyId` is unknown or revoked |
| `401` | `AIP_SIGNATURE_INVALID` | HMAC verification failed |
| `401` | `AIP_TIMESTAMP_DRIFT` | Timestamp outside allowed drift window |
| `401` | `AIP_NONCE_REPLAY` | Nonce was already used within replay window |
| `403` | `AIP_OPERATION_FORBIDDEN` | Key is not authorized for the target operation |
| `415` | `AIP_CONTENT_TYPE_UNSUPPORTED` | Payload is not JSON |
| `422` | `AIP_SCHEMA_INVALID` | Payload failed schema validation |

Recommended response shape:

```json
{
  "error": {
    "code": "AIP_SIGNATURE_INVALID",
    "message": "Signature verification failed."
  }
}
```

## 8. Publish/subscribe transport

The asynchronous auction fanout may use a message bus rather than direct HTTP fanout.

Operators may use Google Pub/Sub, SNS/SQS, Event Grid, Kafka, or similar infrastructure, provided that the transport:

- preserves authenticated publisher identity
- preserves message integrity
- supports delivery within the auction window
- supports per-pool authorization boundaries

If the message bus is not directly signed using the HTTP rules above, the Operator MUST provide equivalent integrity and publisher-authentication guarantees for `ContextRequest` distribution.
