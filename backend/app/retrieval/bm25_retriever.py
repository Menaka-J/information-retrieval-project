"""
bm25_retriever.py

Traditional IR: BM25 ranking algorithm (stronger baseline than TF-IDF).
"""

from rank_bm25 import BM25Okapi
from app.preprocessing.text_preprocessor import preprocess


class Bm25Retriever:
    def __init__(self, corpus: dict):
        """
        corpus: dict[doc_id -> Document] from dataset_loader.load_corpus()
        """
        self.doc_ids = list(corpus.keys())
        tokenized_docs = [preprocess(corpus[doc_id].full_text) for doc_id in self.doc_ids]
        self.bm25 = BM25Okapi(tokenized_docs)

    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        """Returns list of (doc_id, score) sorted by relevance, highest first."""
        tokenized_query = preprocess(query)
        scores = self.bm25.get_scores(tokenized_query)

        ranked_idx = scores.argsort()[::-1][:top_k]
        return [(self.doc_ids[i], float(scores[i])) for i in ranked_idx]