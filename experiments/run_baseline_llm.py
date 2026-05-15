from __future__ import annotations

import json
import sys
from pathlib import Path
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data" / "eval_cases" / "trade_support_30_cases.jsonl"
OUT = ROOT / "experiments" / "results" / "baseline_llm.jsonl"


def direct_answer(query: str) -> str:
    return (
        "문의 감사합니다. 제품 정보, 수량, 희망 일정, 배송지를 보내주시면 확인 후 안내드리겠습니다. "
        "정확한 견적과 진행 가능 여부는 담당자 확인 후 답변드릴 수 있습니다."
    )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with CASES.open(encoding="utf-8") as source, OUT.open("w", encoding="utf-8") as target:
        for line in source:
            case = json.loads(line)
            started = perf_counter()
            answer = direct_answer(case["query"])
            target.write(json.dumps({
                "id": case["id"],
                "query": case["query"],
                "gold_intent": case["intent"],
                "pred_intent": "general",
                "answer": answer,
                "latency_seconds": round(perf_counter() - started, 4),
            }, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
