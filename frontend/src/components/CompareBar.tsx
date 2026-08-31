import { useState } from "react";

interface CompareBarProps {
  onSearch: (query: string, methodA: string, methodB: string) => void;
  loading: boolean;
}

const METHODS = [
  { value: "tfidf", label: "TF-IDF (Traditional)" },
  { value: "bm25", label: "BM25 (Traditional)" },
  { value: "semantic", label: "Semantic (AI)" },
  { value: "hybrid", label: "Hybrid (AI, Proposed)" },
];

export default function CompareBar({ onSearch, loading }: CompareBarProps) {
  const [query, setQuery] = useState("");
  const [methodA, setMethodA] = useState("bm25");
  const [methodB, setMethodB] = useState("hybrid");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query, methodA, methodB);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-4xl mx-auto flex flex-col gap-3">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter a scientific claim, e.g. Aspirin encourages the production of PGE2"
        className="w-full px-4 py-3 rounded-lg bg-[#1a1d24] border border-gray-700 text-gray-100 focus:outline-none focus:border-blue-500"
      />
      <div className="flex items-center gap-3 justify-center flex-wrap">
        <select
          value={methodA}
          onChange={(e) => setMethodA(e.target.value)}
          className="px-3 py-2 rounded-lg bg-[#1a1d24] border border-gray-700 text-gray-100"
        >
          {METHODS.map((m) => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
        <span className="text-gray-500">vs</span>
        <select
          value={methodB}
          onChange={(e) => setMethodB(e.target.value)}
          className="px-3 py-2 rounded-lg bg-[#1a1d24] border border-gray-700 text-gray-100"
        >
          {METHODS.map((m) => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
        <button
          type="submit"
          disabled={loading}
          className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium"
        >
          {loading ? "Searching..." : "Compare"}
        </button>
      </div>
    </form>
  );
}