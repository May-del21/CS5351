# Requirements change log (D1)

**Owner:** Member A.
**Scope:** Every decision and scope change to the requirement set, with timestamp and rationale. Appended, never rewritten. Earlier entries are not edited; a correction is a new entry that says what it corrects.

All times Asia/Hong_Kong (UTC+08:00).

---

## Entries

### 2026-11-07 19:27 — Change-log rule added

Requirement changes must be timestamped and recorded. This file is the record.

### 2026-11-10 19:50 — Rebased on v0.7.1

The registry was rebaselined on TradingAgents v0.7.1 after a source review. The no-holdings rules were pinned to `REQ-TA-RUN-001`; the deterministic validation gate became `REQ-TA-ARCH-002`.

### 2026-11-10 21:43 (Member A) — Added FR-004, FR-005, NFR-REPRO-001

Corrected ARCH-001, NFR-001, SAFETY-002 and Appendix A against v0.7.1.

### 2026-11-12 01:21 (Member A) — v2 after team review

Applied the team decisions recorded in `requirements-draft_problems.md`:

- Research-only scope; portfolio handling withdrawn from requirement claims.
- Three stop reasons only: `DATA`, `MODEL`, `BUDGET`.
- GUI withdrawn (`REQ-TA-FR-002`).
- Only missing price data stops a run.
- `RUN-001` split into separate fields (`run_outcome`, `stop_reason`, `rating`, `output_check`).
- `ARCH-002` redefined as a format check that makes no claim about truth.
- `REQ-TA-NFR-SAFETY-001`, `REQ-TA-NFR-SAFETY-002` and Appendix B (NH-1…NH-5) withdrawn.
- Added `FR-006` (freshness), `FR-007` (rating meaning, no ownership wording), `FR-008` (confidence consistent with data), `NFR-EVAL-001` (evaluation counting rules).

Result: **25 active requirements, 3 withdrawn.** This is the baseline for all later entries.

### 2026-11-12 (review) — Independent review returned 28 findings

`requirements-v2-review-2026-11-12.md` reviewed all 25 active requirements and returned findings V2-01…V2-28. Disposition of that review: findings only, not approved requirements. A accepted several fixes into v2 and left others open; see `requirement-source-notes.md` §3.

### 2026-11-20 (Member B) — Reconciliation candidate circulated

`reconciliation-2026-11-20.md` proposed 21 `SEL-TA-*` requirements as the next implementation increment. **Not adopted.** It is input to A's decision, and it targets a codebase that differs from the local v0.7.1 tree; see OQ-2 in `requirement-source-notes.md`.

### 2026-11-22 (Member A) — Final scope decision

`req-final-scope-A-2026-11-22.md` records A's decision:

| Action | Detail |
|---|---|
| Final active set | **25** requirements, IDs unchanged from v2 |
| Withdrawn | 3 (`FR-002`, `NFR-SAFETY-001`, `NFR-SAFETY-002`); IDs preserved, never reused |
| Blocking defect D-1 | `FR-005` gains coverage code `NOT_REQUESTED` (closes review finding V2-04) |
| Blocking defect D-2 | `NFR-EVAL-001` rule 5 split into repeatability and controlled-change comparison (closes V2-10) |
| Blocking defect D-3 | `NFR-COST-002` restated as a provable bound `CALL_CAP + N_concurrent_branches`, with zero dispatches outside a reservation |
| Lifecycle ruling D-5 | A resumed run keeps its `run_id` and adds an attempt; interrupted attempts are written `INCOMPLETE` and never edited; evaluation counts `run_id`s, not attempts (closes V2-07) |
| Scope rulings | A-1…A-9 (research-only, GUI withdrawn, portfolio code retained but unclaimed, etc.) |
| Status | **Proposed for adoption**, not adopted |

### 2026-11-22 (Member A) — Machine-readable registry published (D1)

Created the D1 artifacts:

| File | Content |
|---|---|
| `docs/req/requirements.yaml` | 25 active entries with ID, type, priority, status, statement, fit criterion, tradeoff, dependencies and sources |
| `docs/req/req-schema.json` | JSON Schema for the registry |
| `docs/req/validate.py` | Schema validation plus the cross-record rules a schema cannot express (unique IDs, no reused withdrawn IDs, no dangling dependencies, no Must→Could ordering, parameter references, no placeholder text, no unverified adoption claim) |

Content decisions recorded at creation:

1. **Statements, fit criteria and tradeoffs are carried from `requirements-draft-v2.md` verbatim** wherever v2 has them, so the registry cannot silently diverge from the reviewed baseline. The source SHA-256 is recorded in the file header.
2. **D-1, D-2 and D-3 are applied inside the affected entries**, marked `amended_by`, with the reason in `note`. The amendments do not live only in the decision document.
3. **GOV-002 had no tradeoff in v2.** A supplies one and marks it as an A-authored addition in `evidence`, because the D1 field set requires a tradeoff for every entry.
4. **`NFR-EVAL-001`'s statement is a numbered rule list, not a "shall" sentence.** The schema accepts this form and the entry's `evidence` records that A accepted it.
5. **`NFR-COST-002` is written as a guarantee-strength statement, not a mechanism mandate.** The `note` records why the bound is `CALL_CAP + N_concurrent_branches` and states that how the gap is closed is a B/D decision. This keeps A inside the ownership boundary in `project-deliverables-and-ownership.md` §1.
6. **All open numbers stay named parameters** in `parameter_appendix`. None is invented.

### 2026-11-22 (Member A) — Correction to an earlier count

An earlier draft of `req-final-scope-A-2026-11-22.md` said "24 active requirements (21 retained + 3 amended)". **That was wrong.** The correct count is **25 active**: 22 retained unchanged and 3 amended in place (FR-005, NFR-EVAL-001, NFR-COST-002). The decision document was corrected on the same day, and every section label was re-checked against its actual row count (8 / 10 / 3 / 2 / 2 = 25).

### 2026-11-22 (Member A) — v3 text baseline generated

Created `requirements-draft-v3.md` from v2. **v2 is unchanged** (SHA-256 still `5742540b…a62519f`) so the reviewed baseline and the review that cites it stay valid.

Method: 12 explicit text substitutions applied by a script that refuses to write unless v2's hash matches and each target string occurs exactly once. Verified afterwards: only 3 requirement blocks differ from v2 (FR-005, NFR-EVAL-001, NFR-COST-002); all 25 IDs, all priorities, all statuses and all type fields are identical; fixture counts unchanged.

Changes applied:

| Decision | Requirement | Effect |
|---|---|---|
| D-1 | FR-005 | `NOT_REQUESTED` added as a coverage code; disclosure rule states an unrequested channel is never a gap; fit criterion gains a market-only fixture case; Open names the branch |
| D-2 | NFR-EVAL-001 | Rule 5 split into repeatability and controlled-change modes; fit criterion gains the three comparison cases |
| D-3 | NFR-COST-002 | Statement restated as a bound with reservation ordering; fit criterion made provable ((a)–(d)); tradeoff names the allowance; non-normative note records the implementation gap and that the mechanism is not prescribed |

### 2026-11-22 (Member A) — D-3 technical decision request issued

`decision-request-D3-cost002-2026-11-22.md` asks Members B and D four questions about whether NFR-COST-002's bound is achievable: (Q1) can the bound hold while SDK retries stay invisible, (Q2) which mechanism, (Q3) the value of `N_concurrent_branches`, (Q4) whether the race test can be deterministic offline.

No reply yet. `NFR-COST-002` stays Must until a reply exists. The downgrade path is stated in the request so the answer cannot be ambiguous.

### 2026-11-22 (Member A) — `selected-requirements.md` prepared but not published

The file now carries the proposed selection table, the withdrawn list and a regeneration script, so adoption produces the final file in one step. Its status line still reads **NOT YET PUBLISHED**, and a YAML/table consistency check confirms the table matches `requirements.yaml` on all 25 rows.

### 2026-11-22 (Member A) — Course PDF obtained; D1 compliance gaps found and fixed

`CS5351-2026-2027-project.pdf` (pages 3–10), `cs5351-introduction.pptx` and `cs5351-2026-2027-process.pdf` were located in the course folder and read directly. Earlier entries in this log treated the ownership document's summary as the only course evidence; that was incomplete and is superseded by this entry.

**OQ-1 closed.** Page 5 asks for "a machine-readable product requirements document and a consolidated requirements registry, both in YAML, under `./docs/req/`", then names only `requirements.yaml` and `req-schema.json`. Page 9 and slide 24 both list the same two files. **One `requirements.yaml` is both the PRD and the registry. No second PRD YAML.**

Three format gaps against page 5 were found and fixed:

| Gap | Fix | Count change |
|---|---|---|
| No `type: invariant` entry, although ARCH-002 already held eight zero-tolerance rules R1–R8 | Promoted to `REQ-TA-INV-001`…`008`, Must, `zero_tolerance: true`, `enforced_by: REQ-TA-ARCH-002` | active 25 → **33** |
| Non-functional entries did not carry the course's `metric + threshold + verification` as distinct fields | Added all three to 10 entries; the schema now requires them by requirement type | — |
| No `baseline_observation` source links, although every entry had a baseline observation and page 5 requires existing-system findings be "linked to their sources" | Extracted and resolved every file path named in a `baseline` field; 26 entries now link to real files, and observations with no single file record the HEAD `9fa1196f` review explicitly | — |

`validate.py` now enforces the course's type coverage, the NFR field triple, the source-link rule, and the zero-tolerance properties of invariants. Each rule was confirmed by a negative test that fails as expected. Result: **33 requirements, 3 withdrawn, 0 errors, 0 warnings.**

The R1–R8 invariants are *promotions*, not new requirements: their statements and fit criteria come from ARCH-002's existing rules table. Enforcement stays with ARCH-002 (one deterministic output check); each invariant entry owns the rule's meaning and its zero-tolerance criterion. `rule_owner` records the provenance, kept separate from `dependencies` so that promoting a rule does not fabricate a Must→Should dependency ordering violation.

### 2026-11-22 (Member A) — Three questions issued to other owners

No requirement text changed. These are the three items that were blocked on someone else's answer.

| Question | To | Document | What A did |
|---|---|---|---|
| OQ-2: which repository is `reconciliation-2026-11-20.md` based on? | B | `question-to-B-repository-2026-11-22.md` | Verified that `e7aed7a9…` is reachable from no remote ref (one branch, one tip `9fa1196f`) and that `runapi/`, `checks.py`, `OutputChecker` and `Q1–Q4` are absent. Asked B four questions, including whether any unpublished work already centralises dispatch — the one answer that could invalidate D-3's premise. |
| OQ-5: is `NFR-COST-002`'s bound achievable? | B, D | `decision-request-D3-cost002-2026-11-22.md` | Finalised the request. Both code excerpts verified line by line against the tree (`setup.py` 160–166, `factory.py` 123–125) and the commit recorded in the header so B can check them against a different baseline. Added the verified analyst default (`trading_graph.py:56`, four analysts plus Memory Log). |
| OQ-3: how is a test-plan approval recorded? | E | `question-to-E-gov002-2026-11-22.md` | Asked E four questions: record location, minimum attribution fields, how CI proves "before the first implementation commit" (proposing git ancestry rather than a timestamp, because author dates are forgeable), and whether an exception path exists. |

Also asked E to confirm ownership of `docs/ai-use-log.yaml`, which the course PDF labels "(D1)" on page 9 but treats as a gate artefact on page 10. A's reading is that it is **E's**, and it has not been added to the requirement registry.

While drafting the OQ-3 request, A found a weakness in `GOV-002`'s current wording: the fit criterion compares timestamps, and a commit author controls their own timestamp. The requirement therefore currently promises a check that a rebase could defeat. This is recorded in the request as Q3 and will be restated in git-graph terms once E answers. `GOV-002` stays `to_be_confirmed` and **Must** in the meantime.

### 2026-11-22 (Member A) — Scope decision document synced to 33

`req-final-scope-A-2026-11-22.md` still said "25 active requirements" and predated the course-PDF review. It has been synced to the registry. **No requirement meaning changed** — this was alignment, not a new decision.

| Section | Change |
|---|---|
| Header | Basis now cites `requirements-draft-v3.md` and the course PDF |
| §1 | Active count 25 → 33; invariants row added |
| §2 | New §2.6 Invariants (8); withdrawn table renumbered to §2.7; FR-005, COST-002 and EVAL-001 summary rows updated to the amended criteria; a note added that `requirements.yaml` wins on any disagreement |
| §4 | Scope decisions A-10…A-13 added (invariant promotion, NFR field triple, source links, single YAML) |
| §5 | Four new limitations: GOV-002's timestamp weakness, invariants unenforced until ARCH-002 exists, COST-002 unproven, repository question open |
| §7 | Change-log entry added; the original "25 active" entry retained verbatim as history |

Verified by script: section labels 8 / 10 / 3 / 2 / 2 / 8 match their actual row counts and sum to 33; the document's ID set equals the registry's exactly (0 missing, 0 extra); every priority matches the YAML. The only remaining occurrence of "25 active" is the historical change-log line, which now reads "25 active at the time".

### 2026-11-23 (Member A) — Member B replied on COST-002; guarantee tightened to `<= CALL_CAP`

Member B's reply (`reply-to-A-cost002-2026-11-22.md`) answered the four questions in `decision-request-D3-cost002-2026-11-22.md`. A verified each technical claim against the tree before acting on it.

| B's answer | A's check | Effect |
|---|---|---|
| Q1: No for a counter around high-level invocations while SDK retries are unobserved; a transport gate could count them | Agreed. This is A's original D-3 reasoning, confirmed. | Noted, no change |
| Q2: Q2-a + Q2-b — one shared run-scoped controller, SDK retries off, each app retry takes a fresh reservation | `openai_client.py:213` forwards `max_retries` in `_PASSTHROUGH_KWARGS`, so `max_retries=0` is reachable on that path | Adopted as the intended mechanism, recorded in the non-normative note |
| Q3: 5 START branches by default (4 analysts + Memory Log), derived from the graph, not a constant; **branch count unnecessary to the bound** | Confirmed `setup.py:160-166`, `trading_graph.py:56` | **Branch allowance withdrawn** (see below) |
| Q4: Yes — injected barrier, 4 workers, one slot, exactly 1 grant and 3 denials; winner need not be deterministic | Accepted; this is the only offline-deterministic form | Adopted as criterion (c) |

**Why the bound tightened.** A had written `CALL_CAP + N_concurrent_branches` on the assumption that concurrent branches could race past a check. B pointed out that this assumption is wrong once a reservation is claimed *before* dispatch and is single-use: concurrent branches each hold their own reservation, so they do not cause overshoot. A also found that its own numbers were inconsistent — the request used 4 branches for the arithmetic while identifying 5 START branches. **Both forms cannot be right, and the strict form is stronger and simpler.**

| | Before (v3) | After (v4) |
|---|---|---|
| Bound | `dispatch_attempts <= CALL_CAP + N_concurrent_branches` (test 12) | `dispatch_attempts <= successful_reservations <= CALL_CAP` (test 8) |
| Reservation | "successful, atomic reservation" | Fresh, **single-use**, authorizes exactly one attempt, consumed even on failure |
| Attempt definition | "one dispatch to a provider" | Explicitly: timeouts, failures, app retries, structured-output re-requests, free-text fallback, memory reflections |
| (b) | `≤ 12 (= 8 + 4)` | `≤ 8`, with SDK retries disabled or every attempt gated |
| (c) | "4-branch race admits exactly 1" | After 7 slots consumed, 4 workers via **injected barrier** against the **real** reservation component, exactly 1 grant and 3 denials |
| (d) | "ends `INCOMPLETE(BUDGET)`" | Adds **no final rating** and **`output_check = NOT_RUN`**; and states a within-cap workflow ends **normally** |

**Also fixed.** The COST-002 `tradeoff` field had accumulated a duplicated sentence from an earlier automated amendment, and its `note` contained a doubled path (`tradingagents/tradingagents/...`). Both corrected. A scan of all 33 entries found no other duplicated text.

**What A did not accept or claim.** B's reply is explicitly a "Proposed B technical response" with no B/D signature. A has adopted it as **A's own requirement wording**, which is A's to set; it is not evidence that B signed, that D agreed, or that the bound is implemented. `COST-002` stays **Must** and **proposed**. Its non-normative note states plainly that the controller does not exist in the baseline and that the provider gateway's internal retries, billable usage and monetary cost are outside the guarantee.

**Still open, and now sharper.** B's reply reports inspecting `Le-kk/CS5351@56bbe29` and finding `tradingagents/runapi/result.py` there, and says `c0081cb` has identical content. A's tree (`May-del21/TradingAgents@9fa1196`) has no `runapi/` at all, and neither commit is reachable from A's remote. **This confirms A has been reading the wrong repository**, not that B erred. A's earlier statements that "`runapi/` does not exist" are true only of that tree and must be read that way. Every baseline observation in the registry was checked against `9fa1196`, so any item whose file moved or changed under `56bbe29` needs re-checking before D builds against it.

**New question for A to decide.** B reports the team's `StopReason` contains `MODEL_FAILURE`, `DATA_FAILURE`, `INTERNAL_ERROR`, `PERSISTENCE_ERROR` and `INTERRUPTED` — five values, and **no `BUDGET`**. `RUN-001` in this registry specifies exactly three (`DATA`, `MODEL`, `BUDGET`). This is a real vocabulary conflict. A has not resolved it; see OQ-6.

### 2026-11-23 (Member A) — Re-verified every baseline observation against the real team repository

The team repository was cloned to `/Users/emma/cityu/CS5351-team` at `c0081cb` (parent `56bbe29`). Member B's report was correct on both counts: `tradingagents/runapi/result.py` exists, and the `StopReason` literal is `MODEL_FAILURE, DATA_FAILURE, INTERNAL_ERROR, PERSISTENCE_ERROR, INTERRUPTED` — five values, no `BUDGET`.

**The larger finding is that A's registry understated the baseline substantially.** Every "no check exists", "nothing collects them", "no run id", "no prompt hash" statement had been verified against `May-del21/TradingAgents@9fa1196`, which is not the submission repository. Against `c0081cb` the boundary already implements the contract this registry describes:

| Requirement | Registry said | Verified baseline at `c0081cb` |
|---|---|---|
| RUN-001 | "no outcome, stop reason, check result or coverage field" | `runapi/result.py` defines all of them with cross-field invariants; `runapi/finalize.py` maps exceptions to reasons |
| ARCH-002 | "No check exists" | `runapi/checks.py` `OutputChecker` implements Q1–Q4 as blocking findings |
| NFR-REPRO-001 | "run_settings() has no run id, timing or prompt hash" | the run manifest carries `run_id`, `code_version`, `source_revision`, `prompt_hash`, `effective_config`, `start_ts_utc`/`end_ts_utc`, `fingerprint_sha256` |
| NFR-OBS-001 | "the graph writes one JSON state file per run" | `runapi/events.py` `EventSink` emits structured events alongside each run |
| SEC-002 | "`get_scrubbed` used by 2 vendor modules; coverage unverified" | plus `runapi/redact.py` `Redactor` at the event, report and error sinks |
| FR-007 | prompts say "recommend maintaining the current position" | prompts now condition Hold on `portfolio_context`; the ownership wording is gone |
| GOV-001 | "CI runs pytest, smoke, ruff; no semantic evaluation" | correct for CI; a semantic evaluation exists outside CI (`docs/verification/semantic-evaluation.md`) |

Confirmed unchanged: FR-004's look-ahead guards, FR-001's lack of evidence IDs, FR-005's lack of per-run coverage collection (no `coverage` field under `runapi/`), NFR-002's hard-coded `analyst_factories`, PERF-001/PERF-002/COST-001/COST-002/COST-003 having no run-level cap or timer, ARCH-001's 4 direct vendor imports in 3 agent files, `test_layering.py` banning only `yfinance`, and SEC-003's disclaimer living in the README.

**Wording corrections applied.** All seven affected `baseline` fields were rewritten to state what the boundary *does* and what remains unverified, rather than what is absent. No requirement statement, priority, dependency or status changed: the gap was in A's description of the baseline, not in the requirements. This matters for D, because "implemented" and "not implemented" lead to different work.

**Method error, recorded.** A bulk `yaml.dump` rewrite of `requirements.yaml` dropped the three `withdrawn_ids`, deleted REQ-TA-INV-005, and left two statements empty; the validator did not detect it because the schema only requires `scope` to exist. The registry was rebuilt deterministically from `requirements-draft-v4.md` by `rebuild_registry.py`, and `validate.py` gained three checks (non-empty prose, the recorded withdrawn set, all eight invariants). Negative fixtures for each check were confirmed to fail. `requirements-draft-v2/v3/v4.md` were never modified.

### 2026-11-23 (Member A) — OQ-6 and OQ-7 decided

**OQ-6, `stop_reason`: extend to six values.** `RUN-001` now specifies `MODEL_FAILURE`, `DATA_FAILURE`, `BUDGET`, `INTERNAL_ERROR`, `PERSISTENCE_ERROR`, `INTERRUPTED`, replacing the earlier three-value list (this line first read `DATA`/`MODEL`; corrected the same day under the revised decision below). Reasoning: the repository already produces runs ending `INCOMPLETE` with `PERSISTENCE_ERROR` or `INTERRUPTED`, so a three-value table left those runs without a valid row and the requirement was false for behaviour that exists. The mapping rule is now explicit: budget exhaustion is `BUDGET` and is never relabelled `INTERNAL_ERROR`; `INTERRUPTED` covers cooperative cancellation and pairs with D-5.

The fit criterion gained five numbered clauses: each of the six reasons appears at least once across 6 one-per-reason fixtures, 0 exhaustion fixtures are labelled `INTERNAL_ERROR`, and any reason outside the six-value vocabulary is 1 blocking defect.

**What A did not do.** `BUDGET` is not implemented — `grep BUDGET tradingagents/runapi/` returns nothing. That is D/B migration work; `RUN-001` stays `proposed`, and this entry states the target, not the current state.

**Revised the same day after Member B's reply (B2).** A had required renaming `MODEL_FAILURE`→`MODEL` and `DATA_FAILURE`→`DATA`. B rejected it: the values are serialized, and the rename touches 23 code/test sites and 9 documents, including `score_gov004.py:57`'s own `STOP_REASONS` set, which would silently reject renamed runs. A accepted and changed the requirement rather than the code. The vocabulary is now `MODEL_FAILURE`, `DATA_FAILURE`, `BUDGET`, `INTERNAL_ERROR`, `PERSISTENCE_ERROR`, `INTERRUPTED`; `MODEL`/`DATA` are labels only. `BUDGET` is the sole addition.

**A factual error of A's, corrected.** A had written that the live evidence contains `INCOMPLETE/PERSISTENCE_ERROR` and `INTERRUPTED` runs. B disputed it; A re-checked and B is right. All 15 deduplicated attempts in `docs/reviews/evidence/live-verification-2026-11-21/` are `COMPLETED` with `stop_reason` null. The justification for six values stands on the typed contract and offline fault tests, not on that cohort. The false sentence is corrected in place in `requirement-source-notes.md` rather than removed.

**B's other corrections, accepted.** `BUDGET` is recognised before the generic classifier; `agents/structured.py`, `memory/settlement.py` and the graph memory step must not swallow a refusal; a concurrent persistence failure keeps `PERSISTENCE_ERROR` primary with the budget cause in safe diagnostics (written into `run001-tables.md`); B proposes catalog row `R17` and will not renumber.

**OQ-7, invariant registers: superseded — split by layer.** The first decision was that B's `docs/architecture/invariants.md` is authoritative, and that A's eight entries merely point at it. B answered that this is the wrong direction: an architecture draft must not erase a requirement through an incorrect pairing. The decision is now that **A's YAML owns the requirement meaning and the zero-tolerance fit criterion, and B's register owns enforcement, runtime monitor and fallback; neither overrides the other.** `proposed_for_adoption` on all eight is correct, not stale.

**B's crosswalk replaced A's.** A had grouped four of the eight under INV-13; B: that is not equivalent coverage. A verified B's split against `invariants.md` and the Q-rules in `runapi/checks.py`: INV-001↔INV-08/INV-03/Q1 (partial), INV-002 (none), INV-003↔INV-02/INV-13 (partial), INV-004…007 (none), INV-008↔INV-03/Q3,Q4 (partial). `INV-001`'s statement was narrowed to what Q1 actually enforces, and `INV-006`'s scope was restricted to the sentiment band.

**A's own error, found while testing B's claim.** B wrote that `R1`–`R8` are the checker rules. In the team's documents they are not: `runtime-policy-catalog.md` uses the same prefix for trigger rows (its `R1` is a provider failover) and `checks.py` emits only `Q1`–`Q4`. Also `R4`–`R7` depend on coverage, sentiment and intermediate-output fields the checker never inspects, and `R2` has no enforcer. The registry and `arch002-rules.md` now say so explicitly: the table states what a compliant system must do, not what the baseline does.

**Also corrected: A had reshuffled its own invariants.** During the rebuild that followed the truncation incident, the eight entries were accidentally re-derived from requirement domains rather than from ARCH-002's R1–R8, so `INV-003` became "no look-ahead" instead of "no banned ownership phrase", and so on for five of the eight. The decision document always described INV-00n as Rn. The rebuild now reads the R1–R8 meaning from the v4 rule table, and all eight match section 2.6 again. Nothing downstream depended on the wrong version, because the registry had not been published.

**Residual.** B's reply is explicitly a draft awaiting Brian's confirmation ("Draft technical response for Brian's review"), D's implementation commitment, C's acceptance and team adoption. A records it as B's technical position, not as a signed agreement.

---

## Not yet decided

These are open and must not be read as resolved by the entries above.

| # | Open item | Owner | Blocks |
|---|---|---|---|
| 1 | Whether one combined YAML satisfies both "YAML PRD" and "consolidated registry" | A + E, with course authority | D1 completeness |
| 2 | Which repository the SEL-TA-* reconciliation describes | Team (B/D) | Any build work citing it |
| 3 | ~~Approval-record format for GOV-002~~ — **closed 2026-11-23**, E answered Q1–Q4 and withdrew its CI-receipt replacement | A + E | — |
| 4 | Whether B/D can make `NFR-COST-002` (a)–(d) hold | B, D | COST-002 Must vs Should |
| 5 | `QUALITY_THRESHOLD`, `RUN_TIME_CAP`, `TOKEN_BUDGET`, `CALL_CAP` values | D measures, A fixes | GOV-001, PERF-001, COST-001, COST-002 |
| 6 | Whether consent, privacy, snapshot and publication get their own invariant entries (OQ-8) | A + B | D1 invariant coverage |
| 7 | D-5 resume design versus INV-11/INV-12 fresh-ID and immutability rules (OQ-8) | A + B | Resume implementation |
| 8 | `SEL-TA-*` to `REQ-TA-*` reconciliation order agreed; the reconciliation table is drafted and awaits C's X1–X6 (OQ-9) | A drafts, C confirms | C's mapping, D9 evidence |
| 9 | Whether the other CI gates (`SEL-TA-GOV-003`, `SEL-TA-GOV-006`) also become requirements (OQ-10) | A + E | Total count, GOV coverage |
| 10 | `docs/ai-use-log.yaml` does not exist; only the `AI-log/` directory does (OQ-11) | E owns, A records | D1 deliverable completeness |
| 11 | Whether the schema-validation gate needs its own registry entry (OQ-12) | C (crosswalk X7), B raised it | Count, GOV coverage |
| 12 | Is the optional portfolio snapshot in input scope? (**Profile contradiction fixed 2026-11-23**; the scope itself is still for team adoption) | Team adoption | Scope, privacy fixtures, engineering evidence |
| 13 | `INV-009`…`013` acceptance-criteria corrections (B §2) — held until D answers Q-8d | B drafts, D answers, A applies | Candidate file only; not in the registry |
| 14 | Must/Should priority inversion: `INV-014` is Must while `FR-003`/`FR-006`/`NFR-REPRO-001` are Should | Team decides whether to raise them | Priority consistency |

---

## 2026-11-23 — Member E's E13–E15 answered: GOV-002 restored, count 33 → 34

**E withdrew its own proposal.** Earlier on 2026-11-23 E proposed replacing prior test-plan approval with post-implementation CI receipts. E has now checked the course PDF: page 10 gate 1 requires that "the tests for the change were approved before implementation began", and pages 6 and 7 require approval before code generation. A read those pages directly and confirms it. E has withdrawn the replacement and will implement the approval gate. The replacement wording is recorded as **withdrawn, not adopted**.

**A's own error, corrected.** A had intended to restate GOV-002's ordering check as commit ancestry, on the reasoning that a timestamp can be set by the author. E's answer is narrower and A accepts it: ancestry is the repository-ordering check only, and proves neither that coding began later nor that a human approved anything. GOV-002 now says so explicitly rather than implying more than it proves.

**GOV-002's record format is now stated** — the item v4 left as "team and course decision". `status` moves from `to_be_confirmed` to `proposed`. It is **not** `implemented`: E states the mechanism and its positive and negative checks are not built, and neither E's reply nor the course citation is the team's adoption record.

**New requirement: `REQ-TA-GOV-003` AI-use log updated before merge.** E14: course page 10 gate 6 names it, and page 9 lists `.github/workflows/ci.yml` as the D7 blocking-gate pipeline, so it belongs in the registry rather than only in repository process. **Count 33 → 34.** The team's `SEL-TA-GOV-005` states the same obligation; `GOV-003` is its `REQ-TA-*` counterpart, and the crosswalk records that, so no untracked duplicate is created.

**Verified before writing.** `.github/workflows/ci.yml` at `c0081cb` has three jobs (`test`, `smoke-install`, `lint`) and no AI-log, dependency, schema, semantic-evaluation or approval gate. Both new criteria are therefore about a gate that does not exist, and both entries say so.

**Recorded as an open delivery gap:** `docs/ai-use-log.yaml` does not exist; only `AI-log/` does (OQ-11). A will not mark it complete because the directory exists.

---

## Signature state

No entry above claims team adoption. Adoption is recorded only in `req-final-scope-A-2026-11-22.md` §6, and only when all five members' boxes are marked.

---

## 2026-11-23 — Member B's reply applied: scope corrections, and B is wrong about nothing so far

**Q-8a answered: five separate entries.** B answered from A's summary sheet without the full statements and said plainly it could not approve unseen criteria. A has now prepared the full file — `oq8-candidate-invariants-2026-11-23.md` with statements, zero-tolerance flags and Given/when/then fits — and a letter `send-to-B-2026-11-23.md`. **Neither has been sent yet.**

**B's scope corrections applied to the candidate file (not to the registry).** `INV-009` narrowed to declared supported entries; `INV-010` split into credential protection and holdings minimisation with separate fits; `INV-011` narrowed to owned artifacts plus path-escape and concurrency fits; `INV-012` mapped to INV-11+12+14 with "enforced in code, not proven end to end"; `INV-013` now requires runtime traversal, not only an import scan.

**B corrected two facts A had wrong.** First, `agents/structured.py` imports the shared `Redactor` at `c0081cb` — the R1 leak was repaired in `56bbe29` — so A no longer claims privacy is "wholly unimplemented". Second, `Q1`–`Q4` are not equivalent to A's proposed `R1`–`R8`, and a catalog row is policy rather than proof of wiring.

**Crosswalk corrections (four downgrades, two fixes, one withdrawal).** FR-007, NFR-001, NFR-004 and NFR-006 move from `equivalent` to a new `partial/overlap` label; NFR-005 names which dimension is unmapped; GOV-001 loses its "same ID number, opposite content" wording, which was wrong twice over and is moot now that E withdrew the replacement; GOV-006 is marked open rather than settled; and the GOV-002 row's mapping to `REQ-TA-GOV-001` plus `validate.py` is **withdrawn** as unsupported. The compared versions are now declared: the 19-ID working selection, not the 21-ID candidate.

**New open question, OQ-12.** The schema-validation gate has no registry entry. A did not add one. Course page 10 names it; B is right that the old mapping was wrong; but adding an entry on one objection would repeat the mistake of sweeping in `SEL-TA-GOV-003`/`006` on one partial answer. C is asked as crosswalk X7.

**Unchanged:** count still 34; nothing from B is in the registry; B's replies are recorded as B's technical position only — they are headed "Draft technical response for Brian to review" and are not signed agreement.

---

## 2026-11-23 — B's §4 answered: `N_EVAL` fixed, input scope re-proposed, two defects named

**`REQ-TA-NFR-EVAL-001` amended — two defects, one of them A's own.** B asked whether `N_EVAL` counts cases or attempts, and whether the existing five cases and two trials establish acceptance under `N_EVAL=20` with an open threshold. Both questions are valid. A then found a second problem: the parameter appendix says `N_EVAL` = 20 cases while the criterion exercised 10 records and never said they were not acceptance. New rule 5 states that `N_EVAL` counts **cases, never attempts**, that a changed population is a **versioned acceptance change** rather than a re-run, and that the rubric, critical items, profile and `QUALITY_THRESHOLD` are **required acceptance inputs owned by D and E**. A did not invent those four values. **Not implemented: no evaluation script exists.**

**Input scope, OQ-13 — A's position revised.** A's crosswalk said the portfolio exclusion "stands unless the team overturns it". That is wrong: the course requires the team to *adopt* `./docs/req/`, and an unadopted set proposes scope rather than settling it by silence. A now proposes **optional user-supplied portfolio input** with consent, freezing, fingerprinting and provenance, as a **proposed scope change requiring team adoption**. B's four §4.2 rows and two corrections were already applied; the schema row stays unmapped pending C (OQ-12/X7).

**Fixture-profile defect, disclosed and not fixed.** The offline profile in `requirements-draft-v4.md` line 577 pins `Portfolio | None`, yet `test_nfr003_privacy.py` needs a portfolio to plant a second position. The profile and the privacy criterion contradict each other. Changing the profile affects every requirement, so it is recorded as an open defect rather than edited quietly.

**Unchanged:** count still 34.

---

## 2026-11-23 — Appendix A contradiction fixed: one offline profile becomes three

**The defect.** `requirements-draft-v4.md` Appendix A pinned the offline profile to `Portfolio | None (research-only scope)`. Eleven test modules supply a portfolio, and `test_nfr003_privacy.py` plants `UNRELATED_HOLDING_MARKER` as a second position — it **cannot pass** without one. The declared profile and the privacy criterion contradicted each other, and A had shipped it.

**The fix, and what it deliberately does not do.** The offline profile is split into **A-A** (no portfolio, the default), **A-B** (confirmed snapshot, selected instrument absent) and **A-C** (confirmed snapshot with one unrelated holding). Every active requirement is assigned to exactly one profile group; static and CI gates are recorded as having no run profile. **No fixture count was re-derived.** Changing the population is a versioned acceptance change, not an edit to an appendix, so counts computed under the old single profile are left as they are and their profile coverage is now stated to be unknown.

**Schema `1.1.0` → `1.2.0`.** `fixture_profiles` is a new **required** top-level key, and `schema_version` is now pinned with `const` so a bump has to be deliberate. Anyone holding the `1.1.0` schema will see 34 valid requirements fail on the new key; `handoff-A-2026-11-23.md` and `confirm-to-E-2026-11-23.md` are updated so E does not wire the old one.

**Validator: three new rules, all run against negative fixtures.** Every active requirement must be assigned exactly once, no assignment may name an unknown ID, and `A-C` must exist. Before this, the fix could have been "made" by deleting `A-C`, which is the same defect with fewer lines. The negative fixtures are recorded in `negative-fixtures.md` rules 18–20.

**What this does not settle.** The input scope itself (OQ-13) is still a proposed change for team adoption. The profile now admits both inputs honestly instead of claiming one.

---

## 2026-11-23 — B's Q-8c answer applied, schema gate added: 34 → 36

**Two entries added, both on B's explicit statement.** `REQ-TA-INV-014` (immutable input snapshot) answers A's re-asked Q-8c with option (1); B's reasoning is that input mutation, artifact isolation and publication fail differently, so folding the snapshot rule into `INV-011` would tie it to the resume question D has not answered. `REQ-TA-GOV-004` (registry validates against its schema) follows B's position that "CI implementation alone is insufficient" and the obligation must be a machine-readable requirement.

**B did not confirm a total.** B wrote: "I cannot confirm a total of 35 without the complete current registry and all pending additions." Nothing in this change records B as agreeing to 36; B is recorded as requiring these two obligations, nothing more.

**The `GOV-004` collision, recorded rather than avoided.** The team's `SEL-TA-GOV-004` is the semantic-evaluation gate, which is A's `REQ-TA-GOV-001`; `docs/architecture/invariants.md` refers to it as "C's semantic evaluation (GOV-004)". A used `REQ-TA-GOV-004` anyway because numbering must not skip, and put a naming warning in the entry. The same warning is in `REQ-TA-INV-014`, because B pointed out that `REQ-TA-INV-014` is **not** architecture `INV-14`, which is the persistence rule mapped by `REQ-TA-INV-012`.

**Five validator errors on A's first draft, all real.** Missing `enforced_by`; a fit criterion that did not start with "Given"; no zero-tolerance wording; two entries with no fixture profile; and — the dangerous one — **the `A-B` assignment key written twice**, where Python silently keeps the last and drops the first. That is the same silent-data-loss shape as the earlier `yaml.dump` incident, and it was found by grep rather than by any tool complaining.

**A pre-existing false reference fixed.** The fixture-profile note cited `REQ-TA-INV-010` and `NFR-FR-003`; neither ID exists, and `INV-010` is only a candidate. It now reads "candidate entry INV-010 (which is NOT in this registry)".

**Three warnings left standing, deliberately.** `INV-014` is Must while the requirements it constrains (`FR-003`, `FR-006`, `NFR-REPRO-001`) are Should. A did not remove this by adding a dependency edge, which would have quietly changed another owner's priorities. It is recorded as open item 14 and named in the entry's note.

**Not done, on purpose.** B's §2 corrections to `INV-009`…`013` are **not** applied, because those five are still candidates outside the registry and `INV-011`'s wording depends on D's answer to Q-8d.

---

## 2026-11-24 — independent integration review: four fixes, and a submission deadline

An independent review of the uploaded package (`project-integration-review-2026-11-24.md`) reported against `a62b801`. **It is right on every point that concerns A.** Recorded here with what was actually done.

**I24 01 — the package was in the wrong place.** PR #16 was **merged** on 2026-11-23 at 22:24, not left open, and it had put the six files at the **repository root**: `requirements.yaml`, `req-schema.json`, `validate.py`, `requirement-source-notes.md`, `negative-fixtures.md`, `change-log.md`. The validator hard-coded `docs/req/...`, so the documented command failed at that location. A did not intend this — the upload went to the root because the GitHub "upload files" flow defaulted there and A did not check the resulting path before committing. Team main then relocated them to `docs/req/` in `424974a`. **The lesson is that A shipped a file layout without ever running the documented command from a fresh clone.** Both scripts now resolve their default paths from `__file__`, and the negative-fixture harness runs from any directory.

**I24 02 — the published snapshot was one revision stale.** Team main held the **34-entry** version; `REQ-TA-INV-014` and `REQ-TA-GOV-004` were in A's working copy and in correspondence but not published. **They were not removed, and A withdraws nothing.** The 36-entry version is the intended one. This entry also confirms the review's second point, which A had recorded but not fixed: `scope.statement` still said portfolio input was outside scope and every fixture ran without one, while Appendix A required a confirmed snapshot for three profiles. **Fixed today** — see below.

**I24 07 — two acceptance contradictions, both A's.** `REQ-TA-NFR-REPRO-001` fit (b) required the RUN-001 fields to be non-null in every record, while `REQ-TA-RUN-001`'s validity table makes the stop reason present only for incomplete runs and the rating only for completed runs. The statement also promised a record and report for every run with no exception, contradicting `REQ-TA-INV-012`'s persistence-failure rule. **Both corrected in `rebuild_registry.py` as a dated override**, with the v4 baseline left byte-identical because it is a recorded artefact at a pinned SHA-256. The fit now checks fields against the validity table and adds a critical-persistence-failure case.

**I24 04 — the validator passed things it claimed to reject.** Reproduced before fixing: deleting `CALL_CAP` exited 0; replacing withdrawn `REQ-TA-FR-002` with a fabricated ID exited 0 (rule 13 checked only the count); pointing `enforced_by` at a nonexistent ID exited 0; a duplicate top-level `schema_version` exited 0 because `yaml.safe_load` silently keeps the last. **All four now fail, and `negative-fixtures-check.py` executes 23 cases asserting non-zero exit *and* the stated reason.** Its first run found that A's own new fixtures did not mutate what they claimed — the harness caught A, which is the point of the harness.

**One correction to the review, offered as a correction.** I24 04 says `validate.py` "treats its first argument as the filename" so `--registry` is unsupported. That was true, and `negative-fixtures.md` had told readers to "call `validate(registry_path)`; A will add the flag"; **that function never existed.** The flag now does, and the sentence is gone.

**Scope statement rewritten, one scope only.** Portfolio input is now stated as **in scope** on a single basis: it is optional, it enters the run only after explicit confirmation, and `FR-002`/`FR-003`/`FR-004`/`FR-006` state their obligations for both inputs. Profiles `A-A`/`A-B`/`A-C` are described as existing so each obligation runs under the input it needs. **`TraderProposal.position_sizing` is recorded as a model suggestion carried in the report, not a validated size** — this keeps the research-only boundary while matching what the implementation actually produces. Whether a conditional sizing suggestion should be permitted at all is **open item 15**, the review's own question, and A does not decide it alone.

**Deadline noted, and one thing A will not do.** The review states the deadline as **25 November 2026, 23:59 Hong Kong**. A's remaining obligation from §4 item 1 is to publish the reconciled snapshot under `docs/req/`; E's is to wire the gate. **A will not describe any gate as enforced, and will not sign an adoption record, on the strength of a deadline.**

---

## 2026-11-24 — two token series disagree in direction; a comparability clause added

The integration review (I24 05) reported **+6.8%** tokens (138,897 → 148,392) measured through `graph.propagate()`. A later optimisation series reported **−24.8%** (to 104,459) measured through `graph.run_transient()`. Same ticker, same date, same model, same week. A checked the code rather than picking a side.

**The entry point is not the cause.** `propagate()` and `run_transient()` both call `_run_graph`; they differ only in a `persist` flag that gates a state write and a memory-log append, neither of which makes a model request (`memory/log.py` says so explicitly: "No LLM call"). Choosing one over the other does not move token counts.

**One indirect difference is real but small.** `persist=True` appends the decision to the memory log; the next run reads it back and `portfolio_manager.py` inserts it into the Portfolio Manager prompt as prior-decision lessons. The newer series pins `memory_log_path` to an empty file, so its Portfolio Manager never receives that context. **That is one call out of ~17 (9,191 tokens, 6.3%), and cannot account for a ~44,000-token gap.** Presenting it as the explanation would be false; it is recorded as a difference that exists, with its size stated.

**What A did not claim.** That either series is wrong, that the fall is real, or that D's harness used a populated memory log — D's harness is untracked, and whether it did is **unknown**, which is written down as unknown.

**What changed in the registry: one clause, no numbers.** `REQ-TA-NFR-COST-001` now says `TOKEN_BUDGET` may be set only from measurements that hold six settings constant — entry point, analyst set, debate round counts, ticker and analysis date, model and provider, and memory-log state — and that a measurement record must name all six. **`TOKEN_BUDGET` remains unset** (`to be measured`, owner D). The clause creates no budget and endorses no figure.

**Two figures in the newer series flagged for care, from its own record.** `−35.0%` divides by `160,826`, a single unoptimised control at the top of the observed range (137,223–154,514); `−24.8%` divides by the two-run 138,897 baseline and is the better-founded figure, though it too spans two memory-log conditions. The series' first round (121,207 → 82,971) was discarded **by its own author** because price data was unavailable — recorded here as correct practice.

---

## 2026-11-24 (later) — a 120,000-token budget was proposed; the form is adopted and the number is not

Member E proposed **120,000 total tokens per run** from three measurements, 99,532 / 103,120 / 110,725 (highest + 8.4%), together with a reference configuration and an explicit rule that missing usage must not be read as zero. A adopted what needs no number and declined the figure. **Both halves of that sentence are recorded here, because the second is the one a reader should check.**

**What was adopted into `REQ-TA-NFR-COST-001`.** (1) The budget counts **input and output** tokens cumulatively across every model call — tool-selection, analysts, both debates, structured-output re-requests, free-text fallback, reported retries — not per call and not input-only; `max_tokens` is a different control. (2) **Reserve before dispatch:** an attempt is dispatched only if its input plus its maximum permitted output fits the remaining budget, because counting after the call returns cannot bound concurrent branches, retries or output allowance. (3) The `INCOMPLETE` / `stop_reason: BUDGET` contract. (4) **Usage availability:** missing usage is `UNKNOWN`, is never summed as zero, and its reservation is retained — the existing rule that an `UNKNOWN` run is not stopped is unchanged, but `UNKNOWN` now spends budget instead of being free. (5) A stated **scope**: the budget binds the reference configuration, and extending it to every ticker, date, analyst set and portfolio mode is a product decision that needs a wider test population. The fit gained five offline cases (within budget, exhaustion, four-way concurrency, no usage metadata, re-request plus fallback), and `metric`, `threshold` and `verification` were restated to match.

**Why the number was not written.** Not a preference: the provenance does not support the comparison the budget needs.

- **All three figures are optimised runs.** The optimisation E authored is the change merged as **PR #18**, and it is already in `main`. The second control, 160,826, is one **unoptimised** run from the same session; the first baseline was two runs averaging 138,897.
- **The proposed reference configuration names the optimisation as on.** A budget measured that way caps the optimised build against itself: a later change could give back much of the saving and still pass. The entry's own comparability clause requires an identical baseline and candidate, and none of the six settings names whether the optimisation is on.
- **The measurement record is not in the repository.** `AI-log/Member-E/2026-11-24_token-input-reduction.md` reached `main` and is the index A read; the measurement record and the raw per-run artifacts did not, so the per-run settings could not be checked against run artifacts.
- **The entry point is not pinned by the name.** `run_transient` is the graph-level `persist=False` form of `_run_graph`; whether the optimised runs reached it through the run API is not recorded. The supported harness, `tests/member_d_verification/token_input_benchmark.py`, is **scripted and unoptimised** — it stubs the tier client — so it can prove the mechanism offline but cannot supply the live before/after pair.

**A provisional figure, labelled as A's derivation, not a measurement.** For the **unoptimised** baseline, 152,000 tokens (about 90% of the single unoptimised control 160,826, rounded up so that a good run is not refused). It is recorded in the tradeoff line and **not applied**: one compliant optimised run already measured 110,725, so the value holds only for the configuration it was derived in, and its internal consistency was never verified. **`TOKEN_BUDGET` stays `open`**, with the proposal visible in its `value` text as "candidate 120000 … not applied".

**Status, stated exactly.** Proposed, **not enforced, not validated**. Three figures below 120,000 are on record; no result shows the system can hold the bound under concurrency, retries or output reservation.

---

## 2026-11-24 (later) — the third copy of the blanket non-null rule, found after PR #20 merged

Brian's second point was that the acceptance wording demands every result field be non-null although completed runs have no stop reason and incomplete runs have no rating. The statement and fit (b) of `REQ-TA-NFR-REPRO-001` were corrected on 2026-11-24 and merged in PR #20. **The `threshold` field of the same entry was not corrected and still read "every listed field non-empty".** That is the same contradiction in a third place, and a reviewer reading only the threshold would still find it.

The threshold now checks fields against RUN-001's validity table: an `INCOMPLETE` record carries a stop reason and no rating, a `COMPLETED` record carries a rating and no stop reason, the six always-present identifiers are non-null, 0 records invent a value to fill a slot, and 0 records change after publication. **No fixture count changed and nothing is claimed about the current build.** The correction is dated in the entry's `baseline` and `note`, not applied to `requirements-draft-v4.md`, which remains a read-only recorded artefact.

**The validator did not catch it, and is not claimed to have.** It checks that references resolve, not that a `threshold` agrees with a `fit_criterion`. This was found by reading the entry, after the merge.

---

## 2026-11-24 (later) — `UNKNOWN` added to the validator's controlled vocabulary

`UNKNOWN` already occurred in `REQ-TA-NFR-COST-001` before this change and passed, because the validator's parameter scan only matches tokens shaped like a tuning parameter (`*_CAP`, `*_BUDGET`, …). It does not match a bare `UNKNOWN`. The entry is recorded in the validator's `VOCABULARY` set anyway, next to the stop reasons and output-check outcomes, so that the value is named where the other controlled values are rather than relying on a regex that happens not to fire. **No rule changed, and no previously passing registry outcome changed.**


---

## 2026-11-24 (later) — external review found five defects; all five confirmed and fixed

An external reviewer (`architecture-extension-review-2026-11-24.md`, plus two chat messages) reported five problems in this package. **A checked each one against the files rather than the report, and all five were accurate.** None is disputed here.

### 1. Incorrect IDs in the scope statement

The scope said `REQ-TA-FR-002` (consent), `REQ-TA-FR-003` (freezing and fingerprint), `REQ-TA-FR-004` (channels) and `REQ-TA-FR-006` (provenance).

`REQ-TA-FR-002` is a **withdrawn GUI entry**. Worse, the whole label set was misaligned: `FR-003` is checkpoint list/resume, `FR-004` is point-in-time evidence, `FR-006` is freshness thresholds, and `FR-007` is rating meaning. Only `FR-001` matched its label.

**Checking the substance turned up a real gap, not just a typo.** No active entry owns the portfolio **confirmation flow** — the confirm/decline/EOF prompts and the event they emit. `REQ-TA-INV-014` requires that confirmation authorizes the frozen selection, but nothing defines the gate itself. The scope now says so and records it as **open item 16**, instead of citing a withdrawn GUI ID. Appendix A's assignment table was rewritten against the real titles.

The reviewer's second half — "other references mix older `SEL-TA-*` meanings with current `REQ-TA-*` IDs" — was checked and **not reproduced**. The three `SEL-TA-*` mentions (`GOV-002`, `GOV-004`, `GOV-005`) are each a stated crosswalk or naming warning, and each names the correct counterpart. Recorded here so the difference between the two halves is visible.

### 2. Broken enforcement references

- **`REQ-TA-INV-012` was cited four times and does not exist.** `INV-009`…`013` were deliberately held back pending D's answer to Q-8d, and the registry kept referencing one of them. Every citation now names architecture `INV-14`, which is where the persistence-failure rule actually lives, and says plainly that it is **not yet registered as a `REQ-TA-*` entry**. `INV-011` had the same problem in `INV-014`'s tradeoff and is fixed the same way.
- **`INV-014.enforced_by` pointed at itself**, which names no enforcer. It now points at `REQ-TA-FR-001`, the evidence-record component that enforces a frozen selection and fingerprint.
- **`GOV-004.enforced_by` pointed at `REQ-TA-GOV-003`**, the AI-use-log gate — a different obligation. The enforcer is `docs/req/validate.py` plus a CI job, and neither is a requirement, so `enforced_by` is **omitted** and the entry's note states why. Naming a requirement there would have misstated the executor either way.

**The root cause was the validator, not carelessness.** Rule 4 walked only the structured fields; an ID quoted in prose was never resolved. That is why four dangling citations passed 36/36 with zero warnings. See item 4.

### 3. Remaining acceptance inconsistencies

`REQ-TA-NFR-REPRO-001`'s statement began "Every run that returns a logical result… shall write exactly one run record", while the same entry exempts a run whose critical artifact fails to publish. The statement now reads "…and successfully publishes its artifacts", and the threshold states its denominator: *among runs whose record and report were successfully published*, 100% carry exactly the fields RUN-001's validity table requires, and a run that fails during staging or commit is excluded from the denominator and must instead not report the artifact as written.

The configuration-comparison and token-comparability wording were reviewed against this same standard; the six named settings and the before/after-pair rule were already stated, and no contradiction was found. **That half of the report is recorded as checked, not as changed.**

### 4. Validator gaps — and the reason they existed

Three mutations were reported to pass. All three did.

| Mutation | Why it passed | Fix |
|---|---|---|
| Delete `STALE_PRICE_DAYS` | The scan read only `statement`, `fit_criterion`, `threshold`; the regex was `[A-Z][A-Z0-9]*_(suffix)` — **one prefix segment only**, so `STALE_PRICE_DAYS` never matched | Regex allows multi-segment prefixes; scan widened to 9 fields |
| Delete `STALE_STATEMENT_DAYS` | Same | Same |
| Delete `N_EVAL` | No `_EVAL` suffix in the pattern at all | `_EVAL` added |
| Delete `requirements` key | The line indexed `doc["requirements"]` directly | Guarded; prints a named finding instead of a traceback |

A fourth gap was found while fixing these: **nothing checked the reverse direction.** Deleting a parameter row whose text citation no longer matched any pattern left a declared-but-unused parameter invisible. Rule 18 now compares each parameter's `used_by` against where its text is actually cited, and fails on a mismatch.

That mismatch check immediately caught two real errors A had not noticed: `QUALITY_THRESHOLD` was listed as used by `REQ-TA-GOV-001` only, though `NFR-COST-001` and `NFR-EVAL-001` also cite it; `N_EVAL` omitted `NFR-EVAL-001`.

**Four new negative fixtures** were added (22–25) for exactly these cases. The suite is now **27**, all failing for their stated reason.

**One exemption was added rather than a silent pass.** `MAX_OHLCV_STALE_DAYS` is `tradingagents/dataflows/vendors/yahoo/ohlcv.py:18`, a code constant quoted in FR-006's baseline to show the price rule already exists upstream. It is not a tunable this registry owns; the registry's own knob is `STALE_PRICE_DAYS`. Recorded in `PARAM_EXEMPT` with that reason.

### 5. Implementation follow-ups — confirmed, unchanged, still open

Both are correct as reported and neither is fixable from this package alone:

- **The dangling-reference boundary still reproduces on `main`.** The four `INV-012` citations were in the merged registry. This branch fixes them; `main` keeps them until it merges.
- **Schema validation is not wired into CI.** No workflow under `.github/workflows/` references `docs/req/validate.py`, so `REQ-TA-GOV-004` states an obligation nothing enforces. Its note already said this at `916d8a6`; it now also records the state at 2026-11-24. Wiring it is a CI change and is **not** made here.

### Verification actually run

```
python3 docs/req/validate.py                36 requirements; 3 withdrawn; 0 error(s), 0 warning(s)   exit 0
python3 docs/req/negative-fixtures-check.py all 27 negative fixtures fail correctly                   exit 0
ruff check .                                All checks passed
rebuild_registry.py                         output byte-identical to the committed YAML
mutation sweep                              all 8 parameter deletions + requirements key: exit 1; unchanged: exit 0
```

`requirements-draft-v4.md` is untouched (read-only recorded artefact, SHA-256 `542f382c…`). The changes go through dated overrides in `rebuild_registry.py`; `requirements.yaml` was regenerated, never hand-edited.
