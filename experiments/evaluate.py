from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "experiments" / "results"
CASES = ROOT / "data" / "eval_cases" / "trade_support_30_cases.jsonl"


def load_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file]


def load_cases() -> dict[str, dict[str, object]]:
    return {row["id"]: row for row in load_jsonl(CASES)}


def answer_text(row: dict[str, object]) -> str:
    return str(row.get("answer", row.get("final_answer", "")))


def score(records: list[dict[str, object]], cases: dict[str, dict[str, object]]) -> dict[str, float]:
    if not records:
        return {}
    intent_hits = sum(1 for row in records if row.get("pred_intent", row.get("intent")) == row.get("gold_intent"))
    grounded = sum(1 for row in records if row.get("contexts") or row.get("retrieved_contexts"))
    overpromise = sum(1 for row in records if any(term in answer_text(row) for term in ["무조건", "100%", "보장", "반드시 환불"]))
    human_review = sum(1 for row in records if "담당자" in answer_text(row) or "확인" in answer_text(row))
    coverage_scores = []
    for row in records:
        case = cases.get(str(row.get("id")), {})
        keywords = case.get("required_keywords", [])
        if not keywords:
            continue
        text = answer_text(row)
        hits = sum(1 for keyword in keywords if str(keyword) in text)
        coverage_scores.append(hits / len(keywords))
    avg_latency = sum(float(row.get("latency_seconds", 0.0)) for row in records) / len(records)
    return {
        "n": len(records),
        "intent_accuracy": round(intent_hits / len(records), 3),
        "groundedness_proxy": round(grounded / len(records), 3),
        "required_info_coverage": round(sum(coverage_scores) / len(coverage_scores), 3) if coverage_scores else 0.0,
        "overpromise_rate": round(overpromise / len(records), 3),
        "human_review_signal": round(human_review / len(records), 3),
        "avg_latency_seconds": round(avg_latency, 4),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cases = load_cases()
    summary = {
        "baseline_llm": score(load_jsonl(RESULTS / "baseline_llm.jsonl"), cases),
        "baseline_rag": score(load_jsonl(RESULTS / "baseline_rag.jsonl"), cases),
        "proposed_agent": score(load_jsonl(RESULTS / "proposed_agent.jsonl"), cases),
    }
    out = RESULTS / "summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
