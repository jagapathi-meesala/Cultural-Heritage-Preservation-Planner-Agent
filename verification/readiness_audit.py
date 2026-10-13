from pathlib import Path
import yaml, json, re
ROOT = Path(__file__).resolve().parents[1]
required = ["agent.yaml","SOUL.md","README.md","RULES.md","DUTIES.md","AGENTS.md","EXPLAINABILITY.md","requirements.txt",".env.example",".gitignore","pytest.ini",
"core/__init__.py","core/planner.py","core/cli.py",
"tools/validate-heritage-records.yaml","tools/assess-preservation-priorities.yaml","tools/build-preservation-plan.yaml",
"skills/heritage-record-validation/SKILL.md","skills/preservation-priority-assessment/SKILL.md","skills/conservation-plan-reporting/SKILL.md",
"tests/test_agent.py","examples/heritage_assets.json"]
missing = [x for x in required if not (ROOT/x).is_file()]
if missing:
    print("FAIL: missing files:", missing); raise SystemExit(1)
manifest = yaml.safe_load((ROOT/"agent.yaml").read_text())
assert manifest["spec_version"] == "0.1.0"
assert re.fullmatch(r"[a-z][a-z0-9-]*", manifest["name"])
assert len(manifest["tools"]) == 3 and len(manifest["skills"]) == 3
assert all(re.fullmatch(r"[a-z][a-z0-9-]*", x) for x in manifest["tools"])
for p in (ROOT/"tools").glob("*.yaml"):
    data = yaml.safe_load(p.read_text())
    assert set(data) == {"name","description","input_schema"}, p
    assert re.fullmatch(r"[a-z][a-z0-9-]*", data["name"])
    assert data["input_schema"]["type"] == "object"
for p in (ROOT/"skills").glob("*/SKILL.md"):
    assert p.read_text().startswith("---\nname: ")
doc = (ROOT/"EXPLAINABILITY.md").read_text()
for heading in ["## Inputs","## Decision","## Limits","## Tool: validate-heritage-records","## Tool: assess-preservation-priorities","## Tool: build-preservation-plan"]:
    assert heading in doc, heading
json.loads((ROOT/"examples/heritage_assets.json").read_text())
print(f"PASS: all {len(required)}/{len(required)} required files present")
print("PASS: manifest name/tool IDs, tool schemas, skill frontmatter, explainability headings, and example JSON")
