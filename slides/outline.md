# 8-Minute Presentation Outline

## 1. Title and Motivation, 40 sec

- Project: TradeCare-Agent.
- Domain: Korea-China B2B trade customer support.
- Goal: support OEM/ODM, purchasing agency, market research, defect claims, logistics/customs inquiries.

## 2. Problem, 1 min

- Trade inquiries are incomplete: missing product photos, quantity, specifications, delivery date, inspection history, contract records, HS code, or certification context.
- Trade support is risk-sensitive: price, lead time, customs, certification, refund, and compensation cannot be guaranteed without verification.
- A single chatbot can hallucinate or overpromise.

## 3. Agent Architecture, 1 min 20 sec

- Intake Agent: classifies intent and finds missing fields.
- Retrieval Agent: searches service and trade knowledge documents.
- Trade Specialist Agent: drafts customer-facing guidance.
- Risk Agent: removes unsafe promises.
- Critic Agent: performs reflection and quality check.

## 4. RAG and Knowledge Base, 50 sec

- Uses local markdown knowledge documents.
- Knowledge covers company profile, OEM/ODM, purchasing agency, Yiwu market research, defect claim process, logistics/customs, quotation fields, and FAQ.
- RAG makes answers grounded in documented service scope.

## 5. Reflection and Risk Handling, 50 sec

- Critic checks missing information, grounding, human-review signal, and overpromising.
- Risk Agent rewrites phrases such as "guaranteed customs clearance" or "definite refund."

## 6. Web App Implementation, 1 min 20 sec

- Built a FastAPI app.
- Root page `/` serves the customer-center web app.
- `/api/chat` runs the Multi-Agent workflow.
- UI shows chat response, intent, critic score, missing fields, and optional RAG/Reflection trace.
- Can be deployed for `trade-yh.com` as `https://api.trade-yh.com/api/chat`.

## 7. Live Demo, 1 min 40 sec

Open:

```text
http://127.0.0.1:8000
```

Suggested query:

```text
중국에서 받은 제품 중 15%가 파손됐어요. 어떻게 대응해야 하나요?
```

Show:

- intent: `defect_claim`
- missing fields: photos/videos, total quantity, receipt date, order records, inspection history
- RAG evidence: defect claim process
- critic score
- final answer avoids refund guarantee

## 8. Evaluation, 1 min

- 30 benchmark cases.
- Baseline LLM vs Baseline RAG vs Proposed Agent.
- Key result: proposed agent improves required-information coverage.

```text
Baseline LLM: 0.139
Baseline RAG: 0.678
Proposed Agent: 0.967
```

## 9. Limitations and Ethics, 40 sec

- The agent is an intake and support assistant, not a final decision maker.
- Human review is required for customs, certification, legal, refund, compensation, and supplier-liability decisions.
- Customer data should be protected.

## 10. Conclusion, 20 sec

- TradeCare-Agent demonstrates Multi-Agent + RAG + Reflection in a realistic B2B trade customer-support domain.
- The project includes runnable code, web app, API server, prompts, knowledge base, evaluation benchmark, and GitHub repository.
