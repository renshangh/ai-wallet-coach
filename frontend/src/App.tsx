import React, { useEffect, useState } from "react";
import { getProfile, getTransactions, getInsights, getYieldAlts } from "./services/api";
import InsightsCards from "./components/InsightsCards";
import CoachChat from "./components/CoachChat";
import TransactionsTable from "./components/TransactionsTable";

type InsightResponse = {
  persona: string;
  spend: { weekend_spend: number; weekday_spend: number };
  risk_alerts: any[];
  nudges: any[];
};

export default function App() {
  const [profile, setProfile] = useState<any>(null);
  const [tx, setTx] = useState<any[]>([]);
  const [insights, setInsights] = useState<InsightResponse | null>(null);
  const [alts, setAlts] = useState<any[]>([]);

  useEffect(() => {
    getProfile().then(setProfile);
    getTransactions().then(d => setTx(d.transactions));
    getInsights().then(setInsights);
    getYieldAlts().then(d => setAlts(d.alternatives));
  }, []);

  if (!profile || !insights) return <div className="p-6">Loading…</div>;

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">AI Wallet Coach</h1>
        <div className="text-sm">Noetic ID: <span className="font-mono">{profile.noetic_id}</span></div>
      </header>

      <InsightsCards
        persona={insights.persona}
        spend={insights.spend}
        riskAlerts={insights.risk_alerts}
      />

      <div className="grid md:grid-cols-2 gap-6">
        <CoachChat nudges={insights.nudges} />
        <div className="rounded-2xl shadow p-4">
          <h3 className="text-xl font-bold mb-2">Safer Yield Alternatives</h3>
          {alts.map((a, i) => (
            <div key={i} className="border rounded-lg p-3 mb-2">
              <p className="font-semibold">{a.name}</p>
              <p className="text-sm">APY ~ {a.apy}% • Audited: {a.audited ? "Yes" : "No"} • {a.chain}</p>
            </div>
          ))}
        </div>
      </div>

      <TransactionsTable txns={tx} />
    </div>
  );
}
