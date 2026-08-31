import type { SearchResult } from "../services/api";

interface ComparisonSummaryProps {
  resultsA: SearchResult[];
  resultsB: SearchResult[];
  labelA: string;
  labelB: string;
}

export default function ComparisonSummary({
  resultsA,
  resultsB,
  labelA,
  labelB,
}: ComparisonSummaryProps) {
  const idsA = resultsA.map((r) => r.doc_id);
  const idsB = resultsB.map((r) => r.doc_id);

  const shared = idsA.filter((id) => idsB.includes(id));
  const onlyA = idsA.filter((id) => !idsB.includes(id));
  const onlyB = idsB.filter((id) => !idsA.includes(id));

  const union = new Set([...idsA, ...idsB]);
  const overlapPercent = union.size === 0 ? 0 : Math.round((shared.length / union.size) * 100);

  const titleFor = (id: number, list: SearchResult[]) =>
    list.find((r) => r.doc_id === id)?.title ?? "";

  return (
    <div className="w-full max-w-4xl mx-auto mb-8 p-5 rounded-lg bg-[#161920] border border-gray-700">
      <h3 className="text-gray-200 font-semibold mb-3">Comparison Summary</h3>

      <div className="flex flex-wrap gap-6 mb-4">
        <div>
          <span className="text-2xl font-bold text-blue-400">{overlapPercent}%</span>
          <span className="text-sm text-gray-500 ml-2">agreement (Jaccard overlap)</span>
        </div>
        <div>
          <span className="text-2xl font-bold text-gray-300">{shared.length}</span>
          <span className="text-sm text-gray-500 ml-2">papers found by both</span>
        </div>
      </div>

      {onlyB.length > 0 && (
        <div className="mb-3">
          <p className="text-sm text-green-400 font-medium mb-1">
            Found only by {labelB} ({onlyB.length}):
          </p>
          <ul className="text-sm text-gray-400 list-disc list-inside">
            {onlyB.map((id) => (
              <li key={id}>{titleFor(id, resultsB)}</li>
            ))}
          </ul>
        </div>
      )}

      {onlyA.length > 0 && (
        <div>
          <p className="text-sm text-yellow-400 font-medium mb-1">
            Found only by {labelA} ({onlyA.length}):
          </p>
          <ul className="text-sm text-gray-400 list-disc list-inside">
            {onlyA.map((id) => (
              <li key={id}>{titleFor(id, resultsA)}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}