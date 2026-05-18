# TradeCare-Agent

Multi-Agent RAG with Reflection for Korea-China B2B trade customer support.

This project implements a web app and API for a Korea-China B2B trade agency customer center. It supports OEM/ODM inquiries, purchasing agency requests, China/Yiwu market research, defect claim handling, logistics, customs, labeling, and quotation intake.

## Run the App

```powershell
pip install -r requirements.txt
uvicorn app.server:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

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
  -> Web App
  -> FastAPI /api/chat
  -> IntakeAgent
  -> RetrievalAgent
  -> TradeSpecialistAgent
  -> RiskAgent
  -> CriticAgent
  -> Final response
```

## CLI Mode

```powershell
python -m app.main --query "1688 링크가 있는데 한국까지 구매대행 가능한가요? 수량은 500개입니다."
python -m app.main --json --query "중국에서 받은 제품 중 15%가 파손됐어요. 어떻게 대응해야 하나요?"
```

## Plus/API Mode

The app can run in two modes.

1. **Reproducible fallback mode**: no API key required.
2. **Paid LLM/API mode**: set `OPENAI_API_KEY` and `TRADECARE_USE_LLM=true`.

```powershell
$env:OPENAI_API_KEY="your_api_key"
$env:TRADECARE_USE_LLM="true"
$env:TRADECARE_MODEL="gpt-4.1-mini"
uvicorn app.server:app --host 127.0.0.1 --port 8000
```

## Run Evaluation

```powershell
python experiments/run_baseline_llm.py
python experiments/run_baseline_rag.py
python experiments/run_proposed_agent.py
python experiments/evaluate.py
```

## Website Deployment

For `https://www.trade-yh.com`, deploy this repository as a backend service and connect the homepage to:

```text
https://api.trade-yh.com/api/chat
```

The example homepage widget is in `web_widget/trade_yh_chat_widget.html`.

## Demo Queries

```text
로고 들어간 의류 라벨 3만 개 제작하고 싶은데 가능한가요?
1688 링크가 있는데 한국까지 구매대행 가능한가요?
중국에서 받은 제품 중 15%가 파손됐어요. 어떻게 대응해야 하나요?
이우시장 조사 요청하려면 어떤 정보를 보내야 하나요?
```

## Metrics

- Intent accuracy
- Required information coverage
- Groundedness proxy
- Overpromise rate
- Human review signal
- Latency

## Limitations and Ethics

This system should not make final legal, customs, certification, or liability decisions. It is designed to collect information, provide grounded procedural guidance, and recommend human review when needed. The agent must avoid promising availability, price, lead time, refund, customs clearance, or certification outcomes before supplier and expert confirmation.
