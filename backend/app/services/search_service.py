"""
search_service.py

Builds all 4 retrievers ONCE (at server startup) and exposes a single
search() function that dispatches to the right method by name.
Building retrievers per-request would reload models every time - too slow.
"""

from app.data.dataset_loader import load_corpus
from app.retrieval.tfidf_retriever import TfidfRetriever
from app.retrieval.bm25_retriever import Bm25Retriever
from app.retrieval.semantic_retriever import SemanticRetriever
from app.retrieval.hybrid_retriever import HybridRetriever

CORPUS_PATH = "../dataset/SciFact/corpus.jsonl"
EMBEDDINGS_DIR = "../embeddings"

VALID_METHODS = {"tfidf", "bm25", "semantic", "hybrid"}


class SearchService:
    def __init__(self):
        print("Loading corpus...")
        self.corpus = load_corpus(CORPUS_PATH)

        print("Building TF-IDF retriever...")
        self.tfidf = TfidfRetriever(self.corpus)

        print("Building BM25 retriever...")
        self.bm25 = Bm25Retriever(self.corpus)

        print("Building Semantic retriever (loading/generating embeddings)...")
        self.semantic = SemanticRetriever(self.corpus, embeddings_dir=EMBEDDINGS_DIR)

        print("Building Hybrid retriever...")
        self.hybrid = HybridRetriever(self.corpus, self.semantic)

        print("All retrievers ready.")

    def search(self, query: str, method: str, top_k: int = 10) -> list[dict]:
        if method not in VALID_METHODS:
            raise ValueError(f"Unknown method '{method}'. Must be one of {VALID_METHODS}")

        if method == "tfidf":
            results = self.tfidf.search(query, top_k=top_k)
        elif method == "bm25":
            results = self.bm25.search(query, top_k=top_k)
        elif method == "semantic":
            results = self.semantic.search(query, top_k=top_k)
        else:  # hybrid
            results = self.hybrid.search(query, candidate_k=50, top_k=top_k)

        output = []
        for doc_id, score in results:
            doc = self.corpus[doc_id]
            output.append({
                "doc_id": doc_id,
                "title": doc.title,
                "abstract": " ".join(doc.abstract),
                "score": round(score, 4),
                "method": method,
            })
        return output


# Singleton instance, built once when this module is first imported
search_service = SearchService()