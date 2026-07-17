"""
metrics.py

Standard IR evaluation metrics, computed per-query then averaged.
"""

import math


def precision_at_k(retrieved_ids: list[int], relevant_ids: set[int], k: int) -> float:
    top_k = retrieved_ids[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / len(top_k)


def recall_at_k(retrieved_ids: list[int], relevant_ids: set[int], k: int) -> float:
    if not relevant_ids:
        return 0.0
    top_k = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / len(relevant_ids)


def f1_score(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def reciprocal_rank(retrieved_ids: list[int], relevant_ids: set[int]) -> float:
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved_ids: list[int], relevant_ids: set[int], k: int) -> float:
    top_k = retrieved_ids[:k]

    dcg = 0.0
    for i, doc_id in enumerate(top_k, start=1):
        rel = 1.0 if doc_id in relevant_ids else 0.0
        dcg += rel / math.log2(i + 1)

    ideal_hits = min(len(relevant_ids), k)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))

    if idcg == 0:
        return 0.0
    return dcg / idcg