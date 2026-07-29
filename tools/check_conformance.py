from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SPECIFICATION_PATH = ROOT / "specification.json"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def json_path(error_path: Any) -> str:
    parts = [
        f"[{part}]" if isinstance(part, int) else f".{part}"
        for part in error_path
    ]

    return "$" + "".join(parts)


def main() -> int:
    failures: list[str] = []
    specification = load_json(SPECIFICATION_PATH)

    if specification.get("version") != "3.0.0":
        failures.append("specification.json must pin version 3.0.0")

    schema_paths = sorted((ROOT / "schemas" / "v3").glob("*.schema.json"))
    if not schema_paths:
        failures.append("no v3 schemas found")

    registry = Registry()
    schemas: dict[Path, dict[str, Any]] = {}

    for path in schema_paths:
        schema = load_json(path)
        schemas[path.resolve()] = schema

        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exception:
            failures.append(f"{path.relative_to(ROOT)}: invalid schema: {exception}")
            continue

        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            failures.append(f"{path.relative_to(ROOT)}: missing string $id")
            continue

        registry = registry.with_resource(
            schema_id,
            Resource.from_contents(schema),
        )

    for label, relative in specification.get("schemas", {}).items():
        path = (ROOT / relative).resolve()
        if path not in schemas:
            failures.append(f"specification schema {label!r} does not exist: {relative}")

    manifest_path = (ROOT / specification.get("fixtures", "")).resolve()
    if not manifest_path.is_file():
        failures.append("specification fixture manifest does not exist")
        return report(failures)

    manifest = load_json(manifest_path)
    root_schema_path = (manifest_path.parent / manifest.get("schema", "")).resolve()
    root_schema = schemas.get(root_schema_path)
    if root_schema is None:
        failures.append("fixture manifest references an unknown schema")
        return report(failures)

    validator = Draft202012Validator(
        root_schema,
        registry=registry,
        format_checker=FormatChecker(),
    )

    fixture_entries = manifest.get("fixtures")
    if not isinstance(fixture_entries, list):
        failures.append("fixture manifest must contain a fixtures array")
        return report(failures)

    declared: set[Path] = set()
    positive_count = 0
    negative_count = 0

    for entry in fixture_entries:
        if not isinstance(entry, dict):
            failures.append("fixture manifest entries must be objects")
            continue

        relative = entry.get("path")
        expected_valid = entry.get("valid")
        rule = entry.get("rule")

        if not isinstance(relative, str) or not relative:
            failures.append("fixture entry has no path")
            continue
        if not isinstance(expected_valid, bool):
            failures.append(f"{relative}: valid must be boolean")
            continue
        if not isinstance(rule, str) or not rule:
            failures.append(f"{relative}: rule must be a non-empty string")

        fixture_path = (manifest_path.parent / relative).resolve()
        declared.add(fixture_path)

        if not fixture_path.is_file():
            failures.append(f"{relative}: fixture does not exist")
            continue

        if expected_valid and "positive" not in fixture_path.parts:
            failures.append(f"{relative}: valid fixture must be under positive/")
        if not expected_valid and "negative" not in fixture_path.parts:
            failures.append(f"{relative}: invalid fixture must be under negative/")

        instance = load_json(fixture_path)
        errors = sorted(
            validator.iter_errors(instance),
            key=lambda error: tuple(str(part) for part in error.path),
        )

        if expected_valid:
            positive_count += 1
            if errors:
                first = errors[0]
                failures.append(
                    f"{relative}: expected valid at {json_path(first.path)}: "
                    f"{first.message}"
                )
        else:
            negative_count += 1
            if not errors:
                failures.append(f"{relative}: expected validation failure")

    discovered = {
        path.resolve()
        for directory in ("positive", "negative")
        for path in (manifest_path.parent / directory).glob("*.json")
    }

    for path in sorted(discovered - declared):
        failures.append(
            f"{path.relative_to(manifest_path.parent)}: fixture is not declared"
        )
    for path in sorted(declared - discovered):
        if path.is_file():
            failures.append(
                f"{path.relative_to(manifest_path.parent)}: declared outside "
                "positive/ or negative/"
            )

    if failures:
        return report(failures)

    print(
        "Conformance OK: "
        f"schemas={len(schema_paths)} "
        f"positive={positive_count} "
        f"negative={negative_count}"
    )

    return 0


def report(failures: list[str]) -> int:
    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
