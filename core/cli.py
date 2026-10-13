import argparse, json, sys
from pathlib import Path
from .planner import build_preservation_plan

def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a preliminary cultural heritage preservation plan.")
    parser.add_argument("input", help="JSON heritage asset file")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        report = build_preservation_plan(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report.get("valid") else 1

if __name__ == "__main__":
    raise SystemExit(main())
