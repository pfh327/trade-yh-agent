from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.agents.orchestrator import TradeCareOrchestrator


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "data" / "knowledge_base"


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


app = FastAPI(
    title="Trade YH Agent API",
    description="Multi-Agent RAG customer support API for trade-yh.com.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.trade-yh.com",
        "https://trade-yh.com",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

agent = TradeCareOrchestrator(
    KNOWLEDGE_DIR,
    use_llm=env_flag("TRADECARE_USE_LLM", default=False),
    model=os.getenv("TRADECARE_MODEL"),
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    include_trace: bool = Field(default=False)


class ChatResponse(BaseModel):
    answer: str
    intent: str
    missing_fields: list[str]
    critic_score: int
    trace: dict[str, Any] | None = None


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "llm_enabled": agent.llm_client.enabled,
        "model": agent.llm_client.model,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = agent.run(request.message)
    return ChatResponse(
        answer=str(result["final_answer"]),
        intent=str(result["intent"]),
        missing_fields=list(result["missing_fields"]),
        critic_score=int(result["critic_score"]),
        trace=result if request.include_trace else None,
    )

