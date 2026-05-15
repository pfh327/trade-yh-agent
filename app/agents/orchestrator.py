from __future__ import annotations

from pathlib import Path
from time import perf_counter

from app.agents.critic_agent import CriticAgent
from app.agents.intake_agent import IntakeAgent
from app.agents.llm_client import LLMClient
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.risk_agent import RiskAgent
from app.agents.trade_specialist_agent import TradeSpecialistAgent


class TradeCareOrchestrator:
    """Coordinates the Multi-Agent + RAG + Reflection workflow."""

    def __init__(self, knowledge_dir: Path, use_llm: bool = False, model: str | None = None) -> None:
        self.intake = IntakeAgent()
        self.retrieval = RetrievalAgent(knowledge_dir)
        self.llm_client = LLMClient(model=model, enabled=use_llm)
        self.specialist = TradeSpecialistAgent(self.llm_client)
        self.risk = RiskAgent()
        self.critic = CriticAgent()

    def run(self, query: str) -> dict[str, object]:
        started = perf_counter()
        intake = self.intake.run(query)
        contexts = self.retrieval.run(query, intake.intent)
        draft = self.specialist.run(query, intake, contexts)
        risk_result = self.risk.run(draft)
        critique = self.critic.run(str(risk_result["answer"]), intake, contexts)

        return {
            "query": query,
            "intent": intake.intent,
            "intent_confidence": intake.confidence,
            "required_fields": intake.required_fields,
            "missing_fields": intake.missing_fields,
            "retrieved_contexts": contexts,
            "risk_flags": risk_result["risk_flags"],
            "critic_score": critique["score"],
            "critic_issues": critique["issues"],
            "llm_enabled": self.llm_client.enabled,
            "model": self.llm_client.model,
            "latency_seconds": round(perf_counter() - started, 4),
            "final_answer": critique["answer"],
        }
