"""
dataset_loader.py

Loads the SciFact dataset (corpus + claims) and exposes clean Python
structures for the rest of the pipeline to use.

Design decision (documented, see project notes):
    A document is treated as "relevant" to a claim if its doc_id appears
    in that claim's `cited_doc_ids` list — regardless of whether the
    `evidence` field is empty (NEI / not enough info) or populated
    (SUPPORT / CONTRADICT). This is correct for evaluating RETRIEVAL
    quality (did we find the right paper?), as opposed to VERIFICATION
    quality (did we correctly judge support/contradict?), which this
    project does not attempt.
"""

import json
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Document:
    doc_id: int
    title: str
    abstract: list[str]

    @property
    def full_text(self) -> str:
        """Title + abstract sentences combined into one searchable string."""
        return self.title + " " + " ".join(self.abstract)


@dataclass
class Claim:
    id: int
    claim: str
    cited_doc_ids: list[int] = field(default_factory=list)
    evidence: dict = field(default_factory=dict)

    @property
    def relevant_doc_ids(self) -> set[int]:
        """Gold relevance set for IR evaluation. See module docstring."""
        return set(self.cited_doc_ids)


def load_corpus(path: str | Path) -> dict[int, Document]:
    """Load corpus.jsonl into a dict keyed by doc_id for O(1) lookup."""
    path = Path(path)
    corpus: dict[int, Document] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            doc = Document(
                doc_id=obj["doc_id"],
                title=obj.get("title", ""),
                abstract=obj.get("abstract", []),
            )
            corpus[doc.doc_id] = doc
    return corpus


def load_claims(path: str | Path) -> list[Claim]:
    """Load a claims_*.jsonl file (train or dev format, with evidence)."""
    path = Path(path)
    claims: list[Claim] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            claim = Claim(
                id=obj["id"],
                claim=obj["claim"],
                cited_doc_ids=obj.get("cited_doc_ids", []),
                evidence=obj.get("evidence", {}),
            )
            claims.append(claim)
    return claims


def load_test_claims(path: str | Path) -> list[dict]:
    """
    Load claims_test.jsonl. NOTE: this file has no cited_doc_ids or
    evidence (it's SciFact's blind test set) so it cannot be used for
    evaluation — only for demo-ing search on unseen claims.
    """
    path = Path(path)
    claims: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            claims.append(json.loads(line))
    return claims