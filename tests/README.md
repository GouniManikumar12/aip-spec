Run the conformance suite from the repo root:

```bash
npm test
```

The suite:

- checks that every schema listed in `tests/conformance-manifest.json` is valid
- validates all files in `examples/`
- validates all files in `tests/valid/`
- confirms all files in `tests/invalid/` fail validation

The runner writes a JSON report to:

```text
tests/conformance-results.json
```
