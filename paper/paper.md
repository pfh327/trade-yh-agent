# TradeCare-Agent: Multi-Agent RAG with Reflection for Korea-China B2B Trade Customer Support

## Abstract

Korea-China B2B trade customer support requires accurate intake, domain-grounded guidance, and careful risk handling. Customers often ask incomplete questions about OEM production, purchasing agency, China market research, defect claims, logistics, customs, labeling, and certification. A single large language model response may miss required information or overpromise supplier, customs, or compensation outcomes. We propose TradeCare-Agent, a Multi-Agent customer-support architecture combining retrieval-augmented generation and reflection. The system separates inquiry classification, knowledge retrieval, trade-specialist response generation, risk review, and critic-based self-correction. We evaluate the system on a 30-case benchmark built for B2B Korea-China trade support and compare it against a direct single-call baseline and a RAG-only baseline.

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

## 5. Experiments

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

### Qualitative Comparison

We also compare the answer behavior qualitatively. For an OEM/sample-production inquiry, a general GPT-style baseline tends to provide broad generic guidance about manufacturing. It may be fluent, but it can omit task-specific intake information such as product images, detailed specifications, patterns, quantity, logo/package files, desired delivery date, and destination. It may also imply feasibility before supplier confirmation.

The RAG-only baseline improves grounding because it retrieves service documents such as `services_oem_odm.md` and `quotation_required_fields.md`. However, without a separate Risk Agent and Critic Agent, the system has weaker control over unsafe commitments and weaker reflection on whether the final answer actually requested the required fields.

TradeCare-Agent improves the response by combining all three steps. It classifies the inquiry as OEM/ODM, retrieves relevant knowledge-base documents, asks for concrete missing information, and explicitly states that MOQ, sample cost, lead time, production feasibility, customs, certification, refund, or compensation must be confirmed before final guidance. Therefore, the proposed system is not only more grounded than a single LLM response, but also more operationally useful for a real customer-center intake workflow.

For human evaluation, we recommend a 1-5 rubric for required-information coverage, actionability, groundedness, and risk handling.

## 6. Limitations and Ethics

The system cannot make final legal, customs, certification, supplier liability, or refund decisions. Trade support often depends on documents, contracts, inspection records, supplier negotiation, and regulation. Therefore, the system should be used as an intake and support assistant, not as an autonomous decision maker.

Potential risks include hallucinated company capability, incorrect customs advice, privacy leakage in customer documents, and excessive automation of responsibility-sensitive disputes. Mitigations include retrieval grounding, risk filtering, critic reflection, human escalation, and explicit uncertainty wording.

## 7. Conclusion

TradeCare-Agent demonstrates how Multi-Agent design, RAG, and Reflection can be combined for a realistic Korea-China B2B trade customer-support task. The project provides runnable code, local knowledge documents, prompts, benchmark cases, baseline comparisons, and reproducible evaluation scripts.
