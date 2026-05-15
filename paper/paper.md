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

## 5. Experiments

We build a 30-case benchmark with 6 OEM/ODM cases, 6 purchasing agency cases, 5 market research cases, 5 defect claim cases, 5 logistics/customs cases, and 3 general or out-of-scope cases.

Baselines:

- Baseline LLM: direct response without retrieval or reflection.
- Baseline RAG: intent classification plus retrieval, but no role-separated risk or critic loop.
- Proposed: Multi-Agent + RAG + Reflection.

Metrics:

- Intent accuracy
- Groundedness proxy
- Overpromise rate
- Average latency

For human evaluation, we recommend a 1-5 rubric for required-information coverage, actionability, groundedness, and risk handling.

## 6. Limitations and Ethics

The system cannot make final legal, customs, certification, supplier liability, or refund decisions. Trade support often depends on documents, contracts, inspection records, supplier negotiation, and regulation. Therefore, the system should be used as an intake and support assistant, not as an autonomous decision maker.

Potential risks include hallucinated company capability, incorrect customs advice, privacy leakage in customer documents, and excessive automation of responsibility-sensitive disputes. Mitigations include retrieval grounding, risk filtering, critic reflection, human escalation, and explicit uncertainty wording.

## 7. Conclusion

TradeCare-Agent demonstrates how Multi-Agent design, RAG, and Reflection can be combined for a realistic Korea-China B2B trade customer-support task. The project provides runnable code, local knowledge documents, prompts, benchmark cases, baseline comparisons, and reproducible evaluation scripts.

