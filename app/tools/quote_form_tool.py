from __future__ import annotations


def build_quote_checklist(intent: str) -> list[str]:
    common = ["제품명", "수량", "희망 납기", "배송지", "사진 또는 URL"]
    if intent == "oem_odm":
        return common + ["로고/라벨 파일", "재질", "샘플 필요 여부"]
    if intent == "purchasing_agent":
        return common + ["상품 옵션", "검품 필요 여부", "구매 플랫폼"]
    if intent == "defect_claim":
        return ["불량 사진/영상", "전체 수량", "불량 수량", "수령일", "주문/계약 자료"]
    return common

