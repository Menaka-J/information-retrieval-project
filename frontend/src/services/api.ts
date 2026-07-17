import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

export interface SearchResult {
  doc_id: number;
  title: string;
  abstract: string;
  score: number;
  method: string;
}

export interface SearchResponse {
  query: string;
  method: string;
  results: SearchResult[];
}

export async function searchPapers(
  query: string,
  method: string,
  top_k: number = 10
): Promise<SearchResponse> {
  const response = await axios.post(`${API_BASE}/search`, {
    query,
    method,
    top_k,
  });
  return response.data;
}