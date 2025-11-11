# 08 · Observability

Operators must emit structured telemetry for every API call, auction, and settlement. The specification defines
common dimensions (such as `request_id`, `auction_id`, `bid_id`, `publisher_id`) to make correlation straightforward.

Recommended practices include redaction-by-default, separate PII handling pipelines, and dedicated audit feeds for regulators.
