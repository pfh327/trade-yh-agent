from __future__ import annotations

import json
import sys
from pathlib import Path
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agents.intake_agent import IntakeAgent
from app.agents.retrieval_agent import RetrievalAgent


CASES = ROOT / "data" / "eval_cases" / "trade_support_30_cases.jsonl"
OUT = ROOT / "experiments" / "results" / "baseline_rag.jsonl"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    intake_agent = IntakeAgent()
    retrieval_agent = RetrievalAgent(ROOT / "data" / "knowledge_base")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with CASES.open(encoding="utf-8") as source, OUT.open("w", encoding="utf-8") as target:
        for line in source:
            case = json.loads(line)
            started = perf_counter()
            intake = intake_agent.run(case["query"])
            contexts = retrieval_agent.run(case["query"], intake.intent)
            evidence = "; ".join(item["title"] for item in contexts[:2])
            answer = (
                f"문의 유형은 {intake.intent}로 보입니다. 관련 자료({evidence})를 기준으로, "
                f"진행 가능 여부는 추가 정보와 공급처 확인 후 안내 가능합니다. "
                f"필요한 정보: {', '.join(intake.missing_fields[:5])}."
            )
            target.write(json.dumps({
                "id": case["id"],
                "query": case["query"],
                "gold_intent": case["intent"],
                "pred_intent": intake.intent,
                "answer": answer,
                "contexts": contexts,
                "latency_seconds": round(perf_counter() - started, 4),
            }, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
