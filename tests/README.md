# AMXP Conformance Fixtures

The `tests/` directory includes canonical samples that integrators can replay when validating their implementations. Files are intentionally small and self-describing so they can be used with any JSON Schema validator.

## Structure
- `valid/` contains payloads that MUST validate against their respective schemas.
- `invalid/` contains payloads that MUST fail validation.
- `conformance-manifest.json` links each case to the schema it targets.

## Usage
```bash
npm install
npm test
```
(Replace the placeholder `npm test` script with your validation logic.)
