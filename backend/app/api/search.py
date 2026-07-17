"""
search.py

API routes for search functionality.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.search_service import search_service, VALID_METHODS

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    method: str = "hybrid"
    top_k: int = 10


@router.post("/search")
def search(request: SearchRequest):
    if request.method not in VALID_METHODS:
        raise HTTPException(status_code=400, detail=f"method must be one of {VALID_METHODS}")
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query cannot be empty")

    results = search_service.search(request.query, request.method, request.top_k)
    return {"query": request.query, "method": request.method, "results": results}


@router.get("/methods")
def get_methods():
    return {"available_methods": list(VALID_METHODS)}