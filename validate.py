#!/usr/bin/env python3
"""Validate docs/req/requirements.yaml against docs/req/req-schema.json plus the
cross-record rules JSON Schema cannot express. Owner: Member A; CI hookup is E's.

Exit code 0 = valid, 1 = invalid. Designed to fail loudly on negative fixtures,
so a green run means the checks are actually doing work.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: python3 -m pip install pyyaml jsonschema")
from jsonschema import Draft202012Validator

# Defaults are resolved relative to this file, so the command works from any
# working directory and from any clone — which is what made the documented
# `python3 docs/req/validate.py` fail when run from the repository root.
HERE = Path(__file__).resolve().parent
YAML_PATH = HERE / "requirements.yaml"
SCHEMA_PATH = HERE / "req-schema.json"

# The withdrawn set is recorded by identity, not by count. Rule 13 previously
# only checked `len(withdrawn) >= 3`, so replacing FR-002 with a made-up ID kept
# the count and passed. Found by an independent review on 2026-11-24.
REQUIRED_WITHDRAWN = {
    "REQ-TA-FR-002": "GUI out of scope",
    "REQ-TA-NFR-SAFETY-001": "Research-only scope: no position sizing is validated",
    "REQ-TA-NFR-SAFETY-002": "Replaced by REQ-TA-FR-007 part 3",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys.

    `yaml.safe_load` silently keeps the last of two identical top-level keys, so
    a registry could carry a stale `schema_version: 0.0.0` line above the real
    one and validate cleanly. Found by an independent review on 2026-11-24.
    """


def _no_duplicate_keys(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"found duplicate key {key!r}", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicate_keys)


def _prose_strings(node, path=""):
    """Yield (location, text) for every string leaf, keyed by its YAML path.

    Used to resolve identifiers quoted in prose. Keeping the path in the
    message is what makes a dangling citation actionable: a bare ID in a
    twenty-line note tells a reviewer nothing about where to fix it.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _prose_strings(value, f"{path}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            label = (value.get("id") or value.get("name")) if isinstance(value, dict) else None
            yield from _prose_strings(value, f"{path}/{label or index}")
    elif isinstance(node, str):
        yield path.lstrip("/") or "(root)", node


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the requirements registry against its schema and cross-record rules.")
    parser.add_argument("registry", nargs="?", default=None,
                        help=f"registry file (default: {YAML_PATH})")
    parser.add_argument("--registry", dest="registry_opt", default=None,
                        help="registry file; accepted because the negative-fixture "
                             "document uses this flag form")
    parser.add_argument("--schema", dest="schema", default=None,
                        help=f"schema file (default: {SCHEMA_PATH})")
    args = parser.parse_args(argv)

    yaml_path = Path(args.registry_opt or args.registry or YAML_PATH)
    schema_path = Path(args.schema) if args.schema else SCHEMA_PATH

    if not yaml_path.is_file():
        print(f"ERROR registry file not found: {yaml_path}")
        return 1
    if not schema_path.is_file():
        print(f"ERROR schema file not found: {schema_path}")
        return 1

    try:
        with open(yaml_path, encoding="utf-8") as handle:
            doc = yaml.load(handle, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        print(f"ERROR registry does not parse as YAML: {exc}")
        return 1
    except OSError as exc:
        print(f"ERROR registry unreadable: {exc}")
        return 1

    with open(schema_path, encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    problems = []

    if not isinstance(doc, dict):
        print("ERROR registry is not a mapping at the top level")
        return 1

    # 1. Structural validation
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "(root)"
        problems.append(f"schema: {where}: {err.message}")

    # A missing top-level key is a schema error, already reported above. The
    # cross-record rules cannot run without them, so report and stop rather than
    # raising a traceback: a reviewer should read a finding, not a stack dump.
    # The traceback on a deleted `requirements` key was reported on 2026-11-24.
    reqs = doc.get("requirements")
    if not isinstance(reqs, list) or not reqs:
        problems.append("schema: /requirements: missing or empty; cross-record rules skipped")
        for line in problems:
            print(("ERROR " if not line.startswith("warning:") else "") + line)
        print("\n0 requirements; 0 withdrawn; "
              f"{len(problems)} error(s), 0 warning(s)")
        return 1
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

    # 4. Every dependency and inviting cross-reference resolves
    for r in reqs:
        for dep in r["dependencies"]:
            if dep not in seen:
                problems.append(f"{r['id']}: dangling dependency {dep}")
        enforced = r.get("enforced_by")
        if enforced and enforced not in seen:
            problems.append(f"{r['id']}: enforced_by names unknown requirement {enforced}")
        for other in r.get("amended_by") or []:
            # `amended_by` may name a requirement OR a recorded decision (D-1…D-5).
            if other in seen or re.fullmatch(r"D-\d+", str(other)):
                continue
            problems.append(f"{r['id']}: amended_by names unknown requirement or decision {other}")

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

    # 6. Parameters and their users resolve in both directions.
    #    The old rule only checked that a named parameter's `used_by` targets exist.
    #    It did not check that a parameter the registry *relies on* is declared, so
    #    deleting CALL_CAP from the appendix exited 0. Found by an independent
    #    review on 2026-11-24.
    declared_params = set()
    for p in doc.get("parameter_appendix", []):
        if p["name"] in declared_params:
            problems.append(f"parameter declared twice: {p['name']}")
        declared_params.add(p["name"])
        for used in p["used_by"]:
            if used not in seen:
                problems.append(f"parameter {p['name']}: used_by unknown requirement {used}")

    # Every UPPER_CASE token the requirement text leans on as a parameter must be
    # declared, unless it is a recorded environment/technical constant below.
    # Controlled vocabularies and configuration keys are not tuning parameters.
    # They are enumerated here BY NAME so that a new one cannot slip in unnoticed:
    # adding either a vocabulary value or a tuning parameter requires editing this
    # list, which is the point.
    VOCABULARY = {
        # RUN-001 stop reasons
        "MODEL_FAILURE", "DATA_FAILURE", "INTERNAL_ERROR", "PERSISTENCE_ERROR",
        "INTERRUPTED", "BUDGET",
        # output-check outcomes and statuses
        "NEEDS_REVIEW", "NOT_RUN", "CHECK_ERROR", "NO_DATA", "NOT_REQUESTED",
        # checkpoint states
        "CONFIG_CHANGED", "RESUMABLE",
        # usage availability
        "UNKNOWN",
        # configuration / mapping keys, not tunables
        "DEFAULT_CONFIG",
    }
    PARAM_EXEMPT = {
        "REQ", "TA", "FR", "NFR", "INV", "SEC", "ARCH", "GOV", "PERF", "COST",
        "EVAL", "REPRO", "OBS", "RUN", "GUI", "JSON", "YAML", "PRD", "D1", "D2",
        "D3", "D4", "D5", "CI", "CLI", "API", "SECONDS", "TOKENS", "CALLS",
        # Code constants quoted to describe the baseline, not tunables this
        # registry owns. MAX_OHLCV_STALE_DAYS is tradingagents/dataflows/
        # vendors/yahoo/ohlcv.py:18; it is cited in FR-006's baseline to show the
        # price rule already exists upstream. The registry's own knob is
        # STALE_PRICE_DAYS in parameter_appendix, which is checked separately.
        "MAX_OHLCV_STALE_DAYS",
    } | VOCABULARY
    # Tuning parameters are the names that appear in `parameter_appendix`; a
    # reference is only suspicious if it is UPPER_CASE, underscored, and not a
    # declared parameter, an exempt token, or an identifier from another namespace.
    # Both branches allow a multi-segment prefix. The earlier pattern matched
    # only one segment before the suffix, so STALE_PRICE_DAYS and
    # STALE_STATEMENT_DAYS were never seen at all; `_EVAL` was missing, so
    # N_EVAL was invisible too. Review 2026-11-24.
    param_re = re.compile(
        r"\b("
        r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*_CAP"
        r"|[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*_(?:BUDGET|DAYS|LIMIT|ALLOWANCE|THRESHOLD|SIZE|RATE|COUNT|ROUNDS|TIMEOUT|EVAL)"
        r")\b")
    # Fields scanned for parameter references. Previously only statement,
    # fit_criterion and threshold were read, so a parameter cited only in
    # `metric` or `verification` was invisible and deleting its appendix row
    # still validated. Reported on 2026-11-24.
    SCANNED = ("statement", "fit_criterion", "threshold", "metric", "verification",
               "tradeoff", "note", "open", "baseline")
    for r in reqs:
        blob_r = json.dumps({k: r.get(k) for k in SCANNED},
                            ensure_ascii=False)
        for token in set(param_re.findall(blob_r)):
            if token in PARAM_EXEMPT or token in declared_params:
                continue
            if token.startswith(("REQ_", "NFR_", "INV_", "SEL_")):
                continue
            problems.append(
                f"{r['id']}: references parameter {token} "
                "that is not declared in parameter_appendix")

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
            blob = json.dumps(r).lower()
            if "zero-tolerance" not in blob and "blocking" not in blob:
                problems.append(
                    f"{r['id']}: invariant fit criterion "
                    "does not state a zero-tolerance outcome")

    # 12. Required prose is non-empty (the failure mode of a bad bulk rewrite)
    for r in reqs:
        for f in ("statement", "fit_criterion", "tradeoff"):
            if not r.get(f, "").strip():
                problems.append(f"{r['id']}: {f} is empty")

    # 13. Withdrawn IDs are exactly the recorded set and appear nowhere as active.
    #     Counting alone was not enough: swapping FR-002 for a made-up ID kept the
    #     count at 3 and passed. Found by an independent review on 2026-11-24.
    missing_w = sorted(set(REQUIRED_WITHDRAWN) - withdrawn)
    extra_w = sorted(withdrawn - set(REQUIRED_WITHDRAWN))
    if missing_w:
        problems.append(
            f"scope.withdrawn_ids lost recorded withdrawn ID(s): {', '.join(missing_w)}")
    if extra_w:
        problems.append(f"scope.withdrawn_ids holds unrecorded ID(s): {', '.join(extra_w)}")

    # 14. The eight invariants are present
    for n in range(1, 9):
        ident = f"REQ-TA-INV-{n:03d}"
        if ident not in seen:
            problems.append(f"missing invariant {ident}")

    # 17. Every `REQ-TA-*` identifier quoted anywhere in the prose resolves.
    #     Rule 4 only walked the structured fields (`dependencies`, `enforced_by`,
    #     `amended_by`), so an ID named only in a statement or a note went unchecked.
    #     That is how `REQ-TA-INV-012` was cited four times in this registry while
    #     no such entry existed. Found by an external review on 2026-11-24.
    id_re = re.compile(r"\bREQ-TA-[A-Z]+-\d{3}\b")
    for where, text in _prose_strings(doc):
        for cited in id_re.findall(text):
            if cited not in seen and cited not in withdrawn:
                problems.append(f"{where}: cites undefined requirement {cited}")

    # 18. Every declared parameter is used by exactly the requirements its
    #     `used_by` names. Deleting a row from `parameter_appendix` used to pass
    #     because the text citation was never read back. Review 2026-11-24.
    for p in doc.get("parameter_appendix", []):
        token_re = re.compile(rf"\b{re.escape(p['name'])}\b")
        uses = [
            r["id"] for r in reqs
            if any(token_re.search(str(r.get(k) or "")) for k in SCANNED)
        ]
        if not uses:
            problems.append(
                f"parameter {p['name']} is declared but no requirement uses it")
        elif sorted(uses) != sorted(p["used_by"]):
            problems.append(
                f"parameter {p['name']}: used_by {sorted(p['used_by'])} but the text "
                f"actually cites it in {sorted(uses)}")

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
        problems.append(
            "profile A-C (portfolio with an unrelated holding) is missing; "
            "the holdings clause cannot be exercised")

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
