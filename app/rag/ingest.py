from __future__ import annotations

from pathlib import Path

from app.rag.retriever import SimpleRetriever


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    retriever = SimpleRetriever.from_directory(root / "data" / "knowledge_base")
    print(f"Loaded {len(retriever.docs)} knowledge documents.")


if __name__ == "__main__":
    main()

