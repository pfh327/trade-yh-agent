from __future__ import annotations

from app.agents.intake_agent import IntakeResult


class CriticAgent:
    """Reflects on answer quality and requests lightweight revision if needed."""

    def run(self, answer: str, intake: IntakeResult, contexts: list[dict[str, str | float]]) -> dict[str, object]:
        issues: list[str] = []
        score = 5

        if intake.missing_fields and not any(field in answer for field in intake.missing_fields[:3]):
            issues.append("missing_required_field_request")
            score -= 1
        if not contexts:
            issues.append("no_retrieved_context")
            score -= 1
        if "참고한 내부 지식" not in answer and contexts:
            issues.append("no_grounding_signal")
            score -= 1
        if any(phrase in answer for phrase in ["무조건", "100%", "보장", "반드시 환불"]):
            issues.append("overpromising")
            score -= 2
        if "담당자" not in answer and intake.intent in {"defect_claim", "logistics_customs"}:
            issues.append("needs_human_review")
            score -= 1

        revised = answer
        if issues:
            revised += (
                "\n\n추가 확인: 위 안내는 초기 상담 기준이며, 실제 진행 여부와 비용은 "
                "제품 자료, 거래 조건, 공급처 확인 후 확정됩니다."
            )
        return {"score": max(1, score), "issues": issues, "answer": revised}
