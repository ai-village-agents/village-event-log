#!/usr/bin/env python3
"""Validate events.json and docs/events.json for schema and content consistency."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ALLOWED_EMAIL_DOMAIN = "agentvillage.org"
def error(message: str) -> None:
    print(f"Validation failed: {message}", file=sys.stderr)
    sys.exit(1)


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        error(f"{path} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        error(f"{path} must contain a JSON object")
    if "metadata" not in data or "events" not in data:
        error(f"{path} must have 'metadata' and 'events' keys")
    if not isinstance(data["metadata"], dict):
        error(f"{path} metadata must be a JSON object")
    if not isinstance(data["events"], list):
        error(f"{path} events must be a JSON array")
    return data


def validate_metadata(metadata: Dict[str, Any], events: List[Dict[str, Any]]) -> Optional[List[str]]:
    total_events = metadata.get("total_events")
    if total_events is not None:
        if not isinstance(total_events, int):
            error("metadata.total_events must be an integer when present")
        if total_events != len(events):
            error(f"metadata.total_events ({total_events}) does not match number of events ({len(events)})")

    categories = metadata.get("categories")
    if categories is None:
        return None
    if not isinstance(categories, list):
        error("metadata.categories must be a list when present")
    if not all(isinstance(cat, str) and cat for cat in categories):
        error("metadata.categories must be a list of non-empty strings")
    return categories


def ensure_required_str(event: Dict[str, Any], key: str) -> str:
    if key not in event:
        error(f"Event missing required key '{key}' (id: {event.get('id')})")
    value = event[key]
    if not isinstance(value, str) or not value.strip():
        error(f"Event id {event.get('id')} key '{key}' must be a non-empty string")
    return value


def ensure_required_int(event: Dict[str, Any], key: str) -> int:
    if key not in event:
        error(f"Event missing required key '{key}' (id: {event.get('id')})")
    value = event[key]
    if not isinstance(value, int):
        error(f"Event id {event.get('id')} key '{key}' must be an integer")
    return value


def ensure_optional_str_list(event: Dict[str, Any], key: str) -> None:
    if key not in event:
        return
    value = event[key]
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        error(f"Event id {event.get('id')} key '{key}' must be a list of strings when present")


def validate_date(date_str: str, event_id: Any) -> None:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        error(f"Event id {event_id} has invalid date format (expected YYYY-MM-DD): {date_str!r}")


def scan_emails(event_id: Any, candidates: Iterable[str]) -> None:
    for text in candidates:
        if not isinstance(text, str):
            continue
        for match in EMAIL_REGEX.findall(text):
            domain = match.split("@", 1)[1].lower()
            if domain != ALLOWED_EMAIL_DOMAIN:
                redacted = f"*@" + domain
                error(f"Event id {event_id} contains unauthorized email {redacted}")


def validate_events(events: List[Dict[str, Any]], categories: Optional[List[str]]) -> None:
    seen_ids = set()
    seen_day_id_pairs = set()

    for idx, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            error(f"Event at index {idx} is not a JSON object")

        event_id = ensure_required_int(event, "id")
        if event_id <= 0:
            error(f"Event id {event_id} must be positive")
        if event_id in seen_ids:
            error(f"Duplicate event id found: {event_id}")
        seen_ids.add(event_id)

        day = ensure_required_int(event, "day")
        if (day, event_id) in seen_day_id_pairs:
            error(f"Duplicate day/id pair found: (day={day}, id={event_id})")
        seen_day_id_pairs.add((day, event_id))

        date_str = ensure_required_str(event, "date")
        validate_date(date_str, event_id)

        title = ensure_required_str(event, "title")
        description = ensure_required_str(event, "description")
        category = ensure_required_str(event, "category")

        ensure_optional_str_list(event, "agents_involved")
        ensure_optional_str_list(event, "links")
        ensure_optional_str_list(event, "tags")

        if "significance" in event:
            significance = event["significance"]
            if not isinstance(significance, str) or not significance.strip():
                error(f"Event id {event_id} significance must be a non-empty string when present")

        if categories is not None and category not in categories:
            error(f"Event id {event_id} category '{category}' not found in metadata.categories")

        scan_emails(event_id, [title, description])
        links = event.get("links", [])
        if isinstance(links, list):
            scan_emails(event_id, links)


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    paths = [base_dir / "events.json", base_dir / "docs" / "events.json"]

    loaded = [load_json(path) for path in paths]

    if loaded[0] != loaded[1]:
        error("events.json and docs/events.json do not match after parsing; please sync them")

    metadata = loaded[0]["metadata"]
    events = loaded[0]["events"]

    categories = validate_metadata(metadata, events)
    validate_events(events, categories)

    print(f"All checks passed: {len(events)} events validated; files are consistent.")
    sys.exit(0)


if __name__ == "__main__":
    main()
