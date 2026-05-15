from __future__ import annotations

from dataclasses import dataclass


INTENT_KEYWORDS = {
    "oem_odm": ["oem", "odm", "제작", "생산", "로고", "샘플", "맞춤", "라벨", "패키지", "도면"],
    "purchasing_agent": ["구매대행", "1688", "타오바오", "알리바바", "링크", "구매", "사입", "공급처", "소량", "사보고"],
    "market_research": ["시장조사", "이우", "조사", "공장", "공급처", "가격 조사", "도매"],
    "defect_claim": ["불량", "파손", "클레임", "환불", "교환", "하자", "분쟁", "보상", "납품", "다릅니다", "작동하지", "깨졌", "찌그러"],
    "logistics_customs": ["통관", "물류", "배송", "운송", "원산지", "라벨", "kc", "인증", "관세", "해운", "항공", "비용"],
}

REQUIRED_FIELDS = {
    "oem_odm": ["제품명", "사진/도면/레퍼런스", "예상 수량", "로고/라벨 파일", "희망 납기", "배송지"],
    "purchasing_agent": ["상품 URL", "옵션/색상/규격", "수량", "배송지", "검품 필요 여부"],
    "market_research": ["제품명", "목표 단가", "예상 수량", "필요 인증/규격", "조사 목적"],
    "defect_claim": ["불량 사진/영상", "전체 수량", "불량 수량", "수령일", "계약/주문 자료", "검품 여부"],
    "logistics_customs": ["제품명", "HS code 또는 재질", "수량/중량/부피", "배송 조건", "목적지", "인증/라벨 필요 여부"],
    "general": ["문의 목적", "제품 정보", "예상 수량", "희망 일정"],
}


@dataclass
class IntakeResult:
    intent: str
    confidence: float
    required_fields: list[str]
    missing_fields: list[str]


class IntakeAgent:
    """Classifies a trade inquiry and identifies missing information."""

    def run(self, query: str) -> IntakeResult:
        lowered = query.lower()
        scores = {
            intent: sum(1 for keyword in keywords if keyword.lower() in lowered)
            for intent, keywords in INTENT_KEYWORDS.items()
        }
        best_intent = max(scores, key=scores.get)
        if scores[best_intent] == 0:
            best_intent = "general"
        confidence = min(0.95, 0.45 + scores.get(best_intent, 0) * 0.15)
        required = REQUIRED_FIELDS[best_intent]
        missing = [field for field in required if not self._field_appears(field, lowered)]
        return IntakeResult(best_intent, confidence, required, missing)

    def _field_appears(self, field: str, lowered_query: str) -> bool:
        hints = {
            "제품명": ["제품", "상품", "라벨", "의류", "부품", "박스", "포장", "용기", "공구"],
            "사진/도면/레퍼런스": ["사진", "도면", "이미지", "레퍼런스", "샘플"],
            "예상 수량": ["개", "수량", "pcs", "박스", "장", "만", "천"],
            "로고/라벨 파일": ["로고", "라벨", "ai", "pdf", "브랜드"],
            "희망 납기": ["납기", "언제", "까지", "일정", "한 달"],
            "배송지": ["한국", "서울", "부산", "배송지", "목적지"],
            "상품 URL": ["http", "1688", "taobao", "alibaba", "타오바오", "알리바바", "링크"],
            "옵션/색상/규격": ["옵션", "색상", "규격", "사이즈", "모델"],
            "수량": ["개", "수량", "pcs", "박스", "장", "만", "천"],
            "검품 필요 여부": ["검품", "검수"],
            "목표 단가": ["단가", "가격", "예산"],
            "필요 인증/규격": ["인증", "kc", "규격"],
            "조사 목적": ["시장조사", "조사", "공급처", "신제품"],
            "불량 사진/영상": ["사진", "영상", "동영상"],
            "전체 수량": ["전체", "총"],
            "불량 수량": ["불량", "%", "퍼센트", "파손"],
            "수령일": ["수령", "받았", "납품"],
            "계약/주문 자료": ["계약", "주문", "발주", "인보이스"],
            "검품 여부": ["검품", "검수"],
            "HS code 또는 재질": ["hs", "재질", "소재"],
            "수량/중량/부피": ["수량", "중량", "kg", "cbm", "부피"],
            "배송 조건": ["fob", "cif", "exw", "항공", "해운"],
            "목적지": ["한국", "서울", "부산", "목적지", "배송"],
            "인증/라벨 필요 여부": ["인증", "라벨", "원산지", "kc"],
            "문의 목적": ["문의", "가능", "상담", "처음"],
            "제품 정보": ["제품", "상품", "회사"],
            "희망 일정": ["일정", "납기", "언제"],
        }
        return any(hint in lowered_query for hint in hints.get(field, [field.lower()]))
