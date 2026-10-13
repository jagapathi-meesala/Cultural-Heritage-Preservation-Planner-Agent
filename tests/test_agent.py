import json
from pathlib import Path
from core.planner import validate_heritage_records, assess_preservation_priorities, build_preservation_plan

def sample():
    return json.loads(Path("examples/heritage_assets.json").read_text())

def test_sample_valid():
    assert validate_heritage_records(sample()["assets"])["valid"]

def test_scores_are_sorted_with_urgent_first():
    result = assess_preservation_priorities(sample()["assets"], sample()["weights"])
    assert result["valid"]
    assert result["priorities"][0]["priority_label"] == "urgent_review"

def test_duplicate_asset_id_rejected():
    assets = sample()["assets"]
    assets[1]["asset_id"] = assets[0]["asset_id"]
    assert not validate_heritage_records(assets)["valid"]

def test_out_of_range_score_rejected():
    assets = sample()["assets"]
    assets[0]["condition_score"] = 101
    assert not validate_heritage_records(assets)["valid"]

def test_zero_weights_rejected():
    weights = {k: 0 for k in ("condition_score","significance_score","exposure_score","urgency_score")}
    assert not assess_preservation_priorities(sample()["assets"], weights)["valid"]

def test_custom_weights_normalized():
    result = assess_preservation_priorities(sample()["assets"], {"condition_score": 1, "significance_score": 1, "exposure_score": 0, "urgency_score": 0})
    assert result["valid"]
    assert abs(sum(result["weights"].values()) - 1) < 1e-9

def test_missing_documentation_warned():
    result = validate_heritage_records(sample()["assets"])
    assert any("provenance_status missing" in w for w in result["warnings"])

def test_report_includes_safeguards():
    report = build_preservation_plan(sample())
    assert report["valid"]
    assert report["limitations"] and report["recommended_next_steps"]
