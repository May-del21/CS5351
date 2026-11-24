#!/usr/bin/env python3
"""Executable negative-fixture harness for docs/req/validate.py.

Owner: Member A. Written 2026-11-24 because an independent integration review
found that `negative-fixtures.md` *described* mutations that the validator did
not actually reject, and because the document's own warning applies to itself:
"a missing dependency, wrong filename or unrelated exception must not count as a
successful negative test".

Every case below asserts THREE things, not one:
  1. the validator exits non-zero,
  2. it exits non-zero **for the stated reason** (the expected message appears),
  3. it does **not** fail because the file was missing, PyYAML/`jsonschema` were
     missing, or some unrelated exception was raised.

Run:  python3 docs/req/negative-fixtures-check.py
Exit: 0 when every fixture fails correctly; 1 otherwise.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATE = HERE / "validate.py"
REGISTRY = HERE / "requirements.yaml"

# Anything matching these means the fixture did not really exercise a rule.
NOT_A_RULE_FAILURE = (
    "Traceback",
    "ModuleNotFoundError",
    "ImportError",
    "No such file",
    "FileNotFoundError",
    "registry file not found",
    "schema file not found",
)


def run(registry: Path, schema: Path | None = None) -> tuple[int, str]:
    cmd = [sys.executable, str(VALIDATE), str(registry)]
    if schema is not None:
        cmd += ["--schema", str(schema)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def mutate_yaml_text(text: str, case: dict) -> str:
    """Apply a text-level mutation (used where YAML must stay malformed)."""
    kind = case["text_mutation"]
    if kind == "duplicate_top_level_key":
        return text.replace("schema_version: 1.2.0",
                            "schema_version: 0.0.0\nschema_version: 1.2.0", 1)
    if kind == "withdrawn_id_swap":
        return text.replace("  - id: REQ-TA-FR-002\n", "  - id: REQ-TA-FR-999\n", 1)
    raise AssertionError(f"unknown text mutation {kind}")


def mutate_doc(doc: dict, case: dict) -> None:
    """Apply a structural mutation through PyYAML (safe for valid YAML)."""
    kind = case["mutation"]
    reqs = {r["id"]: r for r in doc["requirements"]}

    if kind == "bad_priority":
        reqs[case.get("target", "REQ-TA-FR-001")]["priority"] = "Essential"
    elif kind == "duplicate_id":
        doc["requirements"].append(dict(reqs["REQ-TA-FR-001"]))
    elif kind == "drop_withdrawn":
        doc["scope"]["withdrawn_ids"].pop()
    elif kind == "drop_call_cap":
        doc["parameter_appendix"] = [p for p in doc["parameter_appendix"]
                                     if p["name"] != "CALL_CAP"]
    elif kind == "enforced_by_dangling":
        reqs["REQ-TA-INV-001"]["enforced_by"] = "REQ-TA-FR-999"
    elif kind == "dependency_dangling":
        reqs["REQ-TA-FR-001"]["dependencies"] = ["REQ-TA-FR-999"]
    elif kind == "zero_tolerance_off":
        reqs["REQ-TA-INV-004"]["zero_tolerance"] = False
    elif kind == "empty_statement":
        reqs["REQ-TA-FR-005"]["statement"] = ""
    elif kind == "drop_invariant":
        doc["requirements"] = [r for r in doc["requirements"] if r["id"] != "REQ-TA-INV-006"]
    elif kind == "no_when":
        reqs["REQ-TA-INV-007"]["fit_criterion"] = "Given a run, then it passes."
    elif kind == "adopted":
        doc["document"]["status"] = "adopted"
    elif kind == "drop_fixture_profiles":
        doc.pop("fixture_profiles")
    elif kind == "unassign_one":
        a = doc["fixture_profiles"]["assignment"]
        for ids in a.values():
            if "REQ-TA-FR-001" in ids:
                ids.remove("REQ-TA-FR-001")
                break
    elif kind == "assign_twice":
        a = doc["fixture_profiles"]["assignment"]
        for ids in a.values():
            if "REQ-TA-FR-001" in ids:
                break
        a["A-C"].append("REQ-TA-FR-001")
    elif kind == "drop_ac":
        doc["fixture_profiles"]["offline_variants"].pop("A-C")
    elif kind == "withdrawn_reused":
        clone_id = next(r["id"] for r in doc["requirements"]
                        if r["status"] != "withdrawn" and r["type"] == "functional")
        clone = dict(reqs[clone_id])
        clone["id"] = "REQ-TA-FR-002"
        doc["requirements"].append(clone)
    elif kind == "must_depends_could":
        could = next(r["id"] for r in doc["requirements"]
                     if r["priority"] == "Could" and r["status"] != "withdrawn")
        must = next(r["id"] for r in doc["requirements"]
                    if r["priority"] == "Must" and r["status"] != "withdrawn"
                    and r["id"] != could)
        reqs[must]["dependencies"] = [could]
    elif kind == "placeholder":
        reqs["REQ-TA-FR-005"]["statement"] = "TBD"
    elif kind == "type_coverage":
        for r in doc["requirements"]:
            if r["type"] == "performance":
                r["type"] = "functional"
    elif kind == "missing_threshold":
        for r in doc["requirements"]:
            if r["type"] == "cost":
                r.pop("threshold", None)
                break
    elif kind == "prose_dangling_id":
        # A `REQ-TA-*` ID named only in prose, never in a structured field.
        # Classic case: REQ-TA-INV-012 was cited four times with no such entry.
        reqs["REQ-TA-FR-001"]["note"] = (
            "Non-normative: the persistence rule lives in REQ-TA-INV-012.")
    elif kind == "drop_freshness_param":
        doc["parameter_appendix"] = [
            p for p in doc["parameter_appendix"] if p["name"] != "STALE_PRICE_DAYS"]
    elif kind == "drop_n_eval":
        doc["parameter_appendix"] = [
            p for p in doc["parameter_appendix"] if p["name"] != "N_EVAL"]
    elif kind == "drop_requirements_key":
        doc.pop("requirements", None)
    else:
        raise AssertionError(f"unknown mutation {kind}")


CASES = [
    # (name, kind, expected fragment)
    ("1  schema: bad priority", "bad_priority", "Essential"),
    ("2  duplicate id", "duplicate_id", "duplicate id"),
    ("3  withdrawn id reused", "withdrawn_reused", "withdrawn id reused"),
    ("4a dangling dependency", "dependency_dangling", "dangling dependency"),
    ("4b enforced_by points nowhere", "enforced_by_dangling", "enforced_by names unknown"),
    ("5  Must depends on Could", "must_depends_could", "depends on"),
    ("6  CALL_CAP deleted from appendix", "drop_call_cap", "references parameter CALL_CAP"),
    ("7  placeholder text", "placeholder", "placeholder"),
    ("8  type coverage", "type_coverage", "type coverage"),
    ("9  NFR missing threshold", "missing_threshold", "missing threshold"),
    ("11 zero_tolerance off", "zero_tolerance_off", "not marked zero_tolerance"),
    ("12 empty statement", "empty_statement", "statement is empty"),
    ("13a withdrawn entry deleted", "drop_withdrawn", "lost recorded withdrawn ID"),
    ("13b withdrawn id swapped for a fake one", "__withdrawn_id_swap",
     "lost recorded withdrawn ID"),
    ("13c duplicate top-level schema_version", "__dup_key", "duplicate key"),
    ("14 invariant deleted", "drop_invariant", "missing invariant REQ-TA-INV-006"),
    ("15 fit without 'when'", "no_when", "missing when"),
    ("16 adopted without a record", "adopted", "cannot verify the five-member adoption record"),
    ("17 fixture_profiles deleted", "drop_fixture_profiles", "fixture_profiles"),
    ("18 requirement unassigned", "unassign_one", "no fixture profile assigned"),
    ("19 requirement in two groups", "assign_twice", "assigned to more than one profile group"),
    ("20 A-C profile missing", "drop_ac", "profile A-C"),
    # Added 2026-11-24 after an external review found all three passed.
    ("22 prose-cited ID with no entry", "prose_dangling_id", "cites undefined requirement"),
    ("23 freshness-days parameter deleted", "drop_freshness_param", "references parameter"),
    ("24 N_EVAL deleted from appendix", "drop_n_eval", "references parameter N_EVAL"),
    ("25 requirements key removed", "drop_requirements_key", "missing or empty"),
]


def main() -> int:
    if not REGISTRY.is_file():
        print(f"FATAL registry missing: {REGISTRY}")
        return 1

    base_text = REGISTRY.read_text(encoding="utf-8")
    import yaml  # noqa: PLC0415 - intentional: a missing PyYAML is itself a finding below

    base_doc = yaml.safe_load(base_text)

    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)

        # Baseline must be green, or every case below proves nothing.
        code, out = run(REGISTRY)
        if code != 0:
            print("FATAL the real registry does not validate; negative fixtures are meaningless")
            print(out)
            return 1

        for name, mutation, expected in CASES:
            target = tmpdir / "neg.yaml"
            if mutation == "__dup_key":
                target.write_text(
                    mutate_yaml_text(base_text, {"text_mutation": "duplicate_top_level_key"}),
                    encoding="utf-8")
            elif mutation == "__withdrawn_id_swap":
                target.write_text(
                    mutate_yaml_text(base_text, {"text_mutation": "withdrawn_id_swap"}),
                    encoding="utf-8")
            elif mutation == "duplicate_id":
                doc = json.loads(json.dumps(base_doc))
                mutate_doc(doc, {"mutation": mutation})
                with open(target, "w", encoding="utf-8") as fh:
                    yaml.safe_dump(doc, fh, sort_keys=False, allow_unicode=True)
            else:
                doc = json.loads(json.dumps(base_doc))
                mutate_doc(doc, {"mutation": mutation})
                with open(target, "w", encoding="utf-8") as fh:
                    yaml.safe_dump(doc, fh, sort_keys=False, allow_unicode=True)

            code, out = run(target)

            if code == 0:
                failures.append((name, "exited 0; the rule did not fire"))
                continue
            for marker in NOT_A_RULE_FAILURE:
                if marker in out:
                    failures.append((name, f"failed for the wrong reason ({marker})"))
                    break
            else:
                if expected not in out:
                    failures.append(
                        (name, f"failed but did not say {expected!r}: {out.strip()[:160]}"))
                else:
                    print(f"ok   {name}")

    # Missing-schema case: must be a clean named failure, not a traceback.
    with tempfile.TemporaryDirectory() as tmp:
        code, out = run(REGISTRY, schema=Path(tmp) / "nope.json")
        if code == 0:
            failures.append(("21 missing schema file", "exited 0"))
        elif "schema file not found" not in out:
            failures.append(("21 missing schema file", f"wrong message: {out.strip()[:160]}"))
        else:
            print("ok   21 missing schema file")

    print()
    if failures:
        print(f"{len(failures)} fixture(s) did not behave as documented:")
        for name, why in failures:
            print(f"  FAIL {name}: {why}")
        return 1
    print(f"all {len(CASES) + 1} negative fixtures fail correctly, each for its stated reason")
    return 0


if __name__ == "__main__":
    sys.exit(main())
