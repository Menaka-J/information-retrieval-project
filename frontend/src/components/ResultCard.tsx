import type { SearchResult } from "../services/api";

interface ResultCardProps {
  result: SearchResult;
  rank: number;
}

export default function ResultCard({ result, rank }: ResultCardProps) {
  return (
    <div className="w-full max-w-2xl mx-auto p-4 rounded-lg bg-[#1a1d24] border border-gray-700 mb-3">
      <div className="flex justify-between items-start mb-2">
        <span className="text-sm text-gray-500">#{rank}</span>
        <span className="text-sm text-blue-400 font-mono">score: {result.score}</span>
      </div>
      <h3 className="text-lg font-semibold text-gray-100 mb-2">{result.title}</h3>
      <p className="text-sm text-gray-400 line-clamp-3">{result.abstract}</p>
      <div className="mt-2 text-xs text-gray-600">doc_id: {result.doc_id}</div>
    </div>
  );
}