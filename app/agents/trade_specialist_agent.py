from __future__ import annotations

from app.agents.intake_agent import IntakeResult
from app.agents.llm_client import LLMClient


class TradeSpecialistAgent:
    """Drafts a concise trade customer-support answer."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client

    def run(self, query: str, intake: IntakeResult, contexts: list[dict[str, str | float]]) -> str:
        if self.llm_client and self.llm_client.enabled:
            answer = self._run_with_llm(query, intake, contexts)
            if answer:
                return answer
        return self._run_rule_based(query, intake, contexts)

    def _run_with_llm(self, query: str, intake: IntakeResult, contexts: list[dict[str, str | float]]) -> str | None:
        context_text = "\n\n".join(
            f"[{idx + 1}] {item['title']}\n{item['snippet']}" for idx, item in enumerate(contexts[:3])
        )
        prompt = f"""
You are a Korea-China B2B trade customer-center specialist.
Answer in Korean, concise and customer-friendly.
Use at most 6 short lines.

Customer query:
{query}

Intent: {intake.intent}
Missing fields: {", ".join(intake.missing_fields)}
Retrieved knowledge:
{context_text}

Requirements:
- Do not show internal RAG snippets.
- Do not mention "RAG" or "critic".
- Ask only the most important missing fields.
- Avoid guarantees about price, MOQ, lead time, customs, certification, refund, or replacement.
""".strip()
        return self.llm_client.complete(prompt)

    def _run_rule_based(self, query: str, intake: IntakeResult, contexts: list[dict[str, str | float]]) -> str:
        intent_name = self._intent_name(intake.intent)
        top_missing = intake.missing_fields[:4]
        missing_text = ", ".join(top_missing) if top_missing else "현재 정보로 1차 확인이 가능합니다"
        next_step = self._next_step(intake.intent)

        return (
            f"{intent_name}로 확인됩니다.\n\n"
            f"진행 가능 여부와 견적은 중국 공급처 확인 후 안내드릴 수 있습니다.\n"
            f"먼저 아래 정보를 보내주세요.\n"
            f"- {missing_text}\n\n"
            f"접수 후 {next_step}\n"
            f"확정 전까지 단가, MOQ, 납기, 통관 여부는 보장드리기 어렵습니다."
        )

    def _intent_name(self, intent: str) -> str:
        names = {
            "oem_odm": "OEM/ODM 제작 문의",
            "purchasing_agent": "중국 구매대행 문의",
            "market_research": "중국 시장조사 문의",
            "defect_claim": "불량/클레임 대응 문의",
            "logistics_customs": "물류·통관 문의",
            "general": "무역 상담 문의",
        }
        return names.get(intent, "무역 상담 문의")

    def _next_step(self, intent: str) -> str:
        steps = {
            "oem_odm": "제작 가능 여부, 예상 단가, MOQ, 샘플 가능 여부를 확인하겠습니다.",
            "purchasing_agent": "상품 옵션, 재고, 단가, 검품 가능 여부를 확인하겠습니다.",
            "market_research": "후보 공급처와 가격 범위를 조사하겠습니다.",
            "defect_claim": "증빙 자료를 정리해 공급처 클레임 가능성을 검토하겠습니다.",
            "logistics_customs": "품목과 서류 기준으로 물류·통관 확인이 필요한 부분을 검토하겠습니다.",
            "general": "담당자가 상담 방향을 확인하겠습니다.",
        }
        return steps.get(intent, steps["general"])
