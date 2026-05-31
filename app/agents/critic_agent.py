from __future__ import annotations

from app.agents.intake_agent import IntakeResult


class CriticAgent:
    """Reflects on answer quality without making the customer answer verbose."""

    def run(self, answer: str, intake: IntakeResult, contexts: list[dict[str, str | float]]) -> dict[str, object]:
        issues: list[str] = []
        score = 5

        if intake.missing_fields and not any(field in answer for field in intake.missing_fields[:3]):
            issues.append("missing_required_field_request")
            score -= 1
        if not contexts:
            issues.append("no_retrieved_context")
            score -= 1
        if any(phrase in answer for phrase in ["무조건", "100%", "보장됩니다", "반드시 환불"]):
            issues.append("overpromising")
            score -= 2
        if "담당자" not in answer and intake.intent in {"defect_claim", "logistics_customs"}:
            issues.append("needs_human_review")
            score -= 1

        return {"score": max(1, score), "issues": issues, "answer": answer}
