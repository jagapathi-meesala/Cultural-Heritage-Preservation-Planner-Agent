from typing import Any

SCORE_FIELDS = ("condition_score", "significance_score", "exposure_score", "urgency_score")
DEFAULT_WEIGHTS = {"condition_score": 0.30, "significance_score": 0.30, "exposure_score": 0.20, "urgency_score": 0.20}
HIGH_URGENCY_THRESHOLD = 75

def validate_heritage_records(records: Any) -> dict[str, Any]:
    errors, warnings, valid_ids = [], [], []
    if not isinstance(records, list) or not records:
        return {"valid": False, "errors": ["assets must be a non-empty list."], "warnings": [], "valid_asset_ids": []}
    seen = set()
    for i, item in enumerate(records):
        if not isinstance(item, dict):
            errors.append(f"assets[{i}]: expected an object.")
            continue
        aid = item.get("asset_id")
        if not isinstance(aid, str) or not aid.strip():
            errors.append(f"assets[{i}].asset_id: required non-empty string.")
        elif aid in seen:
            errors.append(f"assets[{i}].asset_id: duplicate ID {aid!r}.")
        else:
            seen.add(aid)
        bad = []
        for field in SCORE_FIELDS:
            val = item.get(field)
            if not isinstance(val, (int, float)) or isinstance(val, bool) or not 0 <= val <= 100:
                bad.append(f"assets[{i}].{field}: expected a number from 0 to 100.")
        if bad:
            errors.extend(bad)
        else:
            valid_ids.append(aid)
        for field in ("provenance_status", "condition_evidence", "community_consultation_status", "permissions_status"):
            if not item.get(field):
                warnings.append(f"{aid or 'asset '+str(i)}: {field} missing; verify before planning action.")
    return {"valid": not errors, "errors": errors, "warnings": warnings, "valid_asset_ids": valid_ids}

def _normalize_weights(weights: Any) -> dict[str, float]:
    if weights is None:
        weights = DEFAULT_WEIGHTS
    if not isinstance(weights, dict):
        raise ValueError("weights must be an object.")
    unknown = set(weights) - set(SCORE_FIELDS)
    if unknown:
        raise ValueError("unknown weight keys: " + ", ".join(sorted(unknown)))
    result = {field: float(weights.get(field, DEFAULT_WEIGHTS[field])) for field in SCORE_FIELDS}
    if any(v < 0 for v in result.values()):
        raise ValueError("weights must be non-negative.")
    total = sum(result.values())
    if total <= 0:
        raise ValueError("at least one weight must be greater than zero.")
    return {field: value / total for field, value in result.items()}

def assess_preservation_priorities(records: Any, weights: Any = None) -> dict[str, Any]:
    validation = validate_heritage_records(records)
    if not validation["valid"]:
        return {"valid": False, "errors": validation["errors"], "warnings": validation["warnings"], "priorities": []}
    try:
        normalized = _normalize_weights(weights)
    except (ValueError, TypeError) as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": validation["warnings"], "priorities": []}
    priorities = []
    for item in records:
        contributions = {field: round(float(item[field]) * normalized[field], 4) for field in SCORE_FIELDS}
        score = round(sum(contributions.values()), 2)
        urgency = float(item["urgency_score"])
        label = "urgent_review" if urgency >= HIGH_URGENCY_THRESHOLD else ("high_priority" if score >= 70 else ("medium_priority" if score >= 40 else "routine_review"))
        priorities.append({
            "asset_id": item["asset_id"], "priority_score": score, "priority_label": label,
            "component_scores": {field: item[field] for field in SCORE_FIELDS},
            "weighted_contributions": contributions,
            "missing_evidence": [field for field in ("provenance_status", "condition_evidence", "community_consultation_status", "permissions_status") if not item.get(field)],
            "notes": item.get("notes")
        })
    priorities.sort(key=lambda row: (0 if row["priority_label"] == "urgent_review" else 1, -row["priority_score"], row["asset_id"]))
    return {"valid": True, "errors": [], "warnings": validation["warnings"], "weights": normalized, "priorities": priorities,
            "method": "Weighted average of four supplied 0–100 scores; priority label is a planning aid, not a treatment decision."}

def build_preservation_plan(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"valid": False, "status": "invalid_input", "errors": ["payload must be an object."]}
    validation = validate_heritage_records(payload.get("assets"))
    assessment = assess_preservation_priorities(payload.get("assets"), payload.get("weights"))
    findings = [{"type": "documentation_gap", "detail": w} for w in validation["warnings"]]
    for row in assessment.get("priorities", []):
        if row["priority_label"] == "urgent_review":
            findings.append({"type": "urgent_review", "asset_id": row["asset_id"], "detail": "Arrange qualified condition review and confirm appropriate permissions and consultation."})
    return {
        "agent": "cultural-heritage-preservation-planner-agent",
        "valid": validation["valid"] and assessment["valid"],
        "status": "needs_data_correction" if not validation["valid"] or not assessment["valid"] else "preliminary_preservation_plan",
        "validation": validation, "assessment": assessment, "findings": findings,
        "limitations": [
            "Scores are supplied by the user and are not independent determinations of cultural significance.",
            "No authenticity, ownership, legal status, or physical condition was independently verified.",
            "No physical treatment or irreversible intervention is prescribed."
        ],
        "recommended_next_steps": [
            "Confirm provenance and condition evidence with authorized custodians and qualified conservators.",
            "Consult relevant communities and respect applicable cultural protocols and access restrictions.",
            "Verify permissions, ownership, local heritage rules, and emergency risks before action.",
            "Store sensitive location and cultural information in access-controlled records."
        ]
    }
