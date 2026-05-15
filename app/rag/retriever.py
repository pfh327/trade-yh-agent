from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


@dataclass
class Document:
    title: str
    path: str
    text: str


class SimpleRetriever:
    """Small reproducible TF-IDF retriever for local markdown knowledge."""

    def __init__(self, docs: list[Document]) -> None:
        self.docs = docs
        self.doc_tokens = [tokenize(doc.text + " " + doc.title) for doc in docs]
        self.idf = self._build_idf(self.doc_tokens)

    @classmethod
    def from_directory(cls, directory: Path) -> "SimpleRetriever":
        docs = []
        for path in sorted(directory.glob("*.md")):
            docs.append(Document(title=path.stem.replace("_", " "), path=str(path), text=path.read_text(encoding="utf-8")))
        return cls(docs)

    def search(self, query: str, top_k: int = 4) -> list[dict[str, str | float]]:
        query_vec = self._vectorize(tokenize(query))
        scored = []
        for doc, tokens in zip(self.docs, self.doc_tokens):
            score = self._cosine(query_vec, self._vectorize(tokens))
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "title": doc.title,
                "path": doc.path,
                "score": round(score, 4),
                "snippet": self._snippet(doc.text),
            }
            for score, doc in scored[:top_k]
        ]

    def _build_idf(self, token_lists: list[list[str]]) -> dict[str, float]:
        doc_count = len(token_lists)
        df: dict[str, int] = {}
        for tokens in token_lists:
            for token in set(tokens):
                df[token] = df.get(token, 0) + 1
        return {token: math.log((doc_count + 1) / (count + 1)) + 1 for token, count in df.items()}

    def _vectorize(self, tokens: list[str]) -> dict[str, float]:
        tf: dict[str, int] = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        return {token: count * self.idf.get(token, 1.0) for token, count in tf.items()}

    def _cosine(self, left: dict[str, float], right: dict[str, float]) -> float:
        numerator = sum(value * right.get(token, 0.0) for token, value in left.items())
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)

    def _snippet(self, text: str, max_chars: int = 220) -> str:
        collapsed = " ".join(text.split())
        return collapsed[:max_chars] + ("..." if len(collapsed) > max_chars else "")

