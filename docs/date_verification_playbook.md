# Date Verification Playbook

_Last updated: 2026-02-20 (Village Day 325)_

This playbook explains **how to verify and maintain calendar dates** in `events.json`, and how to use the `date_approximate` flag responsibly.

It encodes:

- The difference between **day numbers** and **calendar dates**
- Evidence levels for date claims
- A **checklist for safely flipping `date_approximate` from `true` to `false`**
- A living table of currently verified **date anchors**

The goal is to keep the event log historically accurate **without over‑claiming precision** where the transcripts are ambiguous.

---

## 1. Concepts: `day`, `date`, and `date_approximate`

The village runs in numbered **days** (Day 1, Day 2, …, Day 325). We also record a calendar **`date`** (`YYYY-MM-DD`).

- `day` is always primary and authoritative.
- `date` is our **best mapping** from that day number to the real‑world calendar.
- `date_approximate` indicates how confident we are about that mapping.

### 1.1 Semantics of `date_approximate`

Use `date_approximate` with the following meaning:

- `date_approximate = false`
  - We have **direct evidence** tying this day number to a specific calendar date.
  - Example: transcript header `### DAY 62 (2025-06-02)` or an explicit statement like
    > "Welcome to Day 100 of the AI Village on Thursday, July 10, 2025."
  - All events with that `day` should share the same exact `date` and `date_approximate=false`.

- `date_approximate = true`
  - The date is inferred (e.g., from the weekday‑only pattern or nearby anchors) but **not explicitly confirmed** in transcripts.
  - This is the default for most earlier days unless/until stronger evidence is found.

Do **not** set `date_approximate=false` solely because a date "looks right" when linearly interpolated. Weekend skips, holidays, and breaks make linear interpolation unreliable.

---

## 2. Evidence Levels for Dates

When researching dates in the transcripts (via the history search tools), classify what you find into evidence levels.

### Level A — Header anchors (strong)

- The transcript header explicitly pairs a day number with a date, for example:

  ```text
  ### DAY 62 (2025-06-02)
  ```

- Or an equivalent machine‑readable header that unambiguously ties `DAY N` to `YYYY-MM-DD`.

**Handling:**
- Treat these as **primary anchors**.
- It is safe to set `date_approximate=false` for that `day` and to correct `date` if needed.


### Level B — In‑session explicit date statements (strong)

- A speaker in the transcript clearly states both **day number** and **full date**, or day + weekday + month + day.
  - Example: `"Today is Day 139, Tuesday August 20, 2025"`.

**Handling:**
- Also treated as **anchor‑grade evidence**, especially if consistent with other references.
- Use these to set or correct `date` and set `date_approximate=false`.


### Level C — Relative date references (medium)

- References like:
  - "Tomorrow is July 10th."
  - "We’re two days out from the June 14 picnic."
- Or clear links to an external, dated artifact (e.g., a blog post or paper with a known publication date) that is tightly coupled to this village day.

**Handling:**
- Use these to **propose** a date, but confirm:
  - That the implied weekday matches the day number’s position in the known weekday‑only pattern.
  - That the inferred date is consistent with all nearby Level A/B anchors.
- Only flip `date_approximate` to `false` if the inferred date survives these consistency checks.


### Level D — Pattern or interpolation only (weak)

- Inferences based solely on:
  - The weekday‑only schedule
  - Counting business days between anchors
  - Statements like "this is about a week after Day 50" without an external calendar reference.

**Handling:**
- **Never sufficient on their own** to set `date_approximate=false`.
- You may adjust `date` using careful interpolation, but keep `date_approximate=true` and document the rationale in a PR description.

---

## 3. Safe Workflow for Updating Dates

Use this checklist when you want to correct or confirm dates for one or more days.

### Step 1 — Choose a target day range

Pick a small contiguous range (for example, Days 60–70 or Days 135–145):

- Prefer ranges that are currently **sparse** or have `date_approximate=true`.
- Check `events.json` first to see which days already have `date_approximate=false`.


### Step 2 — Search transcripts for anchor‑grade evidence

Using the history search tools, look specifically for:

- Transcript headers: `"### DAY 62 (2025-06-02)"` style lines.
- Phrases combining day and date: `"Day 100", "July 10"`, etc.
- Mentions of concrete external dates ("on June 14", "by October 20th"), especially near session openings or recaps.

Capture:

- Exact quotes
- Day numbers
- Calendar dates and weekdays

These snippets should later be cited in your PR description.


### Step 3 — Classify evidence and propose dates

For each `day` in your range:

1. Assign the strongest evidence level you’ve found (A–D).
2. Propose a `date` value:
   - If Level A/B: use the stated date.
   - If Level C: compute the implied date and cross‑check weekday and neighbor anchors.
   - If Level D only: consider leaving the existing date as‑is, or adjusting by interpolation **without** changing `date_approximate=true`.

If evidence conflicts (e.g., two different dates appear for the same day), **stop and document the conflict** instead of guessing.


### Step 4 — Update `events.json` (canonical)

For each day where you have a strong proposal:

1. Update every event with that `day` so that:
   - `date` is the same canonical `YYYY-MM-DD`.
   - `date_approximate` is set according to your evidence level:
     - Level A/B and consistent → `false`.
     - Level C, carefully cross‑checked → usually `false` (but may remain `true` if any doubt remains).
     - Level D only → **keep `true`**.
2. Do **not** change `id`, `day`, or other unrelated fields.
3. If you discover that existing `date_approximate=false` entries were based only on weak evidence, you may flip them **back** to `true`, but call this out clearly in your PR.


### Step 5 — Mirror, validate, regenerate

Follow the standard contributor workflow documented in `README.md`:

```bash
# 1. Mirror canonical events to docs
cp events.json docs/events.json

# 2. Run schema + metadata + email-privacy validation
python3 scripts/validate_events.py

# 3. Regenerate the human-readable timeline
python3 scripts/generate_timeline.py
```

Ensure that:

- Validation passes.
- `events.json` and `docs/events.json` remain identical.
- `docs/timeline.md` is updated.


### Step 6 — Document your reasoning in the PR

In your pull request description, include:

- The **day range** you touched.
- A short **table or bullet list** of `day → date → evidence level`.
- **Transcript quotes** (or search excerpts) that support each Level A/B/C anchor.
- Any remaining uncertainties or open questions.

This makes later audits and refinements much easier and keeps our decisions transparent.

---

## 4. Current Date Anchors (Living Table)

This section is a **living inventory** of high‑confidence anchors discovered so far. When you add or refine anchors, please update this table and cite your transcript evidence in the PR.

> **Note:** The exact set of anchors will evolve. If this table ever diverges from `events.json`, treat `events.json` (plus its `date_approximate` flags) as canonical and file a PR to reconcile the difference.

### 4.1 Strong anchors (Level A/B)

The following day/date pairs are supported by transcript headers or equally strong statements (summary only — see individual PRs for verbatim quotes):

| Day | Date       | Evidence summary                               |
|-----|------------|-----------------------------------------------|
| 1   | 2025-04-02 | Origin day; header and narrative agreements   |
| 6   | 2025-04-06 | Early‑era transcript header                   |
| 10  | 2025-04-11 | Early‑era transcript header                   |
| 13  | 2025-04-14 | First weekday after early weekend break       |
| 14  | 2025-04-15 | Consecutive header sequence                   |
| 15  | 2025-04-16 | Consecutive header sequence                   |
| 41  | 2025-05-12 | PR #8 — "Holiday Break: Trivia & Scavenger Hunts"; header + recap |
| 45  | 2025-05-16 | PR #8 — "Project Resonance" planning; header + recap |
| 50  | 2025-05-21 | Mid‑May header anchor                         |
| 51  | 2025-05-22 | Mid‑May header anchor                         |
| 52  | 2025-05-23 | Mid‑May header anchor                         |
| 55  | 2025-05-26 | Late‑May anchor                               |
| 62  | 2025-06-02 | Transcript header `DAY 62 (2025-06-02)`       |
| 63  | 2025-06-03 | Transcript header `DAY 63 (2025-06-03)`       |
| 64  | 2025-06-04 | Transcript header `DAY 64 (2025-06-04)`       |
| 73  | 2025-06-13 | History search: Day 73 header                 |
| 76  | 2025-06-16 | History search: Day 76 header                 |
| 100 | 2025-07-10 | Explicit Day 100 celebration date             |
| 139 | 2025-08-20 | Day 139 / August 20 anchors (see PR #9 notes) |
| 202 | 2025-10-20 | Late‑October anchor                           |
| 251 | 2025-12-08 | December anchor                               |
| 300 | 2026-01-26 | Day 300 milestone anchor                      |

This table intentionally summarizes rather than reproduces full transcript snippets; see individual enrichment PRs and search history for quoted context.


### 4.2 Derived but still approximate anchors (Level C/D)

Some days have dates that are **strongly suggested** by interpolation and surrounding anchors but lack a direct header or explicit statement. For example:

- Day 75 is likely **2025-06-15 (Sunday)**, inferred from nearby anchored days (73 and 76) and the weekday pattern, but the transcript for Day 75 is missing.

For such days we typically:

- Keep `date` set to the best‑guess value.
- Leave `date_approximate=true`.
- Document the reasoning in a PR description rather than inlining it here.


### 4.3 How to extend this table

When you confirm a new strong anchor:

1. Ensure `events.json` and `docs/events.json` are updated.
2. Flip `date_approximate` to `false` for all events with that `day` (if warranted).
3. Add a new row here with:
   - `Day`
   - `Date`
   - A 1–2 line **evidence summary** (e.g., "header", "opening recap", "explicit date statement").
4. In your PR description, include the actual transcript excerpts you used.

---

## 5. Guardrails and Common Pitfalls

- **Do not over‑fit the weekday pattern.** After the first 10 days, the village generally runs on weekdays, but there are gaps for weekends, holidays, and occasional breaks. Treat the pattern as a hint, not a proof.
- **Avoid chain‑inference.** If your only argument is "this date keeps everything else consistent", that is not enough to set `date_approximate=false`.
- **Respect uncertainty.** It is better to leave `date_approximate=true` than to assert a wrong exact date.
- **Keep edits narrow.** Prefer PRs that cover a modest day range (e.g., 5–20 days) with clearly documented evidence, rather than huge sweeping changes.
- **Use the validator.** Always run `scripts/validate_events.py` and regenerate the timeline before opening a PR.

By following this playbook, we can gradually turn approximate history into well‑supported, auditable dates—without losing track of where our knowledge is still uncertain.

---

## 6. Day 325 update: global mapping and anchor truth table

_As of Day 325, the village-event-log has been globally normalized and the date tooling has been hardened._

Key points:

- `metadata.day_1_date` is set to `"2025-04-02"` in `events.json`.
- A validator rule now enforces a **single global mapping**:
  - For every event, `date` must equal `day_1_date + (day - 1)` calendar days.
  - All events with the same `day` must share the same `date` and the same `date_approximate` value.
- All 466 events on Days 1–325 currently have `date_approximate=false` and pass this mapping check.

### 6.1 What this means for future edits

- Routine edits to existing events (changing titles, descriptions, agents, links, etc.) **must not** change `date` or `day`.
- Adding a new day (e.g., Day 326) must use the date implied by the formula above.
- If you believe transcript evidence contradicts the current mapping, treat that as a **schema-level discussion**:
  - Do not work around the validator with ad hoc `date` changes.
  - Instead, open an issue or PR proposing a mapping change and clearly document the evidence.

### 6.2 Using the day–date anchor truth table

The dense evidence that justified adopting the global mapping is recorded in:

- [`docs/day_date_anchor_truth_table.md`](./day_date_anchor_truth_table.md)

That document:

- Lists Level A/B anchors (direct headers and explicit date statements) across the timeline.
- Summarizes key derived constraints used in the RESONANCE (PR #13) and August drift (PR #16) fixes.

When making date-related changes, you should:

1. Use this playbook for process and guardrails.
2. Use the truth table as a **shared evidence base**.
3. Ensure any proposal stays consistent with both the global mapping and the anchors in that table.

> The anchor table in Section 4 above reflects an earlier, more compact summary. For the most up-to-date and detailed anchor set, prefer the dedicated truth table document.
