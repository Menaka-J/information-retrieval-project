"""
tfidf_retriever.py

Traditional IR: TF-IDF vectorization + Cosine Similarity.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.preprocessing.text_preprocessor import preprocess_to_string


class TfidfRetriever:
    def __init__(self, corpus: dict):
        """
        corpus: dict[doc_id -> Document] from dataset_loader.load_corpus()
        """
        self.doc_ids = list(corpus.keys())
        raw_texts = [corpus[doc_id].full_text for doc_id in self.doc_ids]
        clean_texts = [preprocess_to_string(t) for t in raw_texts]

        self.vectorizer = TfidfVectorizer()
        self.doc_matrix = self.vectorizer.fit_transform(clean_texts)

    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        """Returns list of (doc_id, score) sorted by relevance, highest first."""
        clean_query = preprocess_to_string(query)
        query_vec = self.vectorizer.transform([clean_query])
        scores = cosine_similarity(query_vec, self.doc_matrix).flatten()

        ranked_idx = scores.argsort()[::-1][:top_k]
        return [(self.doc_ids[i], float(scores[i])) for i in ranked_idx]