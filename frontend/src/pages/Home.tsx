import { useState } from "react";
import SearchBar from "../components/SearchBar";
import ResultCard from "../components/ResultCard";
import { searchPapers } from "../services/api";
import type { SearchResult } from "../services/api";

export default function Home() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastMethod, setLastMethod] = useState("");

  const handleSearch = async (query: string, method: string) => {
    setLoading(true);
    setError("");
    try {
      const data = await searchPapers(query, method, 10);
      setResults(data.results);
      setLastMethod(method);
    } catch (err) {
      setError("Search failed. Is the backend running on port 8000?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <h1 className="text-3xl font-bold text-center mb-2">
        Scientific Evidence Retrieval
      </h1>
      <p className="text-center text-gray-500 mb-8">
        Traditional vs. AI-based Information Retrieval on SciFact
      </p>

      <SearchBar onSearch={handleSearch} loading={loading} />

      {error && (
        <p className="text-center text-red-400 mt-4">{error}</p>
      )}

      {results.length > 0 && (
        <div className="mt-10">
          <p className="text-center text-gray-500 mb-4">
            Method: <span className="text-gray-300">{lastMethod}</span> — {results.length} results
          </p>
          {results.map((r, i) => (
            <ResultCard key={r.doc_id} result={r} rank={i + 1} />
          ))}
        </div>
      )}
    </div>
  );
}