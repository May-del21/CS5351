# Negative fixtures for `validate.py`

**Owner:** Member A. **First written:** 23 November 2026. **Rewritten:** 24 November 2026 after an independent integration review.

**Purpose:** Prove that each validation rule actually rejects the thing it claims to reject. A validator is only evidence of a rule if a negative fixture fails on it — **and fails for the stated reason**, not because a file was missing or a dependency was absent.

**Rules now number 27** (21 cross-record + 4 on `fixture_profiles` + 2 added 24 November 2026 after an external review: prose citation resolution and bidirectional parameter use).

---

## Run it

```bash
python3 docs/req/validate.py                    # expects: 36 requirements; 3 withdrawn; 0 error(s), 0 warning(s)
python3 docs/req/negative-fixtures-check.py     # executes all 27 cases below
```

Both commands resolve their default paths **relative to the file itself**, so they work from any working directory and from any clone. **Dependencies:** `pyyaml`, `jsonschema`. No others. Python 3.10+.

---

## What the 24 November review found, and what changed

An independent integration review (`project-integration-review-2026-11-24.md`, finding I24 04) ran five mutations against the previous validator. **Three exited 0 when the document said they must fail**, and one more failed only because the *fixture itself* was wrong. Every item below is a confirmed defect, reproduced before it was fixed.

| The review's mutation | Old behaviour | Now |
|---|---|---|
| Remove `CALL_CAP` from `parameter_appendix` | **exited 0** — rule 6 only checked named parameters' `used_by`, never that a parameter the text *relies on* is declared | Rule 6 checks both directions: a parameter the registry references must be declared |
| Replace withdrawn `REQ-TA-FR-002` with `REQ-TA-FR-999`, keeping 3 entries | **exited 0** — rule 13 only checked `len(...) >= 3` | Rule 13 checks the **identity** of the withdrawn set, not its count |
| Point an invariant's `enforced_by` at a nonexistent ID | **exited 0** — the schema checked identifier syntax, nothing resolved the reference | Rule 4 now resolves `enforced_by` and `amended_by` (allowing `D-1`…`D-5` decision IDs) |
| Add an earlier duplicate top-level `schema_version: 0.0.0` | **exited 0** — `yaml.safe_load` silently keeps the last duplicate key | A `UniqueKeyLoader` rejects any duplicate mapping key at any depth |
| Change only `REQ-TA-GOV-003` to `functional` | failed, but for the wrong reason — rule 8 needs *all* governance coverage gone, and two other governance entries remained | The fixture now removes the **last** entry of a type (performance), which is what rule 8 actually asserts |
| `python3 docs/req/validate.py` from the repository root | **`FileNotFoundError`** — the script hard-coded a relative path | Paths resolve from `__file__` |
| `validate.py --registry <path>` | **`FileNotFoundError: '--registry'`** — the first positional was taken as the filename | `--registry`, `--schema` and a bare positional are all accepted |
| Missing schema file / unparsable YAML | raw traceback | a named one-line failure and exit 1 |

The review also flagged that an earlier version of this document told the reader to "call `validate(registry_path)` from the same file; A will add the flag if E prefers the CLI form". **There was no such function.** That sentence is deleted; the flag exists.

---

## The 27 rules and one failing fixture each

All cases below are executed by `negative-fixtures-check.py`, which asserts three things per case: non-zero exit, **the expected message present**, and **no traceback / missing-file / missing-module text**. A case that fails for an unrelated reason is reported as a failure of the fixture.

| # | Rule | Mutation applied | Expected message fragment |
|---|---|---|---|
| 1 | Schema | Set a requirement's `priority` to `"Essential"` | `is not one of` |
| 2 | Unique IDs | Duplicate `REQ-TA-FR-001` | `duplicate id` |
| 3 | Withdrawn never reused | Re-add `REQ-TA-FR-002` as an active requirement | `withdrawn id reused` |
| 4a | Dependencies resolve | Point a requirement at `REQ-TA-FR-999` | `dangling dependency` |
| 4b | `enforced_by` resolves | Point `REQ-TA-INV-001`'s `enforced_by` at `REQ-TA-FR-999` | `enforced_by names unknown` |
| 5 | Must→Could ordering | Make a Must depend on a Could | `depends on` |
| 6 | Parameter references resolve **both ways** | Delete `CALL_CAP` from `parameter_appendix` | `references parameter CALL_CAP` |
| 7 | No placeholders | Set a statement to `TBD` | `placeholder` |
| 8 | Course type coverage | Change the **only** `performance` entry's type to `functional` | `type coverage` |
| 9 | NFR metric/threshold/verification | Delete `threshold` from a cost entry | `missing threshold` |
| 10 | Source links | Blank the `source` list of an entry with a `baseline` | `no source link` |
| 11 | Invariant zero-tolerance | Set `zero_tolerance: false` on `REQ-TA-INV-004` | `not marked zero_tolerance` |
| 12 | Non-empty prose | Set `statement: ""` on `REQ-TA-FR-005` | `statement is empty` |
| 13a | Exact withdrawn identity set | Delete one entry from `scope.withdrawn_ids` | `lost recorded withdrawn ID` |
| 13b | Exact withdrawn identity set | Replace `REQ-TA-FR-002` with `REQ-TA-FR-999`, keeping 3 entries | `lost recorded withdrawn ID` |
| 13c | No duplicate YAML keys | Add a second top-level `schema_version: 0.0.0` above the real one | `duplicate key` |
| 14 | Required invariants present | Delete `REQ-TA-INV-006` | `missing invariant REQ-TA-INV-006` |
| 15 | Complete Given/when/then | Change `REQ-TA-INV-007`'s fit to `Given a run, then it passes.` | `missing when` |
| 16 | Adoption gate | Set `document.status: adopted` with an empty §6 record | `cannot verify the five-member adoption record` |
| 17 | `fixture_profiles` present | Delete the `fixture_profiles` key | `fixture_profiles` |
| 18 | Every active requirement has a profile | Remove `REQ-TA-FR-001` from its assignment group | `no fixture profile assigned` |
| 19 | No requirement in two groups | Add `REQ-TA-FR-001` to a second group | `assigned to more than one profile group` |
| 20 | Portfolio-holding profile exists | Drop `A-C` from `offline_variants` | `profile A-C` |
| 21 | Schema file absent | Point `--schema` at a nonexistent file | `schema file not found` |
| 22 | Every `REQ-TA-*` ID quoted in prose resolves (rule 17) | Name `REQ-TA-INV-012` in `REQ-TA-FR-001`'s `note` only, with no such entry | `cites undefined requirement` |
| 23 | Parameter references resolve both ways (rule 6, multi-segment names) | Delete `STALE_PRICE_DAYS` | `references parameter` |
| 24 | Parameter references resolve both ways (rule 6, `_EVAL` names) | Delete `N_EVAL` | `references parameter N_EVAL` |
| 25 | A missing top-level key is a finding, not a traceback | Delete the `requirements` key | `missing or empty` |

Rules 18–20 exist because of a real contradiction A had shipped: the offline profile said `Portfolio: None` while the privacy criterion needed a second position to exist. All were confirmed to fail on 2026-11-23.

**Rule 13 exists because of a real incident.** A once rewrote the registry with a bulk `yaml.dump`, which silently dropped all three `withdrawn_ids` and deleted `REQ-TA-INV-005`. The first repair of rule 13 checked only the count, which is why 13b passed for a day.

**Cases 22–25 exist because an external reviewer, not A, found them.** Four mutations passed a suite that claimed to check the same properties: an ID cited only in prose was never resolved (rule 4 read the structured fields only), and the parameter scan could not see `STALE_PRICE_DAYS`, `STALE_STATEMENT_DAYS` or `N_EVAL` at all — its pattern allowed one prefix segment and had no `_EVAL` suffix, and it read only three of the fields a name can appear in. Deleting `requirements` raised a traceback instead of a finding. Rule 18 (the reverse of rule 6) immediately caught two real errors in the registry: `QUALITY_THRESHOLD` and `N_EVAL` both had incomplete `used_by` lists. **A claim that a rule is enforced is only as good as the case that tries to break it.**

**Rule 13c exists because of a second incident of the same family.** Duplicate mapping keys are silent in both `yaml.safe_load` and a Python dict literal; A had already lost five fixture assignments to a duplicated `A-B` key on 2026-11-23. Rejecting duplicates is now the loader's job, not a human's.

---

## What these fixtures do NOT prove

- They prove the validator **rejects** each defect class. They do not prove the registry is **correct** — a wrong-but-well-formed requirement passes. **Finding I24 02 and I24 07 are examples: both were well-formed and wrong.** I24 07 was a contradiction between two entries that no single-record rule can see; it was found by a human reading both, and is now stated in `REQ-TA-NFR-REPRO-001` directly.
- They do not prove any requirement is **implemented** or tested. All non-withdrawn entries are `proposed` or `partial`.
- They are not C's acceptance evidence. C owns independent verification; this file is A's self-check that the tool works.
- **A green schema result is not a green registry, and a green validator run is not an adoption.** `document.status` is `proposed_for_adoption` and all five adoption boxes are empty.

## What a reader should be able to conclude

Someone who runs either command above gets the stated result on the real registry. Someone who applies any row of the table gets a failure naming that rule **and for that reason**. If either is not true, this file is wrong and A needs to know.
