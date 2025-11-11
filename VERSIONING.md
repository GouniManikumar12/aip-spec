# Versioning

AMXP uses semver:
- MAJOR: breaking schema changes
- MINOR: additive schema fields
- PATCH: fixes that do not change validation

Implementations must advertise exact supported versions with `X-AMXP-Version`.

