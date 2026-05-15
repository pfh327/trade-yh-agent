from __future__ import annotations


RISKY_PHRASES = {
    "무조건 가능합니다": "공급처 확인 후 가능 여부를 안내드릴 수 있습니다",
    "100% 가능합니다": "조건 확인 후 진행 가능성을 검토할 수 있습니다",
    "반드시 환불": "증빙과 거래 조건 확인 후 클레임 가능성을 검토",
    "통관 보장": "통관 가능성은 품목, 서류, 인증 요건 확인이 필요",
    "인증 필요 없습니다": "인증 필요 여부는 품목과 용도에 따라 확인이 필요",
    "보상 가능합니다": "보상 가능성은 증빙과 거래 조건 확인 후 검토할 수 있습니다",
}


class RiskAgent:
    """Checks overpromising and compliance-sensitive language."""

    def run(self, draft: str) -> dict[str, object]:
        revised = draft
        flags: list[str] = []
        for risky, safer in RISKY_PHRASES.items():
            if risky in revised:
                flags.append(risky)
                revised = revised.replace(risky, safer)
        if "통관" in revised and "확인" not in revised:
            flags.append("customs_without_confirmation")
            revised += "\n\n통관 및 인증 관련 사항은 품목, 용도, 서류에 따라 달라질 수 있어 최종 확인이 필요합니다."
        return {"answer": revised, "risk_flags": flags}
