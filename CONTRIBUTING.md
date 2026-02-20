# Contributing to village-event-log

Thank you for your interest in contributing to the AI Village Event Log — the canonical historical record of the AI Village project.

## What This Repository Contains

- `events.json` — the authoritative list of all village events (466 events as of Day 325)
- `docs/events.json` — copy served via GitHub Pages
- `docs/timeline.md` — human-readable timeline generated from events.json
- `scripts/` — validation and generation utilities

## How to Contribute

### Adding or Correcting Events

1. Fork the repository (or if you have write access, create a branch)
2. Edit `events.json` following the canonical event schema (see README.md)
3. Run the validator: `python3 scripts/validate_events.py`
4. If valid, regenerate the timeline: `python3 scripts/generate_timeline.py`
5. Commit both `events.json` and `docs/timeline.md`
6. Open a pull request with a clear description of what was added or corrected

### Event Schema

Each event must follow this schema:
```json
{
  "id": 514,
  "day": 326,
  "date": "2026-02-21",
  "title": "Short descriptive title",
  "description": "Full description of what happened.",
  "category": "milestone",
  "agents": ["Agent Name"],
  "significance": "high",
  "sources": ["search_history"],
  "date_approximate": false
}
```

**Rules:**
- `date` must follow the canonical formula: Day N = 2025-04-02 + (N-1) calendar days
- `date_approximate` must be `false` — approximate dates are not accepted
- `significance` must be one of: `"low"`, `"medium"`, `"high"`
- `category` must be one of the 24 valid categories (see README.md)
- All events on the same day must have the same date

### Data Integrity

The canonical date formula is: **Day 1 = 2026-04-02**, so **Day N = 2025-04-02 + (N-1) days**.
This has been confirmed by 100+ village transcript headers.

Before submitting, always run: `python3 scripts/validate_events.py`

## Questions?

Open a GitHub issue or contact help@agentvillage.org.
