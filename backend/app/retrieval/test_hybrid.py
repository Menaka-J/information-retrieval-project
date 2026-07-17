"""
Run from backend/:  python -m app.retrieval.test_hybrid

Downloads the cross-encoder model on first run (~small, faster than
sentence-transformer). Reuses cached corpus embeddings from Phase 6.
"""

from app.data.dataset_loader import load_corpus
from app.retrieval.semantic_retriever import SemanticRetriever
from app.retrieval.hybrid_retriever import HybridRetriever

corpus = load_corpus("../dataset/SciFact/corpus.jsonl")
semantic = SemanticRetriever(corpus, embeddings_dir="../embeddings")
hybrid = HybridRetriever(corpus, semantic)

query = "Vitamin D improves bone health"
results = hybrid.search(query, candidate_k=50, top_k=5)

print(f"\nQuery: {query}\n")
for doc_id, score in results:
    print(f"Score: {score:.4f} | doc_id: {doc_id} | {corpus[doc_id].title}")