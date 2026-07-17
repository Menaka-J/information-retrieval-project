"""
run_evaluation.py

Runs all 4 retrievers against claims_dev.jsonl (which has gold labels),
computes IR metrics for each, and prints/saves a comparison table.

Run from backend/:  python -m app.evaluation.run_evaluation
"""

import time
import json
import pandas as pd

from app.data.dataset_loader import load_corpus, load_claims
from app.retrieval.tfidf_retriever import TfidfRetriever
from app.retrieval.bm25_retriever import Bm25Retriever
from app.retrieval.semantic_retriever import SemanticRetriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.evaluation.metrics import precision_at_k, recall_at_k, f1_score, reciprocal_rank, ndcg_at_k

K = 10  # cutoff for Precision@K, Recall@K, nDCG@K


def evaluate_method(name: str, search_fn, claims: list) -> dict:
    """
    search_fn: a function that takes a query string and returns
               list of (doc_id, score), already sorted by relevance.
    """
    precisions, recalls, f1s, rrs, ndcgs, times = [], [], [], [], [], []

    for claim in claims:
        relevant_ids = claim.relevant_doc_ids
        if not relevant_ids:
            continue  # skip claims with no gold relevant docs

        start = time.perf_counter()
        results = search_fn(claim.claim)
        elapsed = time.perf_counter() - start

        retrieved_ids = [doc_id for doc_id, _ in results]

        p = precision_at_k(retrieved_ids, relevant_ids, K)
        r = recall_at_k(retrieved_ids, relevant_ids, K)
        f1 = f1_score(p, r)
        rr = reciprocal_rank(retrieved_ids, relevant_ids)
        ndcg = ndcg_at_k(retrieved_ids, relevant_ids, K)

        precisions.append(p)
        recalls.append(r)
        f1s.append(f1)
        rrs.append(rr)
        ndcgs.append(ndcg)
        times.append(elapsed)

    n = len(precisions)
    return {
        "Method": name,
        f"Precision@{K}": sum(precisions) / n,
        f"Recall@{K}": sum(recalls) / n,
        "F1": sum(f1s) / n,
        "MRR": sum(rrs) / n,
        f"nDCG@{K}": sum(ndcgs) / n,
        "Avg Time (s)": sum(times) / n,
        "Queries Evaluated": n,
    }


def main():
    print("Loading data...")
    corpus = load_corpus("../dataset/SciFact/corpus.jsonl")
    dev_claims = load_claims("../dataset/SciFact/claims_dev.jsonl")

    print("Building retrievers (this may take a while on first run)...")
    tfidf = TfidfRetriever(corpus)
    bm25 = Bm25Retriever(corpus)
    semantic = SemanticRetriever(corpus, embeddings_dir="../embeddings")
    hybrid = HybridRetriever(corpus, semantic)

    methods = [
        ("TF-IDF", lambda q: tfidf.search(q, top_k=K)),
        ("BM25", lambda q: bm25.search(q, top_k=K)),
        ("Semantic (SBERT+FAISS)", lambda q: semantic.search(q, top_k=K)),
        ("Hybrid (Cross-Encoder Re-rank)", lambda q: hybrid.search(q, candidate_k=50, top_k=K)),
    ]

    all_results = []
    for name, fn in methods:
        print(f"\nEvaluating: {name}...")
        result = evaluate_method(name, fn, dev_claims)
        all_results.append(result)
        print(result)

    df = pd.DataFrame(all_results)
    print("\n=== Final Comparison Table ===")
    print(df.to_string(index=False))

    df.to_csv("../docs/evaluation_results.csv", index=False)
    print("\nSaved to ../docs/evaluation_results.csv")


if __name__ == "__main__":
    main()