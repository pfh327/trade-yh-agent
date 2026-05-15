# Deploying TradeCare-Agent for trade-yh.com

This repository contains the Agent engine and a FastAPI web API.

## 1. Local API Test

```powershell
pip install -r requirements.txt
uvicorn app.server:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/health
```

Send a chat request:

```powershell
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d "{\"message\":\"1688 링크가 있는데 구매대행 가능한가요?\"}"
```

## 2. Production Deployment

Deploy this repository to a server such as Render, Railway, Fly.io, AWS EC2, Naver Cloud, or Cafe24 VPS.

Recommended production command:

```bash
uvicorn app.server:app --host 0.0.0.0 --port 8000
```

If using a paid model/API, set:

```text
OPENAI_API_KEY=your_api_key
TRADECARE_USE_LLM=true
TRADECARE_MODEL=gpt-4.1-mini
```

If running without a paid model/API, omit those variables. The deterministic fallback agent will still work.

## 3. Domain Connection

Recommended API domain:

```text
https://api.trade-yh.com
```

Point `api.trade-yh.com` to the deployed server through your DNS provider. The website should call:

```text
https://api.trade-yh.com/api/chat
```

The server CORS configuration already allows:

```text
https://www.trade-yh.com
https://trade-yh.com
```

## 4. Homepage Widget

Use `web_widget/trade_yh_chat_widget.html` as the simplest front-end example.

Important:

- Change `TRADE_YH_AGENT_API` to the deployed API URL.
- Do not expose `OPENAI_API_KEY` in homepage JavaScript.
- Keep the API key only on the backend server.

## 5. Safety Notes

The homepage chatbot should not make final legal, customs, certification, refund, replacement, or delivery guarantees. Risk-sensitive cases should be escalated to a human 담당자.

