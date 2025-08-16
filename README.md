# AI Wallet Coach – POC (React + Flask)

A hackathon-ready proof-of-concept demonstrating an **AI Wallet Coach** that learns user behavior (via Noetic ID), provides **personalized nudges**, and flags **DeFi risk**. Uses synthetic data for safe demos.

## 📦 Structure
```
ai-wallet-coach-poc/
  backend/        # Flask API (synthetic profile, transactions, insights)
  frontend/       # React + Vite + TS UI
```

## 🚀 Quick Start

### 1) Backend (Flask)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# API at http://localhost:5057/api
```

### 2) Frontend (React + Vite + TS)
```bash
cd ../frontend
npm create vite@latest . -- --template react-ts
npm i
npm i axios
# Replace generated src/ with the provided files in ./frontend/src
npm run dev
# App at http://localhost:5173
```

> If Vite runs on a different port, update `src/services/api.ts` baseURL.

## 🧠 Demo Flow
1. Open the app → header shows **Noetic ID** from backend.
2. **Insights** cards show: Persona, Spend pattern, Risk alerts.
3. **AI Coach** panel shows **nudges** with CTA buttons (mock actions).
4. **Safer Yield Alternatives** section recommends audited pools.
5. **Transactions** table shows weekend spikes & DeFi stakes.

## 🔧 Endpoints
- `GET /api/profile` → { noetic_id, persona, risk_profile }
- `GET /api/transactions` → list of transactions
- `GET /api/insights` → persona + spend stats + risk alerts + nudges
- `POST /api/nudge/accept` → mock accept action
- `GET /api/yield/alternatives` → suggested safer pools

## 🧪 Stretch
- Add `/api/simulate/weekend` to inject a new spend and refresh insights.
- Plug in real wallet read-only sources later (Coinbase / Etherscan) with a **demo mode** toggle.
- Swap rules for a tiny heuristic/classifier if time allows.

## ⚠️ Disclaimer
This POC is **education/demo** only; it does not provide financial advice.


---

## 🤖 LLM (LangChain) Nudges (Optional but Recommended)
Enable **AI-generated coaching** via LangChain + OpenAI.

### 1) Install deps (already in requirements.txt)
- `langchain`, `langchain-openai`, `openai`

### 2) Set your API key
```bash
export OPENAI_API_KEY=sk-...    # macOS/Linux
# or on Windows (PowerShell)
# $Env:OPENAI_API_KEY="sk-..."
```

### 3) Run backend and call the endpoint
```
GET /api/nudge/llm
# → { persona, message, cta }
```

### 4) (Frontend) Add a button to fetch LLM nudge
Example service:
```ts
export const fetchLLMNudge = () => api.get("/nudge/llm").then(r => r.data);
```
Use it in the Coach component to display a dynamic, human-like nudge.
