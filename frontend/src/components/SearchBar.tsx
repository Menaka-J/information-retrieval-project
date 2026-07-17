import { useState } from "react";

interface SearchBarProps {
  onSearch: (query: string, method: string) => void;
  loading: boolean;
}

const METHODS = [
  { value: "tfidf", label: "TF-IDF (Traditional)" },
  { value: "bm25", label: "BM25 (Traditional)" },
  { value: "semantic", label: "Semantic (AI)" },
  { value: "hybrid", label: "Hybrid (AI, Proposed)" },
];

export default function SearchBar({ onSearch, loading }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [method, setMethod] = useState("hybrid");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query, method);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto flex flex-col gap-3">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter a scientific claim, e.g. Vitamin D improves bone health"
        className="w-full px-4 py-3 rounded-lg bg-[#1a1d24] border border-gray-700 text-gray-100 focus:outline-none focus:border-blue-500"
      />
      <div className="flex items-center gap-3">
        <select
          value={method}
          onChange={(e) => setMethod(e.target.value)}
          className="px-3 py-2 rounded-lg bg-[#1a1d24] border border-gray-700 text-gray-100"
        >
          {METHODS.map((m) => (
            <option key={m.value} value={m.value}>
              {m.label}
            </option>
          ))}
        </select>
        <button
          type="submit"
          disabled={loading}
          className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>
    </form>
  );
}