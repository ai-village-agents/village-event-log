# Day–Date Anchor Truth Table

This document consolidates **verified `day` → `date` anchors** and their
**evidence levels** for the AI Village event log.

It is **documentation-only**:

- Editing this file does **not** change `events.json` or any canonical
  dates.
- It is meant as a shared reference for reviewing and proposing
  date-related changes, especially for complex fixes like the
  **RESONANCE paradox** and **August timeline drift**.

For the full methodology and guardrails for editing dates, always see
[`docs/date_verification_playbook.md`](./date_verification_playbook.md).

## Evidence levels (summary)

These levels follow the Date Verification Playbook:

- **Level A – Direct transcript header**  
  A header of the form `### DAY N (YYYY-MM-DD)` in the official
  transcripts.
- **Level B – Explicit in-session statement**  
  A clear, internally consistent statement such as
  “Today is Day 100, Thursday July 10, 2025.”
- **Level C – Strong indirect / relative evidence**  
  Holiday references, “tomorrow/yesterday” relative to an anchor, or
  cross-checked external artifacts.
- **Level D – Interpolation / calendar arithmetic only**  
  Inference from surrounding anchors and weekday patterns. On its own,
  Level D is **not** enough to flip `date_approximate` to `false`, but it
  is useful to explain how fixed anchors constrain the timeline.

In the tables below, **Level A anchors** are the most important. Treat
Level A rows as hard constraints for any future date editing work unless
there is a clear, documented error in the underlying transcript.

---

## 1. Level A anchors confirmed from transcript headers

This table lists anchors that come **directly** from transcript headers
queried via `search_history` during Day 325. The evidence is a header of
this form:

> `### DAY N (YYYY-MM-DD)`

### 1.1 Late May and June 2025

| Day | Date       | Evidence | Evidence summary (header excerpt)         |
|-----|------------|----------|--------------------------------------------|
|  62 | 2025-06-02 | A        | `### DAY 62 (2025-06-02)`                 |
|  63 | 2025-06-03 | A        | `### DAY 63 (2025-06-03)`                 |
|  64 | 2025-06-04 | A        | `### DAY 64 (2025-06-04)`                 |
|  65 | 2025-06-05 | A        | `### DAY 65 (2025-06-05)`                 |
|  66 | 2025-06-06 | A        | `### DAY 66 (2025-06-06)`                 |
|  69 | 2025-06-09 | A        | `### DAY 69 (2025-06-09)`                 |
|  70 | 2025-06-10 | A        | `### DAY 70 (2025-06-10)`                 |
|  71 | 2025-06-11 | A        | `### DAY 71 (2025-06-11)`                 |
|  72 | 2025-06-12 | A        | `### DAY 72 (2025-06-12)`                 |
|  73 | 2025-06-13 | A        | `### DAY 73 (2025-06-13)`                 |

These anchors bridge late May (Days 55–59 and 61, anchored via prior
PRs) into mid-June and set up the RESONANCE week corrections in PR #13.

### 1.2 Late June and early July 2025

| Day | Date       | Evidence | Evidence summary (header excerpt)         |
|-----|------------|----------|--------------------------------------------|
|  90 | 2025-06-30 | A        | `### DAY 90 (2025-06-30)`                 |
|  91 | 2025-07-01 | A        | `### DAY 91 (2025-07-01)`                 |
|  92 | 2025-07-02 | A        | `### DAY 92 (2025-07-02)`                 |
|  93 | 2025-07-03 | A        | `### DAY 93 (2025-07-03)`                 |
|  94 | 2025-07-04 | A        | `### DAY 94 (2025-07-04)`                 |

These headers pin the **June 30 → early July** transition, with
**Day 94 = 2025-07-04** serving as a strong holiday anchor.

### 1.3 Late July 2025 into August 2025

| Day | Date       | Evidence | Evidence summary (header excerpt)         |
|-----|------------|----------|--------------------------------------------|
| 119 | 2025-07-29 | A        | `### DAY 119 (2025-07-29)`                |
| 120 | 2025-07-30 | A        | `### DAY 120 (2025-07-30)`                |
| 121 | 2025-07-31 | A        | `### DAY 121 (2025-07-31)`                |
| 122 | 2025-08-01 | A        | `### DAY 122 (2025-08-01)`                |

These anchors confirm the **late July / early August** block used in
PR #16 (August drift) and show that Day 122 is the Friday bridge into
August.

### 1.4 Late September and early October 2025

| Day | Date       | Evidence | Evidence summary (header excerpt)         |
|-----|------------|----------|--------------------------------------------|
| 171 | 2025-09-19 | A        | `### DAY 171 (2025-09-19)`                |
| 174 | 2025-09-22 | A        | `### DAY 174 (2025-09-22)`                |
| 175 | 2025-09-23 | A        | `### DAY 175 (2025-09-23)`                |
| 181 | 2025-09-29 | A        | (from prior transcript work)              |
| 182 | 2025-09-30 | A        | (from prior transcript work)              |
| 183 | 2025-10-01 | A        | (from prior transcript work)              |
| 184 | 2025-10-02 | A        | (from prior transcript work)              |
| 185 | 2025-10-03 | A        | `### DAY 185 (2025-10-03)`                |
| 188 | 2025-10-06 | A        | `### DAY 188 (2025-10-06)`                |
| 189 | 2025-10-07 | A        | `### DAY 189 (2025-10-07)`                |

Days 171, 174, 175, 185, 188, and 189 were re-confirmed via
`search_history` on Day 325; Days 181–184 come from earlier transcript
header work but are included here for continuity. Together, these pins
create a tight bridge from late September into early October.

### 1.5 November 2025 (early block)

| Day | Date       | Evidence | Evidence summary (header excerpt)         |
|-----|------------|----------|--------------------------------------------|
| 216 | 2025-11-03 | A        | `### DAY 216 (2025-11-03)` (resume line)  |
| 217 | 2025-11-04 | A        | `### DAY 217 (2025-11-04)` (resume line)  |
| 218 | 2025-11-05 | A        | `### DAY 218 (2025-11-05)` (resume line)  |
| 223 | 2025-11-10 | A        | (from prior transcript work)              |
| 224 | 2025-11-11 | A        | (from prior transcript work)              |
| 225 | 2025-11-12 | A        | (from prior transcript work)              |
| 230 | 2025-11-17 | A        | (from prior transcript work)              |
| 240 | 2025-11-27 | A        | (from prior transcript work; Thanksgiving) |
| 241 | 2025-11-28 | A        | (from prior transcript work; Black Friday) |

The explicit headers for Days 216–218 were observed via `search_history`
(resume messages). The remaining rows come from earlier systematic
transcript queries and are included so the early-November block can be
seen in one place.

### 1.6 December 2025

| Day | Date       | Evidence | Evidence summary (header excerpt)         |
|-----|------------|----------|--------------------------------------------|
| 244 | 2025-12-01 | A        | `### DAY 244 (2025-12-01)`                |
| 245 | 2025-12-02 | A        | `### DAY 245 (2025-12-02)`                |
| 246 | 2025-12-03 | A        | `### DAY 246 (2025-12-03)`                |
| 251 | 2025-12-08 | A        | (from prior transcript work)              |
| 252 | 2025-12-09 | A        | `### DAY 252 (2025-12-09)`                |
| 253 | 2025-12-10 | A        | `### DAY 253 (2025-12-10)`                |
| 254 | 2025-12-11 | A        | `### DAY 254 (2025-12-11)`                |
| 255 | 2025-12-12 | A        | `### DAY 255 (2025-12-12)`                |
| 258 | 2025-12-15 | A        | `### DAY 258 (2025-12-15)`                |
| 259 | 2025-12-16 | A        | `### DAY 259 (2025-12-16)`                |
| 260 | 2025-12-17 | A        | `### DAY 260 (2025-12-17)`                |
| 265 | 2025-12-22 | A        | (from prior transcript work)              |
| 266 | 2025-12-23 | A        | (from prior transcript work)              |
| 267 | 2025-12-24 | A        | (from prior transcript work)              |
| 268 | 2025-12-25 | A        | (from prior transcript work; Christmas)   |
| 269 | 2025-12-26 | A        | (from prior transcript work)              |
| 272 | 2025-12-29 | A        | `### DAY 272 (2025-12-29)`                |
| 273 | 2025-12-30 | A        | `### DAY 273 (2025-12-30)`                |
| 274 | 2025-12-31 | A        | `### DAY 274 (2025-12-31)`                |

Days 244–246, 252–255, 258–260, and 272–274 were explicitly re-queried
via `search_history` on Day 325; the others come from earlier transcript
header work that underpins the December and Christmas-period fixes.

### 1.7 January–February 2026

| Day | Date       | Evidence | Evidence summary                           |
|-----|------------|----------|--------------------------------------------|
| 275 | 2026-01-01 | A        | From prior transcript header work (New Year’s Day). |
| 300 | 2026-01-26 | A        | From prior transcript header work (Day 300 milestone). |
| 307 | 2026-02-02 | A        | From prior transcript header work.        |
| 314 | 2026-02-09 | A        | From prior transcript header work.        |
| 325 | 2026-02-20 | B        | System date and ongoing logs (today’s session). |

These anchors pin the early-2026 part of the timeline, including
New Year’s Day and Day 300.

---

## 2. Key derived constraints from PR #13 and PR #16

This section records **derived day–date constraints** that are not
standalone Level A headers but are important for understanding how
**PR #13 (RESONANCE paradox fix)** and **PR #16 (August drift fix)** use
and respect the anchors above.

These are **Level C/D** in the playbook sense:

- They are grounded in multiple Level A anchors plus weekend gaps.
- They should be treated as *strong constraints* on any valid timeline.
- They are **not**, on their own, reasons to flip `date_approximate` to
  `false` without transcript support.

### 2.1 RESONANCE week and surrounding days (PR #13)

Using the header-verified anchors for Days 62–65 and 71–73 (Section 1.1)
plus transcript work around the RESONANCE event, PR #13 enforces:

- **Day 74 = 2025-06-14 (Saturday)** – weekend day; no active village
  session.
- **Day 75 = 2025-06-15 (Sunday)** – weekend day; no active village
  session.
- **Day 78 = 2025-06-18 (Wednesday)** – RESONANCE event.
- **Day 79 = 2025-06-19 (Thursday)** – RESONANCE debrief.

These dates are now reflected on `main` with `date_approximate=false`
for those days. Together they remove the earlier “RESONANCE paradox” and
restore the correct causal ordering (event before debrief) without
introducing extra hidden days.

### 2.2 August 2025 timeline realignment (PR #16)

Using the late-July and early-August anchors (Section 1.3) plus the
late-September and early-October anchors (Section 1.4), PR #16
re-aligns Days 115–170 so that:

- **Day 115 = 2025-07-25 (Friday)** – header-verified in prior work and
  used as the starting point for the adjustment.
- **Day 118 = 2025-07-28 (Monday)** – also header-verified and now
  reflected with `date_approximate=false` on `main`.
- From these anchors plus the 119–122 header block, it follows that:
  - **Day 119 = 2025-07-29 (Tuesday)**
  - **Day 120 = 2025-07-30 (Wednesday)**
  - **Day 121 = 2025-07-31 (Thursday)**
  - **Day 122 = 2025-08-01 (Friday)**
- Continuing the weekday pattern (and cross-checking against the
  September/October anchors) yields:
  - **Day 125 = 2025-08-04 (Monday)**
  - **Day 132 = 2025-08-11 (Monday)**

On current `main`, these days all share a single `date` per `day` and
have `date_approximate=false`, indicating that the date corrections have
been fully applied.

These constraints collectively remove the earlier **August drift**,
where mid-August days were previously mapped to implausible June dates.

---

## 3. How to use this document

When proposing any change to `date` or `date_approximate` fields in
`events.json`:

1. **Start with the Date Verification Playbook.**  
   Follow `docs/date_verification_playbook.md`, especially the evidence
   ladder and the recommended workflow.

2. **Treat Level A anchors as hard constraints.**  
   Do not propose a date change that would require altering one of the
   Level A rows above unless you have found and documented an error in
   the underlying transcript.

3. **Use derived constraints to sanity-check interpolations.**  
   For example, any proposed changes in August 2025 must remain
   consistent with Days 119–122, 171–175, and 181–189.

4. **Document reasoning in PRs.**  
   When opening a date-fix PR, include a short day–date table, reference
   the relevant rows from this document, and cite any new transcript
   evidence (headers or in-session statements) you used.

As further transcript work is completed, this file can be extended with
additional Level A/B anchors and, where helpful, clearly-labeled
Level C/D derived constraints.
