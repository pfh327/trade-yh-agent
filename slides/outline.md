# 8-Minute Presentation Outline

## 1. Problem, 1 min

- Korea-China B2B trade customer inquiries are incomplete and risk-sensitive.
- Single-call chatbots can miss required fields or overpromise.

## 2. Task and Domain, 1 min

- Domain: trade agency customer support.
- Target services: OEM/ODM, purchasing agency, market research, defect claims, logistics/customs.

## 3. Architecture, 2 min

- Intake Agent
- Retrieval Agent
- Trade Specialist Agent
- Risk Agent
- Critic Agent
- Multi-Agent + RAG + Reflection

## 4. Demo, 2 min

Suggested live query:

```text
중국에서 받은 제품 중 15%가 파손됐어요. 어떻게 대응해야 하나요?
```

Show intent classification, retrieved knowledge, missing information, final answer, and critic score.

## 5. Evaluation, 1 min

- 30 benchmark cases.
- Baseline LLM vs Baseline RAG vs Proposed Agent.
- Metrics: intent accuracy, groundedness, overpromise rate, latency.

## 6. Limitations and Ethics, 1 min

- No final legal/customs/certification decisions.
- Human review for risk-sensitive cases.
- Avoid hallucinated service promises.

