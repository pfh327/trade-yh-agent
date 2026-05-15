# TradeCare-Agent

Multi-Agent RAG with Reflection for Korea-China B2B trade customer support.

This project designs a customer-support AI agent for a Korea-China trade agency business such as OEM/ODM sourcing, purchasing agency, Yiwu/China market research, defect claim handling, logistics, customs, labeling, and quotation intake.

## Why This Is an Agent Project

The system is not a single chatbot call. It separates the customer-support workflow into specialized agents:

- **Intake Agent**: classifies the inquiry and extracts missing fields.
- **Retrieval Agent**: retrieves relevant company/service knowledge from local documents.
- **Trade Specialist Agent**: writes a practical B2B customer response.
- **Risk Agent**: removes overpromising or compliance-sensitive wording.
- **Critic Agent**: reflects on answer quality and adds a correction note when needed.

This satisfies three course requirements at once:

- **Multi-Agent**
- **RAG**
- **Reflection / Self-Correction**

## Architecture

```text
User inquiry
  -> IntakeAgent
  -> RetrievalAgent
  -> TradeSpecialistAgent
  -> RiskAgent
  -> CriticAgent
  -> Final response
```

## Plus/API Mode

The project can run in two modes.

1. **Reproducible fallback mode**: no API key required. Rule-based agent logic is used so the professor can run the repository immediately.
2. **Paid LLM/API mode**: set `OPENAI_API_KEY` and run with `--use-llm`. The Specialist Agent uses a stronger model while the Intake, RAG, Risk, and Critic stages remain explicit and evaluable.

```powershell
$env:OPENAI_API_KEY="your_api_key"
$env:TRADECARE_MODEL="gpt-4.1-mini"
python -m app.main --use-llm --query "1688 링크가 있는데 한국까지 구매대행 가능한가요? 수량은 500개입니다."
```

## Quick Start

```powershell
python -m app.main --query "1688 링크가 있는데 한국까지 구매대행 가능한가요? 수량은 500개입니다."
python -m app.main --json --query "중국에서 받은 제품 중 15%가 파손됐어요. 어떻게 대응해야 하나요?"
```

## Run Evaluation

```powershell
python experiments/run_baseline_llm.py
python experiments/run_baseline_rag.py
python experiments/run_proposed_agent.py
python experiments/evaluate.py
```

## Run as Website API

For `https://www.trade-yh.com`, run the agent as a FastAPI server and connect the homepage chat widget to `/api/chat`.

Local test:

```powershell
uvicorn app.server:app --host 127.0.0.1 --port 8000
```

Health check:

```powershell
curl http://127.0.0.1:8000/health
```

Chat API:

```powershell
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d "{\"message\":\"1688 링크가 있는데 구매대행 가능한가요?\"}"
```

Production example:

```text
https://api.trade-yh.com/api/chat
```

When deploying with a paid model/API, set environment variables on the server:

```text
OPENAI_API_KEY=your_api_key
TRADECARE_USE_LLM=true
TRADECARE_MODEL=gpt-4.1-mini
```

The example homepage widget is in `web_widget/trade_yh_chat_widget.html`. Change `TRADE_YH_AGENT_API` to your deployed API URL.

The evaluation dataset contains 30 trade customer-support cases across OEM/ODM, purchasing agency, market research, defect handling, logistics/customs, and out-of-scope requests.

## Baselines

- **Baseline LLM**: direct answer without retrieval or reflection.
- **Baseline RAG**: direct answer with retrieved knowledge.
- **Proposed Agent**: Multi-Agent + RAG + Reflection.

## Metrics

- Intent accuracy
- Required information coverage
- Groundedness proxy
- Overpromise rate
- Human review signal
- Latency

## Demo Queries

```text
로고 들어간 의류 라벨 3만 개 제작하고 싶은데 가능한가요?
1688 링크가 있는데 한국까지 구매대행 가능한가요?
중국에서 받은 제품 중 15%가 파손됐어요. 어떻게 대응해야 하나요?
이우시장 조사 요청하려면 어떤 정보를 보내야 하나요?
```

## Limitations and Ethics

This system should not make final legal, customs, certification, or liability decisions. It is designed to collect information, provide grounded procedural guidance, and recommend human review when needed. The agent must avoid promising availability, price, lead time, refund, customs clearance, or certification outcomes before supplier and expert confirmation.
