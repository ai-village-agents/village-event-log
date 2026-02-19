import json
import sys
from pathlib import Path

ROOT_EVENTS = Path('events.json')
DOCS_EVENTS = Path('docs/events.json')


def load_json(path: Path):
    try:
        with path.open() as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON {path}: {e}", file=sys.stderr)
        sys.exit(1)


def validate_structure(data):
    if not isinstance(data, dict):
        print("ERROR: Root of events.json must be an object", file=sys.stderr)
        sys.exit(1)
    for key in ("metadata", "events"):
        if key not in data:
            print(f"ERROR: Missing top-level key: {key}", file=sys.stderr)
            sys.exit(1)
    events = data["events"]
    if not isinstance(events, list):
        print("ERROR: 'events' must be a list", file=sys.stderr)
        sys.exit(1)
    return data["metadata"], events


def validate_metadata(meta, events):
    errors = []

    total_events = len(events)
    if meta.get("total_events") != total_events:
        errors.append(
            f"metadata.total_events={meta.get('total_events')} does not match len(events)={total_events}"
        )

    days_covered = len({e.get("day") for e in events})
    if meta.get("days_covered") != days_covered:
        errors.append(
            f"metadata.days_covered={meta.get('days_covered')} does not match unique days={days_covered}"
        )

    meta_categories = meta.get("categories")
    if not isinstance(meta_categories, list) or not meta_categories:
        errors.append("metadata.categories must be a non-empty list")

    return errors


def validate_events(meta, events):
    errors = []

    seen_ids = set()
    meta_categories = set(meta.get("categories") or [])
    used_categories = set()

    for idx, e in enumerate(events):
        ctx = f"event index {idx} (id={e.get('id')})"

        # id
        eid = e.get("id")
        if not isinstance(eid, int):
            errors.append(f"{ctx}: id must be int, got {type(eid).__name__}")
        else:
            if eid in seen_ids:
                errors.append(f"Duplicate id detected: {eid}")
            seen_ids.add(eid)

        # day
        if not isinstance(e.get("day"), int):
            errors.append(f"{ctx}: day must be int")

        # date
        if not isinstance(e.get("date"), str) or not e.get("date"):
            errors.append(f"{ctx}: date must be non-empty string")

        # title / description
        if not isinstance(e.get("title"), str) or not e.get("title"):
            errors.append(f"{ctx}: title must be non-empty string")
        if not isinstance(e.get("description"), str) or not e.get("description"):
            errors.append(f"{ctx}: description must be non-empty string")

        # category
        cat = e.get("category")
        if not isinstance(cat, str) or not cat:
            errors.append(f"{ctx}: category must be non-empty string")
        else:
            used_categories.add(cat)
            if meta_categories and cat not in meta_categories:
                errors.append(
                    f"{ctx}: category '{cat}' not present in metadata.categories"
                )

    return errors


def validate_mirror(root_data, docs_data):
    if root_data != docs_data:
        print(
            "ERROR: events.json and docs/events.json differ. "
            "Please sync them (docs/events.json should mirror root events.json).",
            file=sys.stderr,
        )
        return False
    return True


def main():
    root_data = load_json(ROOT_EVENTS)
    docs_data = load_json(DOCS_EVENTS)

    meta, events = validate_structure(root_data)

    errors = []
    errors.extend(validate_metadata(meta, events))
    errors.extend(validate_events(meta, events))

    if not validate_mirror(root_data, docs_data):
        errors.append("docs/events.json mismatch")

    if errors:
        print("Validation failed with the following issues:", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)

    print("validate_events.py: all checks passed.")


if __name__ == "__main__":
    main()
