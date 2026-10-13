# Cultural Heritage Preservation Planner Agent

A deterministic, portable agent that organizes supplied heritage-site and object records into a preliminary preservation planning report. It validates records, calculates transparent priority indicators from user-provided condition, significance, exposure, and urgency scores, and highlights missing documentation.

## Capabilities
- Validate heritage asset identifiers and supplied 0–100 planning scores.
- Rank records for review using configurable weighted indicators.
- Flag high urgency and missing provenance, condition evidence, or community consultation notes.
- Produce a JSON report with rationale, evidence gaps, and suggested next steps.
- Keep assessment separate from conservation treatment decisions.

## Scope and safeguards
This tool does not authenticate artifacts, determine legal ownership, assess cultural significance independently, or prescribe physical treatment. Cultural protocols, community and Indigenous rights, site permissions, and local heritage laws must be respected. Do not expose sensitive site locations or culturally restricted information in public reports. Qualified conservators, heritage authorities, and relevant communities should review any plan before action.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 verification/readiness_audit.py
python3 -m core.cli examples/heritage_assets.json
```

## OpenGAP
Manifest targets OpenGAP v0.1.0. If the official CLI is installed, run `opengap validate`.
