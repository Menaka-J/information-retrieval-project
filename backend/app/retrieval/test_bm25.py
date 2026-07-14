"""
Run from backend/:  python -m app.retrieval.test_bm25
"""

from app.data.dataset_loader import load_corpus
from app.retrieval.bm25_retriever import Bm25Retriever

corpus = load_corpus("../dataset/SciFact/corpus.jsonl")
retriever = Bm25Retriever(corpus)

query = "Vitamin D improves bone health"
results = retriever.search(query, top_k=5)

print(f"Query: {query}\n")
for doc_id, score in results:
    print(f"Score: {score:.4f} | doc_id: {doc_id} | {corpus[doc_id].title}")