import React from "react";

type Txn = { ts: string; type: string; merchant: string; amount: number; category: string };

export default function TransactionsTable({ txns }: { txns: Txn[] }) {
  return (
    <div className="rounded-2xl shadow p-4">
      <h3 className="text-xl font-bold mb-2">Recent Transactions</h3>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left border-b">
            <th className="py-2">Date</th>
            <th>Type</th>
            <th>Merchant / Protocol</th>
            <th>Category</th>
            <th className="text-right">Amount</th>
          </tr>
        </thead>
        <tbody>
          {txns.map((t, i) => (
            <tr key={i} className="border-b">
              <td className="py-2">{new Date(t.ts).toLocaleString()}</td>
              <td>{t.type}</td>
              <td>{t.merchant}</td>
              <td>{t.category}</td>
              <td className="text-right">{t.amount.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
