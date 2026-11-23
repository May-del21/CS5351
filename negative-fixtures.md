# Negative fixtures for `validate.py`

**Owner:** Member A. **Date:** 23 November 2026.
**Purpose:** Prove that each validation rule actually rejects the thing it claims to reject. E asked for the validator and its dependency/command information; a validator is only evidence of a rule if a negative fixture fails on it.

**Rules now number 20** (16 cross-record + 4 on `fixture_profiles`). Command

```bash
python3 docs/req/validate.py        # expects: 34 requirements; 3 withdrawn; 0 error(s), 0 warning(s)
```

**Dependencies:** `pyyaml`, `jsonschema`. No others. Python 3.10+.

---

## How to reproduce

Each case is applied to a **temporary copy** of the registry and must produce the stated error. The real registry is never modified.

```bash
cp docs/req/requirements.yaml /tmp/neg.yaml
python3 - <<'PY'
import yaml, subprocess, shutil
d = yaml.safe_load(open('/tmp/neg.yaml'))
# ... apply ONE mutation from the table below to d ...
yaml.safe_dump(d, open('/tmp/neg.yaml','w'), sort_keys=False, allow_unicode=True)
PY
python3 docs/req/validate.py --registry /tmp/neg.yaml   # must FAIL
```

If `validate.py` does not accept `--registry`, call `validate(registry_path)` from the same file; A will add the flag if E prefers the CLI form.

---

## The seventeen rules and one failing fixture each

| # | Rule | Mutation applied | Expected message fragment |
|---|---|---|---|
| 1 | Schema | Set a requirement's `priority` to `"Essential"` | schema / `Essential` is not one of |
| 2 | Unique IDs | Duplicate `REQ-TA-FR-001` | `duplicate` |
| 3 | Withdrawn preserved | Re-add `REQ-TA-FR-002` as an active requirement | withdrawn ID reused |
| 4 | Dependencies resolve | Point a requirement at `REQ-TA-FR-999` | does not resolve |
| 5 | Must→Could ordering | Make a Must depend on a Could | Must depends on Could |
| 6 | Parameter references | Delete `CALL_CAP` from `parameter_appendix` | unknown parameter |
| 7 | No placeholders | Set a statement to `TBD` | placeholder |
| 8 | Course type coverage | Change `REQ-TA-GOV-003`'s type to `functional` | type coverage |
| 9 | NFR metric/threshold/verification | Delete `threshold` from a non-functional entry | metric/threshold/verification |
| 10 | Source links | Blank the `source` list of an entry with a `baseline` | no source link |
| 11 | Invariant zero-tolerance | Set `zero_tolerance: false` on `REQ-TA-INV-004` | not marked zero_tolerance |
| 12 | Non-empty prose | Set `statement: ""` on `REQ-TA-FR-005` | statement is empty |
| 13 | Exact withdrawn set | Delete one entry from `scope.withdrawn_ids` | 3 are recorded |
| 14 | Eight invariants present | Delete `REQ-TA-INV-006` | missing invariant REQ-TA-INV-006 |
| 15 | Complete Given/when/then | Change `REQ-TA-INV-007`'s fit criterion to `Given a run, then it passes.` | missing when |
| 16 | Adoption gate | Set `document.status: adopted` with an empty §6 record | cannot verify the five-member adoption record |
| 17 | `fixture_profiles` present | Delete the `fixture_profiles` key | schema / `fixture_profiles` is a required property |
| 18 | Every active requirement has a profile | Remove `REQ-TA-FR-001` from its assignment group | `no fixture profile assigned` |
| 19 | No requirement in two groups | Add `REQ-TA-FR-001` to a second group | `assigned to more than one profile group` |
| 20 | Portfolio-holding profile exists | Drop `A-C` from `offline_variants` | `profile A-C … is missing` |

Rules 18–20 exist because of a real contradiction A had shipped: the offline profile said `Portfolio: None` while the privacy criterion needed a second position to exist. A profile mistake that silently unsets itself is exactly the failure these rules catch. All four were run and confirmed to fail on 2026-11-23.

**Rule 13 exists because of a real incident.** A once rewrote the registry with a bulk `yaml.dump`, which silently dropped all three `withdrawn_ids` and deleted `REQ-TA-INV-005`. Rule 13 and rule 14 were added afterwards, and both negative fixtures were confirmed to fail. The earlier validator would have passed that file.

---

## What these fixtures do NOT prove

- They prove the validator **rejects** each defect class. They do not prove the registry is **correct** — a wrong-but-well-formed requirement passes.
- They do not prove any requirement is **implemented** or tested. All non-withdrawn entries are `proposed` or `partial`.
- They are not C's acceptance evidence. C owns independent verification; this file is A's self-check that the tool works.

## What a reader should be able to conclude

Someone who runs the command above gets `0 error(s)` on the real registry. Someone who applies any row of the table gets a failure naming that rule. If either is not true, this file is wrong and A needs to know.
