from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import md5
from pathlib import Path
import re
from typing import Any


TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass
class SearchResult:
    record_id: int
    text: str
    metadata: dict[str, Any]
    score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.record_id,
            "text": self.text,
            "metadata": self.metadata,
            "score": round(self.score, 4),
        }


class MiniSimilaritySystem:
    """
    Minimal similarity system:
    - accepts text input
    - generates embeddings
    - stores them in a local JSON file
    - retrieves top-k similar matches
    """

    def __init__(self, store_path: str = "mini_similarity_store.json", embedding_dim: int = 128) -> None:
        self.store_path = Path(store_path)
        self.embedding_dim = embedding_dim
        self._init_store()

    def _init_store(self) -> None:
        if not self.store_path.exists():
            self._write_store({"next_id": 1, "records": []})

    def _read_store(self) -> dict[str, Any]:
        with self.store_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_store(self, payload: dict[str, Any]) -> None:
        with self.store_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=True, indent=2)

    def add_record(self, text: str, metadata: dict[str, Any] | None = None) -> int:
        cleaned = self._validate_text(text)
        embedding = self.embed_text(cleaned)
        created_at = datetime.now(timezone.utc).isoformat()

        store = self._read_store()
        record_id = int(store["next_id"])
        store["next_id"] = record_id + 1
        store["records"].append(
            {
                "id": record_id,
                "text": cleaned,
                "metadata": metadata or {},
                "embedding": embedding,
                "created_at": created_at,
            }
        )
        self._write_store(store)
        return record_id

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        cleaned_query = self._validate_text(query)
        query_embedding = self.embed_text(cleaned_query)
        store = self._read_store()

        scored: list[SearchResult] = []
        for record in store["records"]:
            embedding = record["embedding"]
            score = self.cosine_similarity(query_embedding, embedding)
            scored.append(
                SearchResult(
                    record_id=record["id"],
                    text=record["text"],
                    metadata=record["metadata"],
                    score=score,
                )
            )

        ranked = sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]
        return [item.to_dict() for item in ranked]

    def embed_text(self, text: str) -> list[float]:
        tokens = self._tokenize(text)
        if not tokens:
            raise ValueError("Text does not contain enough valid tokens to embed.")

        vector = [0.0] * self.embedding_dim
        for token in tokens:
            bucket = self._stable_bucket(token)
            vector[bucket] += 1.0

        return self._normalize_vector(vector)

    def cosine_similarity(self, a: list[float], b: list[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def _validate_text(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        cleaned = " ".join(text.strip().split())
        if not cleaned:
            raise ValueError("Input text cannot be empty.")
        if len(cleaned) > 2000:
            raise ValueError("Input text exceeds the maximum allowed length.")
        return cleaned

    def _tokenize(self, text: str) -> list[str]:
        return TOKEN_RE.findall(text.lower())

    def _stable_bucket(self, token: str) -> int:
        digest = md5(token.encode("utf-8")).hexdigest()
        return int(digest, 16) % self.embedding_dim

    def _normalize_vector(self, vector: list[float]) -> list[float]:
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]


if __name__ == "__main__":
    system = MiniSimilaritySystem()

    samples = [
        ("Looking for AI automation for our campaign launch", {"type": "lead"}),
        ("Need personalised recommendations for e-commerce users", {"type": "recommendation"}),
        ("Want better lead scoring and sales intelligence", {"type": "lead_intelligence"}),
        ("Seeking customer segmentation insights for marketing", {"type": "analytics"}),
    ]

    for text, metadata in samples:
        system.add_record(text, metadata)

    results = system.search("Need AI support for campaign automation", top_k=3)
    for item in results:
        print(item)
