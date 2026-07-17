"""
semantic_retriever.py

AI-based IR: dense embeddings (Sentence Transformer) + FAISS vector search.
Unlike TF-IDF/BM25, this does NOT use the traditional preprocessing
pipeline — the model expects natural, raw text.

Embeddings are cached to disk (embeddings/) so we only compute them once.
"""

import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-mpnet-base-v2"


class SemanticRetriever:
    def __init__(self, corpus: dict, embeddings_dir: str = "embeddings"):
        self.doc_ids = list(corpus.keys())
        self.corpus = corpus
        self.embeddings_dir = Path(embeddings_dir)
        self.embeddings_dir.mkdir(exist_ok=True)

        self.model = SentenceTransformer(MODEL_NAME)

        emb_path = self.embeddings_dir / "corpus_embeddings.npy"
        index_path = self.embeddings_dir / "faiss.index"

        if emb_path.exists() and index_path.exists():
            print("Loading cached embeddings + FAISS index...")
            self.embeddings = np.load(emb_path)
            self.index = faiss.read_index(str(index_path))
        else:
            print("No cache found. Generating embeddings (one-time, may take a few minutes)...")
            texts = [corpus[doc_id].full_text for doc_id in self.doc_ids]
            self.embeddings = self.model.encode(
                texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True
            )
            np.save(emb_path, self.embeddings)

            dim = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)  # inner product = cosine sim, since normalized
            self.index.add(self.embeddings)
            faiss.write_index(self.index, str(index_path))
            print("Embeddings generated and cached.")

    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        """Returns list of (doc_id, score) sorted by relevance, highest first."""
        query_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.doc_ids[idx], float(score)))
        return results