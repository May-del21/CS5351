# Requirement source notes (D1)

**Owner:** Member A.
**Purpose:** Record where each requirement came from, what was observed in the existing system, and which questions remain open. Every claim here is traceable to a named document or a named file, and observations about the codebase are marked with the version they were made against.

Nothing in this file is a requirement. Requirements live in `requirements.yaml`.

---

## 1. Documents that fed the requirement set

| Document | Role | Disposition |
|---|---|---|
| `requirements-draft-v2.md` (SHA-256 `5742540b7b614487082ba399b7a5b33e17f0d24c7e87a88fa69827a6aa62519f`) | The reviewed baseline: 25 active + 3 withdrawn | **Adopted as the text baseline**; amended in three entries by D-1/D-2/D-3 |
| `requirements-draft_problems.md` | Team review comments that produced v2 | Applied in the v2 entry of the change log |
| `requirements-v2-review-2026-11-12.md` | Independent review, 28 findings V2-01…V2-28 | Findings only. Accepted in part (see §3). Not adopted as requirements |
| `architecture-blueprint(1).md` | Member B's architecture, with 13 conflicts O-01…O-13 | Input to feasibility, not a requirement source |
| `reconciliation-2026-11-20.md` | Member B candidate: 21 `SEL-TA-*` requirements | **Not adopted.** See OQ-2. Input only |
| `reconciliation-background-2026-11-20.md` | Broader Member B background | Superseded by the above, by its own statement |
| `project-deliverables-and-ownership.md` | Course-aligned deliverables and ownership | Defines A's D1 file set and A's boundary |
| `Le-kk/CS5351@c0081cb` (the team repository) | The actual submission baseline | **Authoritative for every baseline observation.** Re-verified 2026-11-23; see the change-log entry of that date. `May-del21/TradingAgents@9fa1196` is *not* the submission repository. |
| `docs/architecture/invariants.md` (in the team repository) | Member B's INV-01 … INV-14 | A's entries map to B's by crosswalk, not by authority: A owns meaning and fit, B owns enforcement and fallback. See OQ-7 |
| `tradingagents-requirements-v0.7.1.md` | Earlier requirements draft on v0.7.1 | Superseded by v2 |
| `Problems inspected by Yifeng in original trading agents and suggest requirements.docx` | Member's source inspection of v0.7.1 | One input that led to the research-only direction |

**Course documents consulted (held locally, 2026-11-22):**

| File | Role |
|---|---|
| `CS5351-2026-2027-project.pdf` | The authoritative deliverable specification. Pages 3–10 used. Page 5 is the D1 text; page 9 is the required repository structure; page 10 is the blocking-gate list. |
| `cs5351-introduction.pptx` | Slide 24 repeats the repository structure; used as a cross-check of page 9. |
| `cs5351-2026-2027-process.pdf` | Teaching material on the SE process. Contains no deliverable specification for D1; not used as a requirement source. |

Earlier versions of this file said these were not held by A and treated the ownership document's summary as the only course evidence. **That was wrong** — the PDFs were in `~/cityu/e_CS5351/` all along. The quotations below are from the PDFs themselves.

---

## 2. Observations in the existing system (TradingAgents v0.7.1)

Checked against the local tree at git HEAD `9fa1196fffbcfd9de5146d2dd2869df84ab99838`, `tradingagents.__version__ == "0.7.1"`.

| Observation | Where observed | Requirement it informs |
|---|---|---|
| Analysts fan out concurrently from `START` alongside the memory node | `tradingagents/graph/setup.py` | NFR-COST-002 (concurrency makes a naive cap check unsafe) |
| `llm_max_retries` is forwarded to the provider SDK; SDK-internal retries are invisible to the application | `tradingagents/llm_clients/factory.py` | NFR-COST-002 (why the bound is stated with a branch allowance) |
| `_NOT_IN_SIGNATURE` excludes retry settings from the run signature | `tradingagents/graph/trading_graph.py` | NFR-REPRO-001 (retry settings do not change run identity) |
| 4 direct imports of `dataflows.vendors.*` inside agent modules | `tradingagents/agents/**` | ARCH-001 |
| `MAX_OHLCV_STALE_DAYS = 10` | `tradingagents/dataflows/vendors/yahoo/ohlcv.py` | FR-006, `STALE_PRICE_DAYS` |
| `VENDOR_METHODS` and `route_to_vendor` exist as a single routing point, with sentinel values for failure | `tradingagents/dataflows/router.py` | ARCH-001, FR-005 |
| Per-node SQLite checkpoints keyed by a run signature; no list command and no explicit rerun command | `tradingagents/graph/checkpointer.py` | FR-003 |
| The Portfolio Manager produces a rating; portfolio handling (NH-1…NH-5) already exists on input | `tradingagents/portfolio.py`, `tests/test_portfolio_context.py` | Scope decision A-3 (retained in code, unclaimed by requirements) |
| No run-scoped counter, deadline or call budget anywhere in the application | search over `tradingagents/` | NFR-COST-002, NFR-PERF-002 |

These observations describe what exists. They are **not** claims that any requirement is met.

---

## 3. Disposition of the v2 review (V2-01…V2-28)

The review returned 28 findings. Not all could be checked against the local tree, but these were checked against the v2 text itself:

| Finding | Subject | Disposition in the final set |
|---|---|---|
| V2-04 | No coverage code describes a channel no analyst requested on a completed run | **Open in v2 → fixed by D-1** (`NOT_REQUESTED` added to FR-005) |
| V2-07 | Resume versus "one immutable record per run" was unspecified | **Partially addressed in v2 → ruled by D-5** (run/attempt two-level identity) |
| V2-08 | REPRO-001 required two records differing in exactly one config key while also requiring unique run IDs and timestamps | Fixed in v2 (the comparison rule now names the key difference explicitly) |
| V2-09 | RUN-001 required non-null fields while its own presence rules made some conditional | Fixed in v2 (a "Present when" column per field) |
| V2-10 | EVAL-001 rule 5 forbade every before/after comparison GOV-001 needs | **Open in v2 → fixed by D-2** (repeatability and controlled-change modes) |
| V2-01 | Forced Neutral when no sentiment data exists could read as a passed judgement | Not amended in this decision; FR-008 R6 already treats "no usable source" as forcing the Neutral band and a blocking condition, so the case is disclosed rather than silently passed. **Remains a wording risk for C to test** |

The remaining findings were either accepted into v2 before this decision or are outside A's authority (they concern test procedure, which is C's). This table records only what A decided; it is not a claim that the review is closed.

---

## 4. Sources behind the three amendments

| Decision | Source of the problem | Source of the fix |
|---|---|---|
| D-1 | Review finding V2-04; v0.7.1's `selected_analysts` allows a subset of analysts | A's decision: add one honest code rather than relabel "not asked" as "unavailable" |
| D-2 | Review finding V2-10; GOV-001 needs to score a changed prompt | A's decision: split comparison into repeatability and controlled change |
| D-3 | A's own analysis of concurrency and SDK retries; independently consistent with Member B's "reserve before dispatch" language | A's decision: state a provable bound and require reservation ordering, leaving the mechanism to B/D |
| D-5 | Review finding V2-07 | A's decision: two-level identity with immutable per-attempt records |

---

## 4b. Course-format compliance review (2026-11-22)

After obtaining `CS5351-2026-2027-project.pdf`, the registry was re-checked line by line against page 5's D1 text. Three gaps were found and fixed.

| Course sentence | Gap found | Fix |
|---|---|---|
| "Types cover functional behavior, **invariants (non-negotiable rules with zero-tolerance fit criteria)**, quality attributes, performance, cost, governance, and security." | No requirement had `type: invariant`, although ARCH-002 already carried eight zero-tolerance rules R1–R8. | Promoted R1–R8 to `REQ-TA-INV-001`…`008` (Must, `zero_tolerance: true`, `enforced_by: REQ-TA-ARCH-002`). Total 25 → 33. |
| "Non-functional requirements are expressed as **metric + threshold + verification**." | The three were merged into one `fit_criterion` sentence; CI could not check their presence. | Added structured `metric`, `threshold` and `verification` fields to all 10 non-functional entries; the schema requires them by type. |
| "Requirements discovered through analysis of any existing system or repository are included and **linked to their sources**." | All 25 entries had a `baseline` observation, but 0 had a `baseline_observation` source link. Every `source` pointed only at the previous draft. | Extracted file paths from each `baseline` field, resolved every one against the real tree, and emitted `baseline_observation` links. Where an observation names no single file, the link records the review of HEAD `9fa1196f` explicitly rather than inventing a path. 26 entries linked. |

The generator refuses to write if any path named in a `baseline` field does not resolve to a real file, and refuses if a bare filename resolves to more than one file. This prevented four guessed paths from entering the registry.

`validate.py` now enforces all three course rules, and each was confirmed by a negative test that fails as expected.

## 5. Open questions

**OQ-1 — One YAML or two? — CLOSED 2026-11-22.**

The authoritative text settles it. `CS5351-2026-2027-project.pdf` page 5:

> Produce a machine-readable product requirements document and a consolidated requirements registry, **both in YAML**, under `./docs/req/`

and it then names exactly two files there, only one of which is YAML:

> - `docs/req/requirements.yaml` — every requirement as an entry ...
> - `docs/req/req-schema.json` — the schema used by CI in GitHub to validate the registry as a date.

Page 9's required repository structure lists the same two files and nothing else under `docs/req/`, and slide 24 of `cs5351-introduction.pptx` repeats that structure. Three independent places agree.

**Decision:** one `requirements.yaml` serves as both the machine-readable PRD and the consolidated registry. No second PRD YAML is required. The `scope.prd_narrative` field is retained because it states this basis in the artifact itself.

The ownership document's "A/E should confirm" was written without the PDF in hand; the evidence makes confirmation unnecessary. This is a reading of the course text, not an instructor statement.

**OQ-2 — Which repository? — ANSWERED 2026-11-23, with a correction to A.**

Member B's reply reports inspecting `Le-kk/CS5351@56bbe29` and finding `tradingagents/runapi/result.py` there; E's integration merge `c0081cb` reportedly has identical content. **The team repository is therefore `Le-kk/CS5351`, not `May-del21/TradingAgents`.**

A's earlier conclusion in this file — that B's reconciliation described "a different codebase" and that `runapi/`, `checks.py`, `OutputChecker` and `Q1–Q4` do not exist — **was true only of the tree A was reading** (`May-del21/TradingAgents@9fa1196`) and the inference drawn from it was wrong. B did not err; A was reading the wrong repository. Those statements are retained above as a record of what was checked, and must be read as scoped to `9fa1196`.

**Consequence:** every baseline observation in `requirements.yaml` was verified against `9fa1196`. Any item whose file has moved or changed under `56bbe29` must be re-checked before D builds against it. A has not yet inspected `56bbe29`, so this re-check is outstanding, not done. `May-del21/TradingAgents` should not be treated as the submission repository.

**OQ-3 — GOV-002 approval record format. — CLOSED 2026-11-23 on Member E's reply (Q1–Q4 + E13).**

A opened this because GOV-002's fit criterion compared timestamps, and a commit author sets their own author date, so a rebase could satisfy the check without a real approval.

**What E answered, and A verified.** E checked the course PDF: page 10 gate 1 reads "no code change merges unless the tests for the change were approved before implementation began", and pages 6 and 7 require approval before code generation for the transcript and launch-prompt deliverables. A read those pages directly and confirms the text. So the gate is real and is not deleted.

**E withdrew its own earlier proposal.** On 2026-11-23 E had proposed replacing prior approval with post-implementation CI receipts. E has since withdrawn that, and will implement the approval gate. The replacement wording is recorded as **withdrawn, not adopted**.

**Record format (now stated in GOV-002).** One YAML per approval under `docs/verification/approvals/`, uniquely named, superseded evidence preserved. Fields: `approver`, `approver_role`, `approved_at` with timezone, `plan_ref`, `plan_sha256`, `scope`, `approval_evidence_ref`, `approval_commit`. A bot file is never human approval.

**A's own error, corrected.** A had argued that the fix for the timestamp weakness was **commit ancestry**, and intended to restate the criterion that way. E's answer is narrower: ancestry is the repository-ordering check only. It proves neither that coding began later nor that a human approved the tests, and the requirement and the evidence must not claim it does. The criterion now says exactly that.

**Status.** `proposed`, not `implemented`: E states the mechanism and its positive/negative checks are not built. Neither E's reply nor the course citation is the team's adoption record.

**Known gap, disclosed.** `SEL-TA-GOV-001` in the team's working selection says the same thing. The two are the same obligation under two numberings; neither is evidence that any feature's plan was approved. Historical work without a record is an evidence gap, not a retrospective approval.

**OQ-4 — Parameter values.**
`RUN_TIME_CAP`, `TOKEN_BUDGET`, `CALL_CAP`, `QUALITY_THRESHOLD` and `STALE_STATEMENT_DAYS` are marked provisional or open in `parameter_appendix`. A does not invent them; D measures and A fixes. Status: open, owner D then A.

**OQ-5 — Whether COST-002's bound is achievable. — ANSWERED 2026-11-23.**

Member B's reply answers all four questions. A verified the technical claims (`openai_client.py:213` forwards `max_retries`; `setup.py:160-166` and `trading_graph.py:56` confirm 5 default START branches) and adopted them as A's requirement wording.

**Outcome:** the bound tightened to `dispatch_attempts <= successful_reservations <= CALL_CAP`, the branch allowance withdrawn, single-use reservations required, and (c)/(d) rewritten with an injected-barrier race and an explicit `output_check = NOT_RUN`. `COST-002` stays **Must**.

**Residual, not closed:** B's reply carries no signature and A has not seen D's agreement. The mechanism is a recommendation for D to assess. `COST-002` remains `proposed`, and if D cannot make (a)-(d) hold on every enabled client, A downgrades it to Should and restates it as detection-only.

**OQ-6 — `stop_reason` vocabulary conflict. — CLOSED 2026-11-23 (decision: extend to six).**

Member B's report was confirmed firsthand. In `Le-kk/CS5351@c0081cb`, `tradingagents/runapi/result.py:12-14` held:

```python
StopReason = Literal[
    "MODEL_FAILURE", "DATA_FAILURE", "INTERNAL_ERROR", "PERSISTENCE_ERROR", "INTERRUPTED",
]
```

`RUN-001` specified three: `DATA`, `MODEL`, `BUDGET`.

**Decision (A, 2026-11-23, revised after B's reply): six values** — `MODEL_FAILURE`, `DATA_FAILURE`, `BUDGET`, `INTERNAL_ERROR`, `PERSISTENCE_ERROR`, `INTERRUPTED`. `RUN-001` uses the implementation's existing spellings; `MODEL` and `DATA` survive only as human-facing labels.

Why six and not three: a three-value table has no row for `PERSISTENCE_ERROR` or `INTERRUPTED`, so the requirement would be false for a stop the typed contract already represents. The other option — mapping the extras onto `MODEL_FAILURE` — was rejected because `PERSISTENCE_ERROR` is not a model failure.

Why the existing spellings (B2, B, 2026-11-23): A had required `DATA`/`MODEL`. B rejected the rename — "a rename would be a breaking serialized-value change for consumers and validators expecting the current vocabulary" — and named the cost: 23 code/test sites and 9 documents, including C's `score_gov004.py:57` `STOP_REASONS` set, which would silently reject renamed runs. A accepted and changed the requirement instead. `BUDGET` is now the only addition.

**What this costs, and it is D's work, not A's:**

**Corrected 2026-11-23.** A had written that "the repository holds real `INCOMPLETE/PERSISTENCE_ERROR` and `INTERRUPTED` records". B checked and A re-checked: **it does not.** All 15 deduplicated attempts in `docs/reviews/evidence/live-verification-2026-11-21/` are `COMPLETED` with `stop_reason` null; the 40 null stop reasons in that package are 15 cases plus mirror objects. Persistence and interruption behaviour rests on the typed contract and offline fault/interruption tests, not on that live cohort. The requirement's justification is unaffected — the contract represents those stops and a three-value table cannot — but the earlier sentence was wrong and is corrected rather than deleted.

**B also separated two things A had merged.** `INTERRUPTED` is a real stop; D-5's "resume keeps `run_id` and adds an attempt" is a *different* contract change that conflicts with INV-11/INV-12. B did not approve D-5 through the vocabulary reply. D-5 stands as A's decision but is tracked open under OQ-8.

| Item | State |
|---|---|
| `BUDGET` in the enum, `finalize`, `reporting`, result validation | **Not implemented.** `grep BUDGET tradingagents/runapi/` returns nothing. B: adding an enum value is not automatically supported by any existing reader; each must be updated or it rejects the new value. |
| `BUDGET` runtime-policy row | B proposes **R17** (catalog currently ends at R16, and `R17` is unused) and will not renumber existing rows. B keeps the trigger in RUN-001 as well; the two are complementary. |
| Suppression hazards | B names them: broad handlers in `agents/structured.py`, `memory/settlement.py` and the graph memory step must not hide a refusal. The refusal must be recognised before the generic classifier. |
| Spelling change `MODEL_FAILURE` → `MODEL` | **Withdrawn 2026-11-23 (B2).** B: a rename is a breaking change to a serialized public value; 23 code/test sites and 9 documents consume it, including `score_gov004.py:57`'s own `STOP_REASONS`. A accepted. The requirement now uses `MODEL_FAILURE`/`DATA_FAILURE`; `MODEL`/`DATA` are human-facing labels only. `BUDGET` is the sole addition. |
| Mapping rule | `RUN-001` now states it: budget exhaustion must be `BUDGET` and must never be relabelled `INTERNAL_ERROR`; `INTERRUPTED` covers cooperative cancellation and pairs with D-5's resume rule. |

The values are named in the requirement; the implementation is not. `RUN-001` stays `proposed`.

**Checked and correct:** `runapi/finalize.py:classify_exception` handles `KeyboardInterrupt` and `InterruptedError` explicitly before the substring matching, and an `AuthenticationError` maps to `MODEL_FAILURE`. A initially claimed the `INTERRUPTED` path was unreachable, ran it, and was wrong; the entry was corrected rather than left standing.

**OQ-7 — Two invariant registers. — CLOSED 2026-11-23, then REVISED the same day after B's reply.**

`docs/architecture/invariants.md` in the team repository defines INV-01 … INV-14 with source, statement, enforcing component, verification method, runtime monitor and fallback. A promoted `REQ-TA-INV-001` … `008` from ARCH-002's R1–R8 rules (A-10) without knowing this file existed, because it is not in `9fa1196`.

**First decision (A, 2026-11-23): B's register is authoritative.** Superseded. B answered (B6–B8) that this is wrong in the direction A chose: "an architecture draft should not automatically override a different requirement or erase it through an incorrect pairing."

**Revised decision (A, 2026-11-23, after B's reply): split by layer.** A's YAML owns the requirement meaning and the zero-tolerance fit criterion; B's register owns architecture enforcement, runtime monitor and fallback; neither overrides the other. B's own words: "Keep both deliverables… Avoid conflicting duplicate meanings, not the necessary requirement-to-design trace."

B's corrected crosswalk, now recorded per entry in `requirements.yaml`:

| A's entry | B's entries | Relationship | Deterministic rule | A's disposition |
|---|---|---|---|---|
| INV-001 unreadable rating | INV-08, INV-03 | partial | Q1 | **Restated** so it claims only that `PASSED` is never claimed for `REVIEW`; it no longer implies every completed run yields a usable rating. |
| INV-002 cited ID resolves | none | none | none | Kept. An adopted obligation nothing enforces. |
| INV-003 no ownership phrase | INV-02, INV-13 | partial | none | Kept; A proposes narrowing to assertions grounded in supplied facts, pending B naming the boundary. |
| INV-004 sentiment band | none | none | none | Kept. B asks for the band definitions and enforcing component. |
| INV-005 confidence cap | none | none | none | Kept. B: do not claim INV-13 enforces it. |
| INV-006 no direction without data | none | none | none | Kept, scope narrowed: sentiment band only, never forces the final rating to Hold. |
| INV-007 coverage section equals record | none | none | none | Kept. Needs a separate definition, enforcer and negative test. |
| INV-008 disclaimer, no guarantee | INV-03 | partial | Q3, Q4 | Kept. |

A had grouped INV-004…007 under INV-13. B: that is not equivalent coverage — INV-13 is about ownership, role labels and Hold/REVIEW semantics, none of which is a sentiment-range, confidence-cap, availability-gate or coverage-equality check.

**Also accepted from B:** keep separate machine-readable entries rather than one pointer (B7); no literal `zero_tolerance: true` key is mandated, so the metric/threshold 0/scope/verification fields carry the meaning (B8); the eight rules are not the complete architecture invariant set, so consent, privacy, snapshots, shared entry and publication must be covered too — see OQ-8.

**A's own error, found while checking B's claim.** B wrote that `R1`–`R8` are the checker rules. In the team's documents they are not: `docs/architecture/runtime-policy-catalog.md` uses `R1`–`R16` for unrelated trigger rows (its `R1` is a provider failover), and `runapi/checks.py` emits only `Q1`–`Q4`. The registry now says `R1`–`R8` always means the output-check rule set of draft v4. A also found that `R4`–`R7` rest on coverage, sentiment and intermediate-output fields that the requirement set defines and the checker does not inspect, and `R2` has no enforcer. All eight entries are `proposed` for that reason, not because of a status error.

**OQ-8 — Three obligations that no register currently owns. — OPEN, raised 2026-11-23.**

1. **Architecture invariants beyond the eight.** B: "Also cover the other adopted architecture obligations, including consent, privacy, immutable snapshots, shared entry and publication." `FR-002` (consent), `SEC-002` (privacy), `NFR-REPRO-001` (snapshots/publication) and `ARCH-001` (shared entry) exist as requirements but no `REQ-TA-INV-*` entry covers them. Decision needed: add invariant entries, or state explicitly that D1's invariant coverage is satisfied by these requirements.
2. **D-5 versus INV-11/INV-12.** B: "INV-12 currently specifies a fresh run ID per invocation; INV-11 specifies one logical terminal per run. Reusing the same ID after publishing an interrupted result requires a distinct attempt identity, artifact/event scoping and explicit publication/aggregation rules." D-5 is unaffected as a user decision but is a separate contract change. Blocks nothing today; must be resolved before D builds resume.
3. **Precedence when two stop reasons occur together.** B: retain `PERSISTENCE_ERROR` as primary and the budget cause as secondary. Now written into `run001-tables.md` §Precedence rule; needs B's confirmation of that exact wording.

**OQ-9 — C cross-walk. — OPEN, C replied 2026-11-23.**

C: `SEL-TA-*` comes from `docs/req/selected-requirements.md`, which itself says "working selection authorized for architecture exploration by Brian; pending Member A/team approval as a final registry" (line 3, verified). C therefore cannot claim `SEL-TA-*` supersedes A's set or is the final acceptance baseline, and proposes reconciling the two sets, agreeing scope changes, then updating registry and mapping.

**C1 and C2 are answered.** C1 (rebuild or cross-walk): reconcile and agree scope first, then update both artifacts — A adopted this order. C2 (is `SEL-TA-*` authoritative): not as an approved baseline, but yes as the working and historical baseline C's tests were written against, which C stated and A will not drop. A first recorded this as "partly answered"; that was wrong and is corrected. C3–C10 remain open, and `SEL-TA-NFR-003` has no counterpart in A's ID space.

**OQ-10 — Is the CI pipeline itself a requirement? — ANSWERED 2026-11-23, partly.**

Member C's crosswalk question X4 asked whether the team's working-selection CI obligations (`SEL-TA-GOV-003`, `005`, `006`) should become requirements in A's registry. A had left them as repository process. Member E's E14 answers one of the three directly: the AI-use log gate is course page 10 gate 6 and should be a formal governance requirement. A has added `REQ-TA-GOV-003`.

Still undecided for A: `SEL-TA-GOV-003` (static analysis and regression gates) and `SEL-TA-GOV-006` (branch protection and default-deny file access) are also named on course page 10 and page 9 as D7 blocking gates. A has not yet added them, because E's answer covered only the AI-use log and A would rather take one ID at a time than sweep in three on one person's partial answer. Recorded honestly as open.

**Baseline check, 2026-11-23.** `.github/workflows/ci.yml` at `c0081cb` has three jobs — `test`, `smoke-install`, `lint` — and **no** AI-log gate, dependency gate, schema gate, semantic-evaluation gate or approval gate. `grep -rn "ai-log\|dependency" .github/workflows/` returns nothing.

**OQ-12 — Is schema validation itself a requirement? — CLOSED 2026-11-23: YES, on Member B's reply.**

Member B answered directly: the obligation must be explicitly represented by a machine-readable governance requirement with its own fit and trace links, and "CI implementation alone is insufficient". A had been holding this open to avoid sweeping it in on one person's objection; B's answer asserts the obligation rather than a preference, so A added **`REQ-TA-GOV-004`** at Must / `proposed`. Total 34 → 36 together with `REQ-TA-INV-014`.

**The old text below is kept as the record of why it was open.** It no longer describes the current state.

B objected to the crosswalk row that mapped the team's `SEL-TA-GOV-002` ("registry validates against its schema") to `REQ-TA-GOV-001` plus `validate.py`. B is right on both counts: `REQ-TA-GOV-001` is the semantic-suite requirement, and a validator script is not a requirement. A has **withdrawn** that mapping and left `SEL-TA-GOV-002` as `B-only as a requirement`.

The substance is real: course page 10 lists schema validation as a blocking gate, and `validate.py` is the candidate enforcement. What is undecided is whether the registry must carry an entry for the gate, as `GOV-003` now does for the AI-use log, or whether the gate is satisfied by the command running in CI. A is asking C as crosswalk question **X7** rather than deciding it alone, because adding an entry on one objection would repeat the mistake of sweeping in `SEL-TA-GOV-003`/`006` on one partial answer.

**Status: open.** No requirement added; count unchanged at 34.

**OQ-13 — Input scope. CLOSED 2026-11-24, on one basis: portfolio input is IN scope.**

It had been left "for team adoption". That was not neutral: the published `scope.statement` said portfolio files were outside project scope and every fixture ran without one, while Appendix A required a confirmed snapshot for profiles `A-B` and `A-C`, and the implementation accepts one. An independent review (I24 02) called this what it was — **two contradictory scopes in one document**, not an open question.

The resolution, which A has made and offers for the team to reject: **an optional user-supplied portfolio snapshot is in scope.** A run without one and a run with one are both in scope; a supplied snapshot enters the run only after explicit confirmation; `FR-002`, `FR-003`, `FR-004` and `FR-006` each state their obligations for both inputs. The research-only boundary is preserved by what the system does **not** claim: it places no orders, assumes no account ownership, treats holdings as unverified user input, and does not validate position size or exposure. `TraderProposal.position_sizing` is recorded as a model suggestion carried in the report, **not** a validated size.

**Still open (item 15): whether a conditional sizing suggestion should be permitted at all.** The implementation produces the field; the research-only scope says no sizing is validated. A did not resolve this by deleting the field from a description.

**OQ-15 — What sets `TOKEN_BUDGET`? — OPEN, but the rule for accepting a figure is now CLOSED.**

Two measurement series exist for NVDA on 2026-01-09 and **disagree in direction**: D reports +6.8% (138,897 → 148,392, via `propagate()`), E reports −24.8% (to 104,459, via `run_transient()` with an empty memory log). A checked rather than chose: the entry points share one code path and differ only in a `persist` flag that makes no model request, so the entry point is not the cause; the memory-log difference is real but is one call of ~17 and cannot explain a ~44,000-token gap. Full reading in `token-measurement-comparability-2026-11-24.md`.

**Closed part:** what a figure must satisfy before it may set a budget. `REQ-TA-NFR-COST-001` now requires six settings to be held constant and named — entry point, analyst set, round counts, ticker and date, model and provider, memory-log state — and forbids deriving a budget or a saving percentage from a comparison where one differs unnamed.

**Still open:** the value itself, and which series is reproducible. That is D's measurement and E's control to settle; A will not set `TOKEN_BUDGET` from either figure as they stand.

**2026-11-24 (later) — a candidate figure arrived; the rule it must meet did not change.** E proposed **120,000 total tokens per run** (input plus output) from three measurements, 99,532 / 103,120 / 110,725, and supplied the reference configuration and an explicit "missing usage is not zero" rule. A read E's own AI log before writing anything, and the provenance blocks the number:

- **All three figures are optimised.** The optimisation is the change merged as PR #18 and is already in `main`. The control 160,826 is one unoptimised run from the same session; the first baseline was two runs averaging 138,897.
- **The reference configuration says the optimisation is on.** Measured that way, the budget caps the optimised build against itself, so a later change could surrender most of the saving and still pass. The comparability clause requires an identical baseline and candidate, and no setting names whether the optimisation is on.
- **The measurement record is not in the repository.** The AI-log index reached `main`; the measurement record and raw per-run artifacts did not.
- **The supported harness does not close the gap.** `tests/member_d_verification/token_input_benchmark.py` is a **scripted, unoptimised** measurement over `run_transient` — it stubs the tier client — so it can exercise the budget mechanism offline but cannot supply a live before/after pair.

**A adopted what needed no number and recorded the rest as a proposal:** total-not-per-call accounting, reserve-before-dispatch, the `INCOMPLETE`/`BUDGET` contract, `UNKNOWN` spending budget, and the narrower scope. `TOKEN_BUDGET` stays `open`, with "candidate 120000 … not applied" visible in its value. A provisional 152,000 for the **unoptimised** baseline is in the tradeoff line as A's derivation, not a measurement, and is not applied.

**What would close this:** one before/after pair under the identical named configuration, from the repository rather than a local harness, with the baseline and the allowance both recorded. Then the budget is baseline plus a stated allowance, and a later regression is detectable.

**OQ-14 — Which `GOV-004` is meant? — NAMED AND GUARDED, not closed.**

Two different things now answer to "GOV-004": the team's `SEL-TA-GOV-004` (the semantic-evaluation gate, which is A's `REQ-TA-GOV-001`) and A's new `REQ-TA-GOV-004` (registry schema validation). `docs/architecture/invariants.md` and `docs/architecture/risk-list.md` in the team repository use the first meaning; A's registry now uses the second.

A did **not** renumber to avoid this, because a gap in `REQ-TA-GOV-*` would read as a reserved or deleted ID and would be indistinguishable from the withdrawn-ID accidents this registry has already had. Instead both entries carry an in-text naming warning, and this note exists so that the collision is discoverable rather than silent.

**Open for the crosswalk:** C's X1–X6 review needs to state, per row, which numbering is meant. A will not resolve this by fiat.

**OQ-13 — Input scope: is the optional portfolio snapshot in range? — SUPERSEDED 2026-11-24; see the CLOSED entry above. The text below is the record of how it got there and still describes the fixture-profile defect accurately.**

B's point: "research-only output" does not imply "no portfolio input". The supported product accepts either no portfolio or a user-supplied snapshot, and that path's consent, validation, freezing and provenance behaviour is already implemented and tested, which is much of the team's engineering evidence.

**A's earlier position was wrong in form as well as substance.** The crosswalk said the exclusion "stands unless the team overturns it". The course requires contributors to *adopt* `./docs/req/`; an unadopted set can propose a scope but cannot settle one by silence. That sentence is withdrawn.

**A now proposes:** optional user-supplied portfolio input, with consent before any holdings payload moves, read-only source files, a frozen and fingerprinted snapshot, provenance naming the snapshot used, no orders and no broker or exposure claim. Exposure cap, sizing validation and the NH rules stay withdrawn and are not revived. This is a **proposed scope change requiring team adoption**, not a settled exclusion, and it is not A's to decide alone.

**Defect found in A's own document while answering this — FIXED 2026-11-23.** `requirements-draft-v4.md` line 577 pinned the offline fixture profile to `Portfolio | None (research-only scope)`, yet `test_nfr003_privacy.py` plants `UNRELATED_HOLDING_MARKER` as a second position and therefore needs a portfolio to pass. The declared profile and the privacy criterion contradicted each other. The offline profile is now split into **A-A** (no portfolio), **A-B** (snapshot, selected instrument absent) and **A-C** (snapshot with one unrelated holding), every active requirement is assigned exactly once, and the validator enforces it. **No fixture count was re-derived** — a changed population is a versioned acceptance change, not an appendix edit. Schema `1.1.0` → `1.2.0`, with `fixture_profiles` required. What the split does **not** do is decide the input scope: that is still OQ-13.

**What A did not do:** no existing input test was marked out of scope and no forward trace link was removed.

**OQ-11 — Delivery gap: the AI-use log format. — OPEN, owned by E.**

E's E15: original-language AI-use records already exist under `AI-log/`, but the course-specified `docs/ai-use-log.yaml` (course page 9, labelled D1) **has not been supplied**. A records it as an open delivery item and will not mark it complete because the directory exists. E will prepare the YAML as a structured index; A and the other members supply the selected records. Full annotated D5 transcripts remain a separate deliverable.

## 6. What A did not do

- Did not write an architecture decision, a test procedure or implementation code.
- Did not mark any requirement `implemented`.
- Did not fill in approvals, signatures, transcripts or results.
- Did not answer OQ-3 on the course's behalf. OQ-1 was closed by quoting the course PDF, not by guessing what the instructor meant.
- Did not adopt Member B's `SEL-TA-*` candidate or the different codebase it describes.

**OQ-16 — Who owns the portfolio confirmation flow? — OPEN (found 2026-11-24).**

The scope statement used to say `REQ-TA-FR-002` owned "consent". That ID is the **withdrawn GUI entry**, and the labels beside it were misaligned too (`FR-003` is checkpoint/resume, `FR-004` is point-in-time evidence, `FR-006` is freshness). Correcting the citation exposed a real gap rather than a typo: **no active requirement owns the confirmation gate** — the confirm/decline/EOF prompts, the event they emit (`input.consent` exists in `runapi/events.py`), and the rule that declining aborts the run without reading the file. `REQ-TA-INV-014` says confirmation authorizes the frozen selection; it does not define the gate.

This is recorded as open rather than closed by inventing an owner. Adding the entry would be `REQ-TA-FR-009` (numbering must not skip), and it needs a decision on whether the gate is a requirement or a UX detail of the CLI. Owner: A to propose, B to confirm the event contract.

**OQ-16b — Architecture rules named `INV-11`, `INV-12`, `INV-14`.** Three architecture invariants are cited by the registry but are not `REQ-TA-*` entries. `INV-14` (persistence failure) is referenced from `NFR-REPRO-001` and `INV-014`; `INV-11` (resume) from `INV-014`. Earlier text pointed at `REQ-TA-INV-012` / `REQ-TA-INV-011`, IDs that do not exist, because `INV-009`…`013` were deliberately held back pending D's answer to Q-8d. The citations now name the architecture ID and say it is unregistered. **Whenever Q-8d closes and those entries are added, these citations must be rewritten to the `REQ-TA-*` form.**
