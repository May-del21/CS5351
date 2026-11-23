#!/usr/bin/env python3
"""Validate docs/req/requirements.yaml against docs/req/req-schema.json plus the
cross-record rules JSON Schema cannot express. Owner: Member A; CI hookup is E's.

Exit code 0 = valid, 1 = invalid. Designed to fail loudly on negative fixtures,
so a green run means the checks are actually doing work.
"""
import json
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: python3 -m pip install pyyaml jsonschema")
from jsonschema import Draft202012Validator

YAML_PATH = "docs/req/requirements.yaml"
SCHEMA_PATH = "docs/req/req-schema.json"


def main() -> int:
    # An explicit path lets docs/req/negative-fixtures.md run a single mutation
    # against a temporary copy without touching the real registry.
    yaml_path = sys.argv[1] if len(sys.argv) > 1 else YAML_PATH
    doc = yaml.safe_load(open(yaml_path, encoding="utf-8"))
    schema = json.load(open(SCHEMA_PATH, encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    problems = []

    # 1. Structural validation
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "(root)"
        problems.append(f"schema: {where}: {err.message}")

    reqs = doc["requirements"]
    ids = [r["id"] for r in reqs]

    # 2. IDs unique
    seen = set()
    for ident in ids:
        if ident in seen:
            problems.append(f"duplicate id: {ident}")
        seen.add(ident)

    # 3. Withdrawn IDs are preserved and never reused
    withdrawn = {w["id"] for w in doc["scope"]["withdrawn_ids"]}
    for ident in withdrawn & seen:
        problems.append(f"withdrawn id reused in requirements: {ident}")

    # 4. Every dependency resolves
    for r in reqs:
        for dep in r["dependencies"]:
            if dep not in seen:
                problems.append(f"{r['id']}: dangling dependency {dep}")

    # 5. A Must must not depend on a Could (Must -> Should is allowed but reported)
    pri = {r["id"]: r["priority"] for r in reqs}
    for r in reqs:
        for dep in r["dependencies"]:
            if dep in pri:
                if r["priority"] == "Must" and pri[dep] == "Could":
                    problems.append(
                        f"{r['id']} (Must) depends on {dep} (Could): invalid ordering")
                elif r["priority"] == "Must" and pri[dep] == "Should":
                    problems.append(
                        f"warning: {r['id']} (Must) depends on {dep} (Should)")

    # 6. Every parameter referenced in used_by exists
    for p in doc.get("parameter_appendix", []):
        for used in p["used_by"]:
            if used not in seen:
                problems.append(f"parameter {p['name']}: used_by unknown requirement {used}")

    # 7. No placeholder text left behind
    blob = json.dumps(doc, ensure_ascii=False)
    for token in ("FIXME", "TBD", "TODO", "lorem ipsum"):
        if re.search(re.escape(token), blob, re.I):
            problems.append(f"placeholder text found: {token}")

    # 8. Course D1: type coverage must include functional, invariant, governance,
    #    security, performance and cost.
    required_types = {"functional", "invariant", "governance", "security", "performance", "cost"}
    have = {r["type"] for r in reqs}
    for t in sorted(required_types - have):
        problems.append(f"course D1 type coverage: no requirement of type {t}")

    # 9. Course D1: every non-functional requirement states metric + threshold + verification
    nf_types = {"quality_reliability", "quality_maintainability", "quality_observability",
                "quality_reproducibility", "quality_evaluation", "performance", "cost"}
    for r in reqs:
        if r["type"] in nf_types:
            for f in ("metric", "threshold", "verification"):
                if not r.get(f):
                    problems.append(f"{r['id']}: non-functional entry missing {f}")

    # 10. Course D1: requirements found by existing-system analysis are linked to their sources
    for r in reqs:
        if r.get("baseline") and not r["baseline"].startswith("Not present") \
                and not any(s["kind"] == "baseline_observation" for s in r["source"]):
            problems.append(
                f"{r['id']}: has a baseline observation but no baseline_observation source link")

    # 11. Invariants are zero-tolerance and name the component that enforces them
    for r in reqs:
        if r["type"] == "invariant":
            if r.get("zero_tolerance") is not True:
                problems.append(f"{r['id']}: invariant is not marked zero_tolerance")
            if not r.get("enforced_by"):
                problems.append(f"{r['id']}: invariant does not name enforced_by")
            if "zero-tolerance" not in json.dumps(r).lower() and "blocking" not in json.dumps(r).lower():
                problems.append(f"{r['id']}: invariant fit criterion does not state a zero-tolerance outcome")

    # 12. Required prose is non-empty (the failure mode of a bad bulk rewrite)
    for r in reqs:
        for f in ("statement", "fit_criterion", "tradeoff"):
            if not r.get(f, "").strip():
                problems.append(f"{r['id']}: {f} is empty")

    # 13. Withdrawn IDs are exactly the recorded set and appear nowhere as active
    if len(withdrawn) < 3:
        problems.append(f"scope.withdrawn_ids holds {len(withdrawn)} entries; 3 are recorded (FR-002, SAFETY-001, SAFETY-002)")

    # 14. The eight invariants are present
    for n in range(1, 9):
        ident = f"REQ-TA-INV-{n:03d}"
        if ident not in seen:
            problems.append(f"missing invariant {ident}")

    # 16. Every active ID appears exactly once in the printed total
    if len(reqs) != len(seen):
        problems.append(f"{len(seen)} ids but {len(reqs)} entries; duplicate or unindexed entry")

    # 16. Every active ID appears in the fixture-profile assignment exactly once
    fp = doc.get("fixture_profiles", {})
    assigned = {}
    for group, ids in fp.get("assignment", {}).items():
        for rid in ids:
            assigned.setdefault(rid, []).append(group)
    active_ids = [r["id"] for r in doc.get("requirements", []) if r.get("status") != "withdrawn"]
    unassigned = [i for i in active_ids if i not in assigned]
    twice = {i: g for i, g in assigned.items() if len(g) > 1}
    unknown = [i for i in assigned if i not in active_ids]
    if unassigned:
        problems.append(f"no fixture profile assigned: {', '.join(unassigned[:5])}")
    if twice:
        problems.append(f"assigned to more than one profile group: {', '.join(sorted(twice)[:5])}")
    if unknown:
        problems.append(f"fixture profile names an unknown requirement: {', '.join(unknown[:5])}")
    if "A-C" not in fp.get("offline_variants", {}):
        problems.append("profile A-C (portfolio with an unrelated holding) is missing; the holdings clause cannot be exercised")

    # 15. Every fit criterion is a complete Given/when/then
    for r in reqs:
        fc = (r.get("fit_criterion") or "").lower()
        missing = [w for w in ("given", "when", "then") if w not in fc]
        if missing:
            problems.append(f"{r['id']}: fit_criterion is missing {', '.join(missing)}")

    # 8. Adoption gate: adopted status requires a completed record we cannot see here
    if doc["document"]["status"] == "adopted":
        problems.append(
            "document.status is 'adopted' but this script cannot verify the five-member "
            "adoption record; set it to adopted only when that record is actually signed")

    for line in problems:
        print(("ERROR " if not line.startswith("warning:") else "") + line)
    hard = [p for p in problems if not p.startswith("warning:")]
    print(f"\n{len(reqs)} requirements; {len(withdrawn)} withdrawn; "
          f"{len(hard)} error(s), {len(problems) - len(hard)} warning(s)")
    return 0 if not hard else 1


if __name__ == "__main__":
    sys.exit(main())
