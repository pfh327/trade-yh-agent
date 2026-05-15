from __future__ import annotations

from app.agents.intake_agent import IntakeResult
from app.agents.llm_client import LLMClient


class TradeSpecialistAgent:
    """Drafts a practical trade customer-support answer."""

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
            f"[{idx + 1}] {item['title']}\n{item['snippet']}" for idx, item in enumerate(contexts[:4])
        )
        prompt = f"""
You are a Korea-China B2B trade customer-center specialist.
Answer in Korean.

Customer query:
{query}

Predicted intent: {intake.intent}
Required fields: {", ".join(intake.required_fields)}
Missing fields: {", ".join(intake.missing_fields)}

Retrieved company/service knowledge:
{context_text}

Write a concise but professional customer response. Requirements:
- classify the inquiry naturally,
- include a short required-information checklist,
- ask for missing high-impact information,
- explain the next process,
- do not promise final price, MOQ, lead time, customs clearance, certification, refund, or replacement,
- recommend human 담당자 confirmation for risk-sensitive cases.
""".strip()
        return self.llm_client.complete(prompt)

    def _run_rule_based(self, query: str, intake: IntakeResult, contexts: list[dict[str, str | float]]) -> str:
        context_lines = "\n".join(f"- {item['title']}: {item['snippet']}" for item in contexts[:3])
        missing = ", ".join(intake.missing_fields[:6]) if intake.missing_fields else "현재 문의에 핵심 정보가 비교적 포함되어 있습니다"
        checklist = ", ".join(intake.required_fields)
        intent_name = self._intent_name(intake.intent)

        return (
            f"문의 주신 내용은 {intent_name} 유형으로 보입니다.\n\n"
            f"정확한 진행 가능 여부, 단가, MOQ, 납기, 물류비는 중국 공급처와 담당자 확인 후 안내드리는 것이 안전합니다. "
            f"현재 단계에서는 다음 정보를 보내주시면 확인이 빨라집니다: {missing}.\n\n"
            f"필수 확인 정보 체크리스트: {checklist}.\n\n"
            f"권장 진행 절차는 1) 제품/요청사항 정리, 2) 중국 공급처 또는 시장 조사, "
            f"3) 단가/MOQ/납기/검품 조건 확인, 4) 물류·통관·라벨 이슈 검토, "
            f"5) 최종 견적 및 진행 방식 안내 순서입니다.\n\n"
            f"참고한 내부 지식:\n{context_lines}\n\n"
            f"사진, 링크, 수량, 희망 납기, 배송지와 함께 문의 목적을 보내주시면 "
            f"담당자가 구체 조건을 확인해 다음 답변을 드릴 수 있습니다."
        )

    def _intent_name(self, intent: str) -> str:
        names = {
            "oem_odm": "중국 OEM/ODM 제작 문의",
            "purchasing_agent": "중국 구매대행 문의",
            "market_research": "중국시장/이우시장 조사 문의",
            "defect_claim": "불량 및 클레임 대응 문의",
            "logistics_customs": "물류·통관·라벨 문의",
            "general": "일반 무역 상담 문의",
        }
        return names.get(intent, "일반 무역 상담 문의")
