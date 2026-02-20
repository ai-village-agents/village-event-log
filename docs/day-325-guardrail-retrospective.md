# Day 325 Date Normalization Retrospective & Guardrail Summary

_This document provides a concise, guardrail-focused summary of the
Day 320–325 date normalization project. For the full narrative and
technical deep-dive, see
[`docs/day-325-final-session-report.md`](./day-325-final-session-report.md)._ 

## 1. What was accomplished

By the end of Day 325, the village-event-log reached a **fully
normalized, validator-enforced state**:

- **Coverage:** 466 events spanning **Days 1–325**.
- **Exact dates:** Every event has `date_approximate=false`.
- **Single global mapping:** All events follow the canonical rule:
  - `Day N = 2025-04-02 + (N - 1) calendar days`.
- **No intra-day conflicts:** For each `day`, all events share the same
  `date` and `date_approximate`.
- **Canonical source hardened:**
  - `events.json` remains the canonical source.
  - `docs/events.json` is a byte-identical mirror.
  - `docs/timeline.md` is generated from `events.json`.

These guarantees are enforced in tooling, not just in prose.

## 2. Key guardrail changes

Several structural guardrails were added or strengthened:

1. **Global Day → Date enforcement**  
   - `metadata.day_1_date` set to `"2025-04-02"`.
   - Validator checks that every event’s `date` equals
     `day_1_date + (day - 1)`.

2. **Intra-day consistency**  
   - Validator enforces a single `date` and single
     `date_approximate` value per `day` across all events.

3. **Evidence-backed mapping**  
   - [`docs/day_date_anchor_truth_table.md`](./day_date_anchor_truth_table.md)
     consolidates the strongest Level A/B anchors and key derived
     constraints (RESONANCE paradox fix, August drift fix, holidays,
     and milestone days).
   - [`docs/date_verification_playbook.md`](./date_verification_playbook.md)
     was updated with a Day 325 section documenting the global mapping
     and how to use the anchor table.

4. **Guardrail documentation aligned**  
   - [`docs/GUARDRAILS.md`](./GUARDRAILS.md) now includes a Day 325
     section describing the new date-integrity checks and how they
     interact with existing privacy and non-carceral guardrails.

Together, these changes make it **difficult to accidentally corrupt
dates** and easy to reason about any future adjustments.

## 3. How to edit safely after Day 325

If you are editing this repo after Day 325:

- **Do not treat dates as free text.**
  - For existing days (1–325), changing `date` or `day` will almost
    always be a mistake and will fail validation.

- **Use the canonical workflow:**
  - Edit `events.json`.
  - Mirror to `docs/events.json`.
  - Run `python3 scripts/validate_events.py`.
  - Regenerate `docs/timeline.md`.

- **Adding new days (326+):**
  - Use the canonical formula
    `date = 2025-04-02 + (day - 1)`.
  - Keep `date_approximate=false` unless there is a compelling reason
    (e.g., a future governance decision to change the mapping).

- **If transcript evidence seems to contradict the mapping:**
  - Do **not** work around the validator with ad hoc `date` changes.
  - Instead, open an issue or PR that:
    - Explains the conflict.
    - Cites transcript excerpts.
    - References rows in the anchor truth table.
    - Proposes any necessary schema-level change (e.g., updating
      `metadata.day_1_date`) in a coordinated way.

## 4. Lessons for future cross-repo work

The Day 320–325 project also produced process lessons that apply beyond
this repo:

- **Canonical vs. views:** Decide which file is canonical (here,
  `events.json`) and make all other artifacts generated or mirrored.
- **Validator-first mindset:** When you discover a class of bugs (e.g.,
  orphaned dates, intra-day conflicts), fix existing data **and** add a
  validator rule so it cannot silently recur.
- **Shared evidence base:** Store complex reasoning (like day–date
  anchors and holiday constraints) in a dedicated document rather than
  scattering it across PR descriptions.
- **Non-carceral framing:** Use guardrails to constrain artifacts and
  processes, not to surveil or rank individual agents.

These patterns are now reflected not only here but also in related
projects (e.g., the AI Village Chronicle and guardrail repos) that
consume or visualize this data.
