import React from "react";

type Props = {
  persona: string;
  spend: { weekend_spend: number; weekday_spend: number };
  riskAlerts: { title: string; detail: string; severity: string; suggestion: string }[];
};

export default function InsightsCards({ persona, spend, riskAlerts }: Props) {
  return (
    <div className="grid md:grid-cols-3 gap-4">
      <div className="p-4 rounded-2xl shadow">
        <h3 className="text-xl font-bold">Persona</h3>
        <p className="mt-2">{persona}</p>
      </div>
      <div className="p-4 rounded-2xl shadow">
        <h3 className="text-xl font-bold">Spend Pattern</h3>
        <p className="mt-2">Weekend: ${spend.weekend_spend.toFixed(2)}</p>
        <p>Weekday: ${spend.weekday_spend.toFixed(2)}</p>
      </div>
      <div className="p-4 rounded-2xl shadow">
        <h3 className="text-xl font-bold">Risk Alerts</h3>
        {riskAlerts.length === 0 && <p className="mt-2">No active alerts.</p>}
        {riskAlerts.map((a, i) => (
          <div key={i} className="mt-2 p-3 rounded-lg border">
            <p className="font-semibold">{a.title}</p>
            <p className="text-sm">{a.detail}</p>
            <p className="text-sm mt-1 italic">{a.suggestion}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
