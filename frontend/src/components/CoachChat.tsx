import React, { useState } from "react";
import { acceptNudge, fetchLLMNudge } from "../services/api";

type Nudge = { type: string; message: string; cta?: { label: string; action: string } };

export default function CoachChat({ nudges }: { nudges: Nudge[] }) {
  const [log, setLog] = useState<string[]>([]);
  const onAccept = async (n: Nudge) => {
    await acceptNudge(n.type);
    setLog(l => [`✅ Accepted: ${n.type}`, ...l]);
  };
  return (
    <div className="rounded-2xl shadow p-4">
      <h3 className="text-xl font-bold mb-2">AI Coach</h3>
      <button
        onClick={async () => {
          const res = await fetchLLMNudge();
          setLog(l => [`🤖 AI Coach: ${res.message}`, ...l]);
        }}
        className="mb-3 px-3 py-2 rounded-xl border hover:bg-gray-50"
      >
        Ask AI Coach (LLM)
      </button>
    
      <div className="space-y-3">
        {nudges.map((n, i) => (
          <div key={i} className="border rounded-lg p-3">
            <p>{n.message}</p>
            {n.cta && (
              <button
                onClick={() => onAccept(n)}
                className="mt-2 px-3 py-2 rounded-xl border hover:bg-gray-50"
              >
                {n.cta.label}
              </button>
            )}
          </div>
        ))}
      </div>
      {log.length > 0 && (
        <div className="mt-4 text-sm text-green-700">
          {log.map((l, i) => <div key={i}>{l}</div>)}
        </div>
      )}
    </div>
  );
}
