import { useState } from "react";
import Home from "./pages/Home";
import Compare from "./pages/Compare";

function App() {
  const [tab, setTab] = useState<"search" | "compare">("compare");

  return (
    <div>
      <div className="flex justify-center gap-2 pt-6">
        <button
          onClick={() => setTab("search")}
          className={`px-4 py-2 rounded-lg font-medium ${
            tab === "search" ? "bg-blue-600 text-white" : "bg-[#1a1d24] text-gray-400"
          }`}
        >
          Single Search
        </button>
        <button
          onClick={() => setTab("compare")}
          className={`px-4 py-2 rounded-lg font-medium ${
            tab === "compare" ? "bg-blue-600 text-white" : "bg-[#1a1d24] text-gray-400"
          }`}
        >
          Compare Methods
        </button>
      </div>
      {tab === "search" ? <Home /> : <Compare />}
    </div>
  );
}

export default App;