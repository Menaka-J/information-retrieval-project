import type { SearchResult } from "../services/api";

interface ResultCardProps {
  result: SearchResult;
  rank: number;
  isShared?: boolean;
}

export default function ResultCard({ result, rank, isShared }: ResultCardProps) {
  const relevancePercent = Math.round(result.normalized_score * 100);

  return (
    <div
      className={`w-full max-w-2xl mx-auto p-4 rounded-lg border mb-3 ${
        isShared ? "bg-[#1a2420] border-green-700" : "bg-[#1a1d24] border-gray-700"
      }`}
    >
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">#{rank}</span>
          {isShared && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-green-800 text-green-300">
              Also found by other method
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-blue-500" style={{ width: `${relevancePercent}%` }} />
          </div>
          <span className="text-xs text-blue-400 font-mono w-10 text-right">
            {relevancePercent}%
          </span>
        </div>
      </div>
      <h3 className="text-lg font-semibold text-gray-100 mb-2">{result.title}</h3>
      <p className="text-sm text-gray-400 line-clamp-3">{result.abstract}</p>
      <div className="mt-2 text-xs text-gray-600">doc_id: {result.doc_id}</div>
    </div>
  );
}