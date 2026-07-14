"""
text_preprocessor.py

Preprocessing pipeline used by TF-IDF and BM25 (traditional retrievers).
Steps: lowercase -> tokenize -> remove stopwords/punctuation -> lemmatize.

Note: the AI retrievers (Sentence Transformer, Cross-Encoder) do NOT use
this — they take raw text directly, since those models are trained on
natural, unprocessed sentences.
"""

import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

_stop_words = set(stopwords.words("english"))
_lemmatizer = WordNetLemmatizer()
_punct_table = str.maketrans("", "", string.punctuation)


def preprocess(text: str) -> list[str]:
    """
    Run the full traditional-IR preprocessing pipeline on a string.
    Returns a list of clean lemmatized tokens.
    """
    text = text.lower()
    text = text.translate(_punct_table)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in _stop_words]
    tokens = [_lemmatizer.lemmatize(t) for t in tokens]
    return tokens


def preprocess_to_string(text: str) -> str:
    """
    Same as preprocess(), but returns a single space-joined string.
    Useful for scikit-learn's TfidfVectorizer, which expects strings.
    """
    return " ".join(preprocess(text))