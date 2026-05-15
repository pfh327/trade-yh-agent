# Demo Queries and Expected Behavior

## OEM/ODM

```text
로고 들어간 의류 라벨 3만 개 제작하고 싶은데 가능한가요?
```

Expected behavior:

- Intent: `oem_odm`
- Ask for logo/label file, desired delivery schedule, destination, material/spec if missing.
- Avoid saying production is guaranteed.

## Purchasing Agency

```text
1688 링크가 있는데 한국까지 구매대행 가능한가요? 수량은 500개입니다.
```

Expected behavior:

- Intent: `purchasing_agent`
- Ask for exact URL, option/spec, delivery address, inspection need.
- Explain supplier price and stock confirmation.

## Defect Claim

```text
중국에서 받은 제품 중 15%가 파손됐어요. 어떻게 대응해야 하나요?
```

Expected behavior:

- Intent: `defect_claim`
- Ask for photos/videos, total quantity, defective quantity, receipt date, order records, inspection history.
- Avoid promising refund or replacement.
- Recommend 담당자 review.

## Customs/Certification

```text
이 제품 한국 수입할 때 KC 인증이 필요한지 확인 가능한가요?
```

Expected behavior:

- Intent: `logistics_customs`
- Ask for product name, material, use case, HS code if available, quantity.
- Avoid final certification judgment.

