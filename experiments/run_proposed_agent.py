from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agents.orchestrator import TradeCareOrchestrator


CASES = ROOT / "data" / "eval_cases" / "trade_support_30_cases.jsonl"
OUT = ROOT / "experiments" / "results" / "proposed_agent.jsonl"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    agent = TradeCareOrchestrator(ROOT / "data" / "knowledge_base")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with CASES.open(encoding="utf-8") as source, OUT.open("w", encoding="utf-8") as target:
        for line in source:
            case = json.loads(line)
            started = perf_counter()
            result = agent.run(case["query"])
            result["gold_intent"] = case["intent"]
            result["pred_intent"] = result["intent"]
            result["id"] = case["id"]
            result["latency_seconds"] = round(perf_counter() - started, 4)
            target.write(json.dumps(result, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
