"""
main.py

FastAPI entrypoint. Run from backend/:
    uvicorn main:app --reload

NOTE: first startup will be slow (loading models, building retrievers).
Subsequent requests are fast.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.search import router as search_router

app = FastAPI(title="Semantic Scientific Evidence Retrieval API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this before deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}