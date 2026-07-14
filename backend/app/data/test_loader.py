"""
test_loader.py

Quick sanity check for dataset_loader.py. Run this once to confirm
the dataset loads correctly and to see basic stats about it.

Run from the backend/ folder:
    python -m app.data.test_loader
"""

from app.data.dataset_loader import load_corpus, load_claims, load_test_claims

DATASET_DIR = "../dataset/SciFact"


def main():
    corpus = load_corpus(f"{DATASET_DIR}/corpus.jsonl")
    train_claims = load_claims(f"{DATASET_DIR}/claims_train.jsonl")
    dev_claims = load_claims(f"{DATASET_DIR}/claims_dev.jsonl")
    test_claims = load_test_claims(f"{DATASET_DIR}/claims_test.jsonl")

    print(f"Corpus size: {len(corpus)} documents")
    print(f"Train claims: {len(train_claims)}")
    print(f"Dev claims:   {len(dev_claims)}")
    print(f"Test claims:  {len(test_claims)} (unlabeled, demo-only)")

    # How many dev claims actually have a non-empty relevant_doc_ids set?
    dev_with_relevant = [c for c in dev_claims if len(c.relevant_doc_ids) > 0]
    print(f"\nDev claims with at least 1 relevant doc: {len(dev_with_relevant)} / {len(dev_claims)}")

    # Show one fully parsed example
    example = dev_claims[1] if len(dev_claims) > 1 else dev_claims[0]
    print("\n--- Example parsed claim ---")
    print(f"ID: {example.id}")
    print(f"Claim: {example.claim}")
    print(f"Relevant doc_ids (gold): {example.relevant_doc_ids}")

    if example.relevant_doc_ids:
        first_doc_id = next(iter(example.relevant_doc_ids))
        if first_doc_id in corpus:
            doc = corpus[first_doc_id]
            print(f"\n--- Matching document (doc_id={first_doc_id}) ---")
            print(f"Title: {doc.title}")
            print(f"Full text length: {len(doc.full_text)} chars")


if __name__ == "__main__":
    main()