# TradeCare-Agent: Multi-Agent RAG with Reflection for Safe Korea-China B2B Trade Consulting

## Abstract

Safe Korea-China B2B trade consulting requires accurate intake, domain-grounded guidance, and careful risk handling. Customers often ask incomplete questions about OEM production, purchasing agency, China market research, defect claims, logistics, customs, labeling, and certification. A single large language model response may miss required information or overpromise supplier, customs, or compensation outcomes. We propose TradeCare-Agent, a Multi-Agent customer-support architecture combining retrieval-augmented generation and reflection. The system separates inquiry classification, knowledge retrieval, trade-specialist response generation, risk review, and critic-based self-correction. We implement the system as a runnable FastAPI web app and evaluate it on a 30-case benchmark built for B2B Korea-China trade support. We compare it against a direct single-call baseline and a RAG-only baseline, and additionally organize 20 realistic customer-question cases for qualitative evaluation and demo preparation.

## 1. Introduction

B2B trade agency customers need practical answers, but their initial inquiries are often underspecified. For example, an OEM request may omit quantity, drawings, logo files, or delivery schedule. A defect claim may omit evidence, defect rate, inspection history, or transaction records. A customs question may require product category, material, HS code, and certification context.

This project targets a Korea-China trade agency customer center. The goal is not to replace human trade managers, but to collect required information, provide grounded procedural guidance, and reduce unsafe or hallucinated responses.

## 2. Related Work

Retrieval-Augmented Generation improves factual grounding by conditioning generation on retrieved external knowledge. ReAct-style agents combine reasoning and tool use for multi-step tasks. Reflexion and critic-based approaches introduce self-evaluation loops that allow agents to identify and correct weak outputs. TradeCare-Agent applies these ideas to a narrow B2B trade-support setting.

## 3. Task Definition

Input: a customer inquiry in Korean.

Output: a grounded customer-center response that classifies inquiry intent, requests missing required information, gives next-step guidance, uses retrieved service knowledge, and avoids overpromising price, lead time, customs clearance, certification, refund, or replacement.

Target intents are OEM/ODM, purchasing agency, market research, defect claim, logistics/customs, and general or out-of-scope inquiry.

## 4. Method

TradeCare-Agent consists of five agents: Intake Agent, Retrieval Agent, Trade Specialist Agent, Risk Agent, and Critic Agent.

The Intake Agent classifies the inquiry and identifies required missing fields. The Retrieval Agent searches local markdown knowledge documents using a reproducible TF-IDF retriever. The Trade Specialist Agent drafts a customer-facing answer using intake results and retrieved contexts. The Risk Agent revises unsafe wording such as unconditional availability, guaranteed refund, or guaranteed customs clearance. The Critic Agent evaluates answer quality and performs a lightweight reflection step.

We use five agents because Korea-China trade support has multiple distinct failure modes. Intake failures lead to missing product photos, quantity, specifications, inspection records, or delivery information. Retrieval failures lead to unsupported answers that do not reflect the company's documented service scope. Drafting failures make the answer hard for customers to act on. Risk failures can overpromise supplier availability, price, delivery, customs clearance, certification, refund, or compensation. Reflection failures leave these problems unchecked. Separating these roles makes each failure point explicit and allows the system to compare a single-call response against a structured Multi-Agent workflow.

### RAG Knowledge Base Sources

The RAG knowledge base is stored as local Markdown files in `data/knowledge_base/*.md`. It includes company profile information, OEM/ODM service guidance, purchasing agency guidance, Yiwu and China market research guidance, defect claim procedures, logistics/customs guidance, quotation required fields, and FAQ. These documents were manually curated from the Yoon Hang Trade service scope, website-facing service information, and operator-provided customer-service rules collected during project development.

This source design is important for the architecture justification. A single LLM response may answer from generic prior knowledge and miss company-specific constraints. In contrast, the Retrieval Agent grounds the answer in documented service rules, such as required OEM information, supplier confirmation requirements, defect evidence requirements, and customs/certification uncertainty. The downstream Risk Agent and Critic Agent then check whether the generated answer still follows these retrieved constraints.

## 5. System Implementation

We implement TradeCare-Agent as a local web application to demonstrate that the architecture is not only conceptual but runnable. The backend uses Python FastAPI with a Uvicorn ASGI server. The root endpoint `/` serves the customer-center user interface, and `/api/chat` executes the Multi-Agent workflow. A `/health` endpoint is provided for deployment and status checks.

The frontend is implemented with static HTML, CSS, and JavaScript. The interface shows the customer chat, the generated AI response, detected intent, critic score, required and missing information, and an optional RAG/Reflection trace. This layout allows a presenter or operator to inspect why the agent produced a certain answer rather than only seeing the final response.

The app can run without an external API key through deterministic fallback logic for reproducible demos. When `OPENAI_API_KEY` is provided, the project can optionally use an OpenAI-compatible model configuration, with `gpt-4.1-mini` as the default model name. The current submitted quantitative evaluation uses deterministic local scripts for reproducibility.

For future website deployment, the app can be connected to `trade-yh.com` through an embedded widget or iframe, with the API hosted separately, for example as `https://api.trade-yh.com/api/chat`. The current repository includes app code, static frontend files, prompts, local RAG documents, evaluation scripts, presentation materials, and deployment notes.

## 6. Experiments

We build a 30-case benchmark with 6 OEM/ODM cases, 6 purchasing agency cases, 5 market research cases, 5 defect claim cases, 5 logistics/customs cases, and 3 general or out-of-scope cases.

All systems are evaluated on the same dataset, `data/eval_cases/trade_support_30_cases.jsonl`, using the same metric script in `experiments/evaluate.py`.

Baselines:

- Baseline LLM: direct single-response baseline without retrieval or reflection.
- Baseline RAG: intent classification plus retrieval, but no role-separated risk or critic loop.
- Proposed: Multi-Agent + RAG + Reflection.

For reproducibility, the submitted quantitative results are generated by deterministic local scripts rather than external GPT or Claude API calls. The app implementation supports an optional OpenAI-compatible model setting, with default model `gpt-4.1-mini` when `OPENAI_API_KEY` is provided. Claude was not used in the reported experiment.

Metrics:

- Intent accuracy
- Groundedness proxy
- Required-information coverage
- Overpromise rate
- Human-review signal
- Average latency

The main reported score is required-information coverage. For each benchmark case, we define required keywords or information items, such as product photos, quantity, specifications, inspection evidence, delivery destination, or customs/certification context. The metric computes the fraction of required items included in the answer and averages it across 30 cases.

Results:

- Baseline LLM: 0.139 required-information coverage
- Baseline RAG: 0.678 required-information coverage
- Proposed Multi-Agent + RAG + Reflection: 0.967 required-information coverage

### Architecture-Level Performance Comparison

Table 1 summarizes the architecture-level comparison across the three evaluated systems. The purpose is to show whether each added architectural component contributes to safer and more complete trade-consulting answers.

| System | Architecture | Intent Accuracy | Grounding Proxy | Required-Info Coverage | Overpromise Rate | Human-Review Signal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline LLM | Direct single response without retrieval or reflection | 0.100 | 0.000 | 0.139 | 0.000 | 1.000 |
| Baseline RAG | Intake classification + retrieval, no risk/critic loop | 1.000 | 0.900 | 0.678 | 0.000 | 1.000 |
| TradeCare-Agent | Intake + Retrieval + Specialist + Risk + Critic | 1.000 | 0.900 | 0.967 | 0.000 | 1.000 |

The comparison indicates that retrieval alone improves grounding and required-information coverage compared with a direct single-response baseline. However, the full Multi-Agent workflow further improves required-information coverage from 0.678 to 0.967 because the Specialist, Risk, and Critic stages explicitly request task-specific missing fields and verify the answer before final output. In this project, overpromise rate is zero for all submitted deterministic runs because the baseline scripts already use conservative wording; therefore, required-information coverage is the most informative metric for comparing the architectures.

We also interpret the comparison as an ablation-style result. Removing RAG reduces company-policy grounding. Removing the Risk Agent weakens control over unsupported commitments, such as final price, MOQ, delivery time, customs clearance, certification, refund, or compensation. Removing the Critic Agent weakens reflection on whether the answer actually includes the required intake fields. Therefore, the full architecture is justified not only by a higher score but also by clearer operational control over trade-consulting failure modes.

### Qualitative Comparison

We also compare the answer behavior qualitatively. For an OEM/sample-production inquiry, a general GPT-style baseline tends to provide broad generic guidance about manufacturing. It may be fluent, but it can omit task-specific intake information such as product images, detailed specifications, patterns, quantity, logo/package files, desired delivery date, and destination. It may also imply feasibility before supplier confirmation.

The RAG-only baseline improves grounding because it retrieves service documents such as `services_oem_odm.md` and `quotation_required_fields.md`. However, without a separate Risk Agent and Critic Agent, the system has weaker control over unsafe commitments and weaker reflection on whether the final answer actually requested the required fields.

TradeCare-Agent improves the response by combining all three steps. It classifies the inquiry as OEM/ODM, retrieves relevant knowledge-base documents, asks for concrete missing information, and explicitly states that MOQ, sample cost, lead time, production feasibility, customs, certification, refund, or compensation must be confirmed before final guidance. Therefore, the proposed system is not only more grounded than a single LLM response, but also more operationally useful for a real customer-center intake workflow.

### 20 Customer-Question Cases

In addition to the 30-case quantitative benchmark, we prepared 20 realistic customer-question cases for presentation and qualitative evaluation. These cases cover customs delay, trade contract review, EU apparel export documents, shipment information correction, customs declaration amount correction, food import quarantine, customs seizure, FOB cost responsibility, low-risk payment methods, cargo damage claims, electronic-product import tariffs, certificate-of-origin reissue, consolidated cargo customs declaration, CIF/CFR insurance responsibility, overdue customs clearance and auction risk, Chinese partner import/export qualification lookup, air and sea freight calculation, consignee cargo abandonment, FTA tariff preference evidence, and tariff late-fee reduction.

For each case, we define an expected answer core, or gold-standard checklist. For example, a customs-delay inquiry should include delay-cause checking, official customs inquiry, and whether additional documents are required. A cargo-damage case should include responsibility analysis, claim documents, claim procedure, and insurance linkage. These 20 cases are used to show that TradeCare-Agent can be extended from project evaluation into a practical customer-service FAQ and demo scenario library.

For human evaluation, we recommend a 1-5 rubric for required-information coverage, actionability, groundedness, and risk handling.

## 7. Limitations and Ethics

The system cannot make final legal, customs, certification, supplier liability, or refund decisions. Trade support often depends on documents, contracts, inspection records, supplier negotiation, and regulation. Therefore, the system should be used as an intake and support assistant, not as an autonomous decision maker.

Potential risks include hallucinated company capability, incorrect customs advice, privacy leakage in customer documents, and excessive automation of responsibility-sensitive disputes. Mitigations include retrieval grounding, risk filtering, critic reflection, human escalation, and explicit uncertainty wording.

## 8. Evaluation Prompt and Reproducibility

In addition to the deterministic script-based metrics, the project defines an evaluation prompt that can be used for human evaluation or LLM-as-a-judge style qualitative review. This prompt is not required to reproduce the numeric results in `experiments/results/summary.json`; instead, it documents how answer quality can be reviewed consistently.

### Reflection/Critic Evaluation Prompt

```text
You are an evaluator for a Korea-China B2B trade customer-support agent.

Given:
1. Customer inquiry
2. Retrieved knowledge snippets
3. Agent answer
4. Gold required information items

Evaluate the answer using the following criteria:

1. Required-information coverage:
   Does the answer request the information needed for the task?
   Examples: product photo, specification, quantity, logo/package file,
   desired delivery date, defect evidence, order record, customs/certification context.

2. Groundedness:
   Is the answer consistent with the retrieved company/service knowledge?
   Does it avoid unsupported claims beyond the knowledge base?

3. Risk control:
   Does the answer avoid promising final price, MOQ, lead time, customs clearance,
   certification, refund, replacement, or compensation before confirmation?

4. Actionability:
   Does the answer provide a clear next step for the customer or operator?

5. Human-review signal:
   Does the answer indicate human or expert review when the issue involves
   customs, certification, legal responsibility, refund, compensation, or supplier liability?

Return:
{
  "required_info_coverage": 1-5,
  "groundedness": 1-5,
  "risk_control": 1-5,
  "actionability": 1-5,
  "human_review_signal": "PASS" or "FAIL",
  "overall_comment": "short explanation",
  "revision_needed": true or false,
  "revision_instruction": "specific revision if needed"
}
```

The deterministic evaluation script uses keyword-based required-information coverage for reproducibility, while the above prompt supports qualitative review of answer quality. All evaluation cases, generated outputs, and scripts are included in the repository so that the reported comparison can be reproduced or extended.

## 9. Conclusion

TradeCare-Agent demonstrates how Multi-Agent design, RAG, and Reflection can be combined for a realistic Korea-China B2B trade customer-support task. The project provides runnable code, a FastAPI web app, local knowledge documents, prompts, benchmark cases, 20 realistic customer-question cases, baseline comparisons, reproducible evaluation scripts, presentation materials, and GitHub repository assets.
