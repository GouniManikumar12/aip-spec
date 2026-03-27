#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import jsonschema
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
EXAMPLES_DIR = ROOT / "examples"
TESTS_DIR = ROOT / "tests"
MANIFEST_PATH = TESTS_DIR / "conformance-manifest.json"
REPORT_PATH = TESTS_DIR / "conformance-results.json"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_schema_store() -> tuple[dict[str, dict], Registry]:
    schemas: dict[str, dict] = {}
    resources: list[tuple[str, Resource]] = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        schema = load_json(path)
        schemas[path.name] = schema
        resource = Resource.from_contents(schema)
        resources.append((path.resolve().as_uri(), resource))
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resources.append((schema_id, resource))
    return schemas, Registry().with_resources(resources)


def validator_for(schema_name: str, schemas: dict[str, dict], registry: Registry) -> jsonschema.protocols.Validator:
    path = SCHEMAS_DIR / schema_name
    schema = schemas[schema_name]
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(schema, registry=registry)


def infer_schema_name(path: Path) -> str:
    name = path.name
    mapping = {
        "platform-request": "platform-request.json",
        "context-request": "context-request.json",
        "context-": "context-request.json",
        "bid": "bid.json",
        "auction-result": "auction-result.json",
        "auction-": "auction-result.json",
        "creative-input": "creative-input.json",
        "creative.example": "creative.json",
        "event-exposure-shown": "event-exposure-shown.json",
        "exposure-": "event-exposure-shown.json",
        "event-interaction-started": "event-interaction-started.json",
        "interaction-": "event-interaction-started.json",
        "event-delegation-started": "event-delegation-started.json",
        "delegation-started-": "event-delegation-started.json",
        "event-delegation-activity": "event-delegation-activity.json",
        "delegation-activity-": "event-delegation-activity.json",
        "event-delegation-expired": "event-delegation-expired.json",
        "delegation-expired-": "event-delegation-expired.json",
        "event-task-completed": "event-task-completed.json",
        "task-completed-": "event-task-completed.json",
        "ledger-record": "ledger-record.json",
    }
    for prefix, schema_name in mapping.items():
        if name.startswith(prefix):
            return schema_name
    raise KeyError(f"No schema mapping defined for {name}")


def validate_instance(path: Path, expect_valid: bool, schemas: dict[str, dict], registry: Registry) -> tuple[bool, str | None, str]:
    schema_name = infer_schema_name(path)
    validator = validator_for(schema_name, schemas, registry)
    instance = load_json(path)
    try:
        validator.validate(instance)
        if expect_valid:
            return True, None, schema_name
        return False, "Expected validation failure, but payload passed.", schema_name
    except jsonschema.ValidationError as exc:
        if expect_valid:
            location = "$" if not exc.absolute_path else "$." + ".".join(str(p) for p in exc.absolute_path)
            return False, f"{location}: {exc.message}", schema_name
        return True, None, schema_name


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    schemas, registry = build_schema_store()

    results: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
        "categories": defaultdict(dict),
        "failures": [],
    }
    failures: list[dict[str, str]] = []

    schema_passed = 0
    schema_total = 0
    for rel_path in manifest["schemas"]:
        schema_total += 1
        schema_name = Path(rel_path).name
        try:
            validator_for(schema_name, schemas, registry)
            schema_passed += 1
        except Exception as exc:  # noqa: BLE001
            failures.append(
                {
                    "category": "schemas",
                    "path": rel_path,
                    "error": str(exc),
                }
            )

    example_files = sorted(EXAMPLES_DIR.glob("*.json"))
    examples_passed = 0
    for path in example_files:
        ok, error, schema_name = validate_instance(path, True, schemas, registry)
        if ok:
            examples_passed += 1
        else:
            failures.append(
                {
                    "category": "examples",
                    "path": str(path.relative_to(ROOT)),
                    "schema": schema_name,
                    "error": error or "Unknown validation failure",
                }
            )

    valid_passed = 0
    for rel_path in manifest["valid"]:
        path = ROOT / rel_path
        ok, error, schema_name = validate_instance(path, True, schemas, registry)
        if ok:
            valid_passed += 1
        else:
            failures.append(
                {
                    "category": "valid",
                    "path": rel_path,
                    "schema": schema_name,
                    "error": error or "Unknown validation failure",
                }
            )

    invalid_passed = 0
    for rel_path in manifest["invalid"]:
        path = ROOT / rel_path
        ok, error, schema_name = validate_instance(path, False, schemas, registry)
        if ok:
            invalid_passed += 1
        else:
            failures.append(
                {
                    "category": "invalid",
                    "path": rel_path,
                    "schema": schema_name,
                    "error": error or "Unknown validation failure",
                }
            )

    results["categories"] = {
        "schemas": {"passed": schema_passed, "total": schema_total},
        "examples": {"passed": examples_passed, "total": len(example_files)},
        "valid": {"passed": valid_passed, "total": len(manifest["valid"])},
        "invalid": {"passed": invalid_passed, "total": len(manifest["invalid"])},
    }
    results["failures"] = failures
    total_checks = schema_total + len(example_files) + len(manifest["valid"]) + len(manifest["invalid"])
    passed_checks = schema_passed + examples_passed + valid_passed + invalid_passed
    results["summary"] = {
        "passed": passed_checks,
        "total": total_checks,
        "success": not failures,
    }

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")

    print(f"Schemas: {schema_passed}/{schema_total}")
    print(f"Examples: {examples_passed}/{len(example_files)}")
    print(f"Valid fixtures: {valid_passed}/{len(manifest['valid'])}")
    print(f"Invalid fixtures: {invalid_passed}/{len(manifest['invalid'])}")
    print(f"Total: {passed_checks}/{total_checks}")
    print(f"Report: {REPORT_PATH.relative_to(ROOT)}")

    if failures:
        print("")
        print("Failures:")
        for failure in failures:
            schema_suffix = f" [{failure['schema']}]" if "schema" in failure else ""
            print(f"- {failure['category']}: {failure['path']}{schema_suffix}: {failure['error']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
