"""
hybrid_retriever.py

Proposed method: FAISS retrieves top-50 candidates, then a Cross-Encoder
re-scores each (query, doc) pair directly for higher-precision ranking,
and we keep the top-10.

Cross-Encoders are slower than bi-encoders (like SemanticRetriever) because
they score each pair jointly instead of comparing precomputed vectors —
that's why we only run it on a small candidate set (50), not the whole corpus.
"""

from sentence_transformers import CrossEncoder

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"


class HybridRetriever:
    def __init__(self, corpus: dict, semantic_retriever):
        """
        corpus: dict[doc_id -> Document]
        semantic_retriever: an already-built SemanticRetriever instance
            (reused so we don't re-embed the corpus twice)
        """
        self.corpus = corpus
        self.semantic_retriever = semantic_retriever
        self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

    def search(self, query: str, candidate_k: int = 50, top_k: int = 10) -> list[tuple[int, float]]:
        # Stage 1: FAISS retrieves broad candidates
        candidates = self.semantic_retriever.search(query, top_k=candidate_k)
        candidate_doc_ids = [doc_id for doc_id, _ in candidates]

        # Stage 2: Cross-Encoder re-scores each (query, doc) pair
        pairs = [(query, self.corpus[doc_id].full_text) for doc_id in candidate_doc_ids]
        rerank_scores = self.cross_encoder.predict(pairs)

        # Stage 3: sort by new scores, keep top_k
        scored = list(zip(candidate_doc_ids, rerank_scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [(doc_id, float(score)) for doc_id, score in scored[:top_k]]