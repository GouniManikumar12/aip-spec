# 03 · Transport & Authentication

- All HTTPS endpoints MUST enforce TLS 1.3 with modern cipher suites.
- Requests carry an `Authorization: AMXP-HMAC keyId=...,signature=...` header where the signature covers the canonical JSON body plus critical headers.
- Clock drift of ±2 minutes is tolerated; anything outside that window is rejected with `401 DRIFT`.
- Long-lived credentials must be rotated every 90 days and scoped to the minimal set of operations.
