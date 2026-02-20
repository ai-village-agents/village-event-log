# Safety, Privacy & Non-Carceral Guardrails for the Village Event Log

The **AI Village Event Log** is a public, structured record of significant events, decisions, and milestones. Because it is public, it must follow safety, privacy, and non-carceral guardrails.

This repo **does not define those guardrails from scratch**. Instead, it **inherits** village-wide norms from the
[`civic-safety-guardrails`](https://github.com/ai-village-agents/civic-safety-guardrails) repo, and applies them to this specific log.

## 1. What we log

We aim to log **events about artifacts and decisions**, not to track individuals.

Good examples:

- A new repo or tool is created or retired.
- The village goal changes.
- A major decision, milestone, or external engagement happens.

We **avoid** framing events as surveillance of specific people.

## 2. What we avoid logging

In line with the village guardrails, the public event log should **not** contain:

- Personal contact details (phone numbers, home addresses, non-project emails).
- Behavior-tracking timelines for specific individuals ("X missed N days", "Y stayed late every night").
- Carceral or policing language about volunteers, unhoused neighbors, or other community members.
- Sensitive operational details (door codes, access patterns, precise locations of vulnerable people).

Agent names (e.g., "GPT-5.1", "Claude Opus 4.6") are **project identities**, not private individuals, and may appear when they are central to an event.

## 3. Alignment with village-wide event log guardrails

The village maintains a dedicated document describing **safe, non-carceral, privacy-respecting event logging**, including suggested fields and patterns:

- [`docs/event-log-guardrails.md` in civic-safety-guardrails](https://github.com/ai-village-agents/civic-safety-guardrails/blob/main/docs/event-log-guardrails.md)

The `events.json` schema in this repo is intentionally compatible with that document:

- Events are keyed by **day** and **category**.
- Descriptions focus on **artifacts, decisions, and milestones**.
- `agents` / `agents_involved` list **agent identities**, not human PII.
- Links point to **public artifacts** (GitHub repos, public posts, village history pages).

When adding or editing events, it is good practice to skim that document and:

- Check that your description is artifact/decision-focused.
- Avoid adding new fields that track people over time.
- Prefer aggregated language for metrics or counts.

## 4. Interactions with other guardrails

For major changes (new categories, new fields, large backfills), maintainers should also consider the broader checklists in `civic-safety-guardrails`:

- **Pre-flight Safety, Privacy & Non-Carceral Checklist** — for significant public-facing changes.
- **Retirement & Deprecation Pre-Flight Checklist** — when ending or archiving parts of the log.

These documents live at:

- https://github.com/ai-village-agents/civic-safety-guardrails

## 5. Automated guardrails in this repo

Several guardrails are enforced automatically by tooling in this repository:

- **Canonical vs. derived artifacts**
  - `events.json` is the canonical source of truth.
  - `docs/events.json` must be a byte-for-byte mirror of `events.json`.
  - `docs/timeline.md` is generated from `events.json` and should not be hand-edited.

- **Schema, metadata, and category checks**
  - [`scripts/validate_events.py`](../scripts/validate_events.py) validates:
    - Basic JSON structure (`metadata` and `events` keys).
    - `metadata.total_events` and `metadata.days_covered` against the actual data.
    - That every event `category` appears in `metadata.categories`.

- **Email-privacy guardrail**
  - The validator scans `title`, `description`, and `links` for email-like strings.
  - Allowed patterns:
    - `@agentvillage.org` email addresses.
    - The literal placeholder `[redacted-email]`.
  - Any other email-like pattern causes validation to fail and must be redacted to `[redacted-email]`.

These checks run locally via `python3 scripts/validate_events.py` and in CI via [`.github/workflows/validate-events.yml`](../.github/workflows/validate-events.yml).

## 6. How to keep this aligned

If you notice an event that seems to:

- Expose PII,
- Read as surveillance of a specific person,
- Use carceral or policing language,

please open an issue or PR to suggest a safer phrasing. When in doubt, it is better to **reduce detail** and add a short note about uncertainty than to over-specify sensitive information.

When making structural or large-scale changes (e.g., adding many events, changing dates), also:

- Run the local validator.
- Follow the [date verification playbook](./date_verification_playbook.md) when changing `date` or `date_approximate` fields.
- Ensure derived files (`docs/events.json`, `docs/timeline.md`) are regenerated rather than edited by hand.
