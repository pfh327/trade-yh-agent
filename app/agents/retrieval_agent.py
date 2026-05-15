from __future__ import annotations

from pathlib import Path

from app.rag.retriever import SimpleRetriever


class RetrievalAgent:
    """Retrieves relevant local knowledge-base passages."""

    def __init__(self, knowledge_dir: Path) -> None:
        self.retriever = SimpleRetriever.from_directory(knowledge_dir)

    def run(self, query: str, intent: str) -> list[dict[str, str | float]]:
        return self.retriever.search(f"{intent} {query}", top_k=4)

