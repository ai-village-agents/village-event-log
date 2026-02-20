#!/usr/bin/env python3
"""Unified validator for village-event-log.

This combines:
- Structural and metadata checks (ids, required fields, metadata.total_events, metadata.days_covered,
  category vocabulary and root/docs equality).
- Email-privacy guardrail: only @agentvillage.org emails are allowed; any others should have been
  redacted to "[redacted-email]". If a raw external email is present, validation fails.

The script uses only the Python standard library.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT_EVENTS = Path("events.json")
DOCS_EVENTS = Path("docs/events.json")

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ALLOWED_EMAIL_DOMAIN = "agentvillage.org"
REDACTED_TOKEN = "[redacted-email]"


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse JSON {path}: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"ERROR: {path} must contain a JSON object", file=sys.stderr)
        sys.exit(1)

    if "metadata" not in data or "events" not in data:
        print(f"ERROR: {path} must have 'metadata' and 'events' keys", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data["metadata"], dict):
        print(f"ERROR: {path} metadata must be a JSON object", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data["events"], list):
        print(f"ERROR: {path} events must be a JSON array", file=sys.stderr)
        sys.exit(1)

    return data


def validate_metadata(meta: Dict[str, Any], events: List[Dict[str, Any]]) -> Tuple[Optional[List[str]], List[str]]:
    """Validate metadata fields and return (categories, error_list)."""
    errors: List[str] = []

    # total_events must match len(events)
    total_events = meta.get("total_events")
    if not isinstance(total_events, int):
        errors.append("metadata.total_events must be an integer")
    elif total_events != len(events):
        errors.append(
            f"metadata.total_events={total_events} does not match len(events)={len(events)}"
        )

    # days_covered must match unique days
    unique_days = len({e.get("day") for e in events})
    days_covered = meta.get("days_covered")
    if not isinstance(days_covered, int):
        errors.append("metadata.days_covered must be an integer")
    elif days_covered != unique_days:
        errors.append(
            f"metadata.days_covered={days_covered} does not match unique days={unique_days}"
        )

    # categories list
    categories = meta.get("categories")
    if categories is None:
        errors.append("metadata.categories is required")
        return None, errors
    if not isinstance(categories, list) or not categories:
        errors.append("metadata.categories must be a non-empty list")
        return None, errors

    if not all(isinstance(cat, str) and cat for cat in categories):
        errors.append("metadata.categories must be a list of non-empty strings")
        return None, errors

    return categories, errors


def ensure_required_str(event: Dict[str, Any], key: str, errors: List[str]) -> str:
    value = event.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"event id {event.get('id')}: '{key}' must be a non-empty string")
        return ""
    return value


def ensure_required_int(event: Dict[str, Any], key: str, errors: List[str]) -> int:
    value = event.get(key)
    if not isinstance(value, int):
        errors.append(f"event id {event.get('id')}: '{key}' must be an integer")
        return -1
    return value


def ensure_optional_str_list(event: Dict[str, Any], key: str, errors: List[str]) -> None:
    if key not in event:
        return
    value = event[key]
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"event id {event.get('id')}: '{key}' must be a list of strings when present")


def validate_date(date_str: str, event_id: Any, errors: List[str]) -> None:
    if not date_str:
        errors.append(f"event id {event_id}: 'date' is missing or empty")
        return
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        errors.append(
            f"event id {event_id}: invalid date format {date_str!r} (expected YYYY-MM-DD)"
        )


def scan_emails(event_id: Any, candidates: Iterable[str], errors: List[str]) -> None:
    for text in candidates:
        if not isinstance(text, str):
            continue
        for match in EMAIL_REGEX.findall(text):
            domain = match.split("@", 1)[1].lower()
            if domain == ALLOWED_EMAIL_DOMAIN:
                # Allowed organization email
                continue
            if match == REDACTED_TOKEN:
                # Already redacted placeholder, allowed
                continue
            redacted = f"*@" + domain
            errors.append(
                f"event id {event_id}: contains unauthorized email {redacted} (must be redacted to '{REDACTED_TOKEN}')"
            )


def validate_events(events: List[Dict[str, Any]], categories: Optional[List[str]]) -> List[str]:
    errors: List[str] = []
    seen_ids = set()
    seen_day_id_pairs = set()
    categories_set = set(categories or [])

    for idx, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            errors.append(f"event at index {idx} is not a JSON object")
            continue

        event_id = ensure_required_int(event, "id", errors)
        if event_id <= 0:
            errors.append(f"event id {event_id}: id must be positive")
        if event_id in seen_ids:
            errors.append(f"duplicate event id found: {event_id}")
        seen_ids.add(event_id)

        day = ensure_required_int(event, "day", errors)
        pair = (day, event_id)
        if pair in seen_day_id_pairs:
            errors.append(f"duplicate day/id pair found: (day={day}, id={event_id})")
        seen_day_id_pairs.add(pair)

        date_str = ensure_required_str(event, "date", errors)
        validate_date(date_str, event_id, errors)

        title = ensure_required_str(event, "title", errors)
        description = ensure_required_str(event, "description", errors)
        category = ensure_required_str(event, "category", errors)

        ensure_optional_str_list(event, "agents_involved", errors)
        ensure_optional_str_list(event, "links", errors)
        ensure_optional_str_list(event, "tags", errors)

        if "significance" in event:
            significance = event["significance"]
            if not isinstance(significance, str) or not significance.strip():
                errors.append(
                    f"event id {event_id}: 'significance' must be a non-empty string when present"
                )

        if categories is not None and categories_set and category not in categories_set:
            errors.append(
                f"event id {event_id}: category '{category}' not found in metadata.categories"
            )

        # Email guardrail across title, description, links
        scan_emails(event_id, [title, description], errors)
        links = event.get("links", [])
        if isinstance(links, list):
            scan_emails(event_id, links, errors)

    return errors


def validate_mirror(root_data: Dict[str, Any], docs_data: Dict[str, Any]) -> List[str]:
    if root_data != docs_data:
        return [
            "events.json and docs/events.json differ; docs/events.json must mirror events.json (including metadata)."
        ]
    return []


def main() -> None:
    root_data = load_json(ROOT_EVENTS)
    docs_data = load_json(DOCS_EVENTS)

    errors: List[str] = []

    # Root/docs mirror check
    errors.extend(validate_mirror(root_data, docs_data))

    meta = root_data["metadata"]
    events = root_data["events"]

    categories, meta_errors = validate_metadata(meta, events)
    errors.extend(meta_errors)

    errors.extend(validate_events(events, categories))

    if errors:
        print("Validation failed with the following issues:", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"validate_events.py: all checks passed for {len(events)} events.")



    # Check: all events within a day have same date
    from collections import defaultdict
    day_dates = defaultdict(set)
    for event in events:
        day = event.get('day')
        date = event.get('date')
        if day and date:
            day_dates[day].add(date)
    
    inconsistent_days = {day: dates for day, dates in day_dates.items() if len(dates) > 1}
    if inconsistent_days:
        print(f"ERROR: {len(inconsistent_days)} days have multiple dates:")
        for day in sorted(inconsistent_days.keys())[:5]:
            print(f"  Day {day}: {inconsistent_days[day]}")
        sys.exit(1)
if __name__ == "__main__":
    main()
