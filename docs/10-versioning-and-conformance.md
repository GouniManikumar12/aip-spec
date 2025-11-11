# 10 · Versioning & Conformance

All payloads carry `spec_version`. Breaking changes increment the major component and require a new conformance suite. Minor changes must remain backward compatible and include migration notes.

Conformance is demonstrated by running the JSON fixtures in `tests/` against the schemas in `schemas/`, then submitting attestations back to the AMXP governance group.
