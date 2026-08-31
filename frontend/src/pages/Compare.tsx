import { useState } from "react";
import CompareBar from "../components/CompareBar";
import ResultCard from "../components/ResultCard";
import ComparisonSummary from "../components/ComparisonSummary";
import { searchPapers } from "../services/api";
import type { SearchResult } from "../services/api";

const METHOD_LABELS: Record<string, string> = {
  tfidf: "TF-IDF (Traditional)",
  bm25: "BM25 (Traditional)",
  semantic: "Semantic (AI)",
  hybrid: "Hybrid (AI, Proposed)",
};

export default function Compare() {
  const [resultsA, setResultsA] = useState<SearchResult[]>([]);
  const [resultsB, setResultsB] = useState<SearchResult[]>([]);
  const [methodA, setMethodA] = useState("");
  const [methodB, setMethodB] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (query: string, mA: string, mB: string) => {
    setLoading(true);
    setError("");
    try {
      const [dataA, dataB] = await Promise.all([
        searchPapers(query, mA, 5),
        searchPapers(query, mB, 5),
      ]);
      setResultsA(dataA.results);
      setResultsB(dataB.results);
      setMethodA(mA);
      setMethodB(mB);
    } catch (err) {
      setError("Search failed. Is the backend running on port 8000?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const idsA = resultsA.map((r) => r.doc_id);
  const idsB = resultsB.map((r) => r.doc_id);

  return (
    <div className="min-h-screen py-12 px-4">
      <h1 className="text-3xl font-bold text-center mb-2">
        Traditional vs. AI Retrieval — Side by Side
      </h1>
      <p className="text-center text-gray-500 mb-8">
        Same claim, two methods, compared directly
      </p>

      <CompareBar onSearch={handleSearch} loading={loading} />

      {error && <p className="text-center text-red-400 mt-4">{error}</p>}

      {resultsA.length > 0 && (
        <>
          <div className="mt-8">
            <ComparisonSummary
              resultsA={resultsA}
              resultsB={resultsB}
              labelA={METHOD_LABELS[methodA]}
              labelB={METHOD_LABELS[methodB]}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl mx-auto">
            <div>
              <h2 className="text-center text-lg font-semibold text-gray-300 mb-4">
                {METHOD_LABELS[methodA]}
              </h2>
              {resultsA.map((r, i) => (
                <ResultCard
                  key={r.doc_id}
                  result={r}
                  rank={i + 1}
                  isShared={idsB.includes(r.doc_id)}
                />
              ))}
            </div>
            <div>
              <h2 className="text-center text-lg font-semibold text-gray-300 mb-4">
                {METHOD_LABELS[methodB]}
              </h2>
              {resultsB.map((r, i) => (
                <ResultCard
                  key={r.doc_id}
                  result={r}
                  rank={i + 1}
                  isShared={idsA.includes(r.doc_id)}
                />
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}