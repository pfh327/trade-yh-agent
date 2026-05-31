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
- Why five agents: trade support has different failure points for intent classification, evidence retrieval, answer drafting, risk filtering, and self-review, so the workflow separates these roles.
- Single-call chatbot risk: one model response may skip missing information, cite no company knowledge, or overpromise price, delivery, refund, customs, or certification.

## 4. RAG Knowledge Base Sources, 1 min

- Source location: `data/knowledge_base/*.md`.
- Source types: company profile, service descriptions, quotation required fields, FAQ, defect claim process, logistics/customs guidance.
- Domain sources were manually curated from the Yoon Hang Trade service scope, website-facing service information, and operator-provided 상담 rules.
- RAG role: retrieves relevant company/service knowledge before answer generation.
- Why this matters: compared with a single LLM, the answer is grounded in documented company policy and can cite service-specific required information.
- Example: OEM/ODM answers retrieve `services_oem_odm.md` and `quotation_required_fields.md`; defect claims retrieve `defect_claim_process.md`.

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

- Dataset: `data/eval_cases/trade_support_30_cases.jsonl`.
- Scale: 30 benchmark cases covering OEM/ODM, purchasing agency, market research, defect claims, logistics/customs, and general inquiries.
- Compared systems: Baseline LLM vs Baseline RAG vs Proposed Agent, all tested on the same 30 cases.
- Model setting: the reproducible submitted run uses deterministic local scripts without external GPT/Claude calls; the app can optionally use OpenAI `gpt-4.1-mini` when `OPENAI_API_KEY` is provided. Claude was not used in this experiment.
- Main metric shown below: `required_info_coverage`.
- Definition: for each case, we define required keywords or required information items; the score is the average fraction of those items included in the answer.
- Other logged metrics: intent accuracy, groundedness proxy, overpromise rate, human-review signal, and latency.
- Key result: proposed agent improves required-information coverage.

```text
Baseline LLM: 0.139
Baseline RAG: 0.678
Proposed Agent: 0.967
```

## 9. Qualitative Answer Comparison, 1 min

Same customer question: "Can you make a branded apparel/sample product in China?"

| Method | Typical answer behavior | Weakness |
| --- | --- | --- |
| General GPT | Gives broad generic advice about OEM production. | May not ask for all required trade information and may sound too confident. |
| GPT + RAG | Uses company/service documents and asks for some missing fields. | Still lacks a separate risk check and reflection loop. |
| TradeCare Agent | Classifies OEM/ODM intent, retrieves service rules, asks for images/specs/patterns/quantity/logo/delivery, and states that MOQ, sample cost, lead time, and feasibility require supplier confirmation. | More structured, safer, and closer to real customer-center intake. |

Main qualitative advantage: TradeCare Agent does not only answer the question; it turns an incomplete customer message into an actionable intake checklist while avoiding unsupported promises.

## 10. Limitations and Ethics, 40 sec

- The agent is an intake and support assistant, not a final decision maker.
- Human review is required for customs, certification, legal, refund, compensation, and supplier-liability decisions.
- Customer data should be protected.

## 11. Conclusion, 20 sec

- TradeCare-Agent demonstrates Multi-Agent + RAG + Reflection in a realistic B2B trade customer-support domain.
- The project includes runnable code, web app, API server, prompts, knowledge base, evaluation benchmark, and GitHub repository.
