"""
Run from backend/:  python -m app.retrieval.test_semantic

First run will be slow (embedding ~5183 docs on CPU, a few minutes).
After that, it loads from cache instantly.
"""

from app.data.dataset_loader import load_corpus
from app.retrieval.semantic_retriever import SemanticRetriever

corpus = load_corpus("../dataset/SciFact/corpus.jsonl")
retriever = SemanticRetriever(corpus, embeddings_dir="../embeddings")

query = "Vitamin D improves bone health"
results = retriever.search(query, top_k=5)

print(f"\nQuery: {query}\n")
for doc_id, score in results:
    print(f"Score: {score:.4f} | doc_id: {doc_id} | {corpus[doc_id].title}")