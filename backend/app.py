from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dateutil.parser import parse as dtparse

app = Flask(__name__)
CORS(app)

# ---- Synthetic data (replace with a DB later) ----
USER = {
    "noetic_id": "noetic_12345",
    "name": "Alex",
    "risk_profile": "medium",
    "persona": None  # inferred below
}

# make a mcp call to get current expenses from the mock server 
import requests
# Define the URL of the REST API endpoint
url = 'http://localhost:8000/mcp/credit/transactions/recent'

# Make a GET request to the API
response = requests.get(url)

TXNS=[]

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    TXNS = response.json()
    #print("from json\n",TXNS)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")


"""TXNS = [
    # fiat-like spend
    {"ts": "2025-07-04T19:22:00Z", "type": "card", "merchant": "DoorDash", "amount": -38.20, "category": "Food"},
    {"ts": "2025-07-05T22:14:00Z", "type": "card", "merchant": "Target", "amount": -92.51, "category": "Shopping"},
    {"ts": "2025-07-06T01:02:00Z", "type": "card", "merchant": "Uber", "amount": -27.80, "category": "Transport"},
    # weekday smalls
    {"ts": "2025-07-08T13:05:00Z", "type": "card", "merchant": "Starbucks", "amount": -6.55, "category": "Food"},
    {"ts": "2025-07-09T18:30:00Z", "type": "card", "merchant": "Chipotle", "amount": -14.25, "category": "Food"},
    # income
    {"ts": "2025-07-15T09:00:00Z", "type": "ach", "merchant": "Employer Inc", "amount": 3200.00, "category": "Income"},
    # crypto / defi
    {"ts": "2025-07-18T14:11:00Z", "type": "defi", "merchant": "PoolX", "amount": -500.00, "category": "DeFi:Stake"},
    {"ts": "2025-07-25T09:41:00Z", "type": "defi", "merchant": "PoolX", "amount": 12.00, "category": "DeFi:Rewards"},
    {"ts": "2025-07-26T20:10:00Z", "type": "defi", "merchant": "AnonYield9000", "amount": -400.00, "category": "DeFi:Stake"},
    {"ts": "2025-07-27T10:20:00Z", "type": "defi", "merchant": "AnonYield9000", "amount": 4.00, "category": "DeFi:Rewards"},
    # weekend spend spike
    {"ts": "2025-08-02T23:50:00Z", "type": "card", "merchant": "Best Buy", "amount": -289.99, "category": "Electronics"},
    {"ts": "2025-08-03T00:35:00Z", "type": "card", "merchant": "Bars & Pubs", "amount": -63.40, "category": "Nightlife"} 
] """

SAFE_ALT_POOLS = [
    {"name": "Lido stETH", "apy": 4.1, "audited": True, "chain": "Ethereum"},
    {"name": "Aave v3 USDC", "apy": 3.2, "audited": True, "chain": "Multiple"},
]

HIGH_RISK_PROTOCOLS = {"AnonYield9000": {"reason": "Unaudited contract, anon team, abnormal liquidity swings"}}

def is_weekend(dt: datetime) -> bool:
    return dt.weekday() >= 5

def spend_stats():
    weekend = sum(-t["amount"] for t in TXNS if t["amount"] < 0 and is_weekend(dtparse(t["ts"])))
    weekday = sum(-t["amount"] for t in TXNS if t["amount"] < 0 and not is_weekend(dtparse(t["ts"])))
    return {"weekend_spend": weekend, "weekday_spend": weekday}

def persona_infer():
    stats = spend_stats()
    weekend_bias = stats["weekend_spend"] > (stats["weekday_spend"] * 0.6)
    defi_stakes = [t for t in TXNS if t["type"] == "defi" and "Stake" in t["category"]]
    risky = any(t["merchant"] in HIGH_RISK_PROTOCOLS for t in TXNS)
    if len(defi_stakes) >= 2 and risky:
        return "High-Risk Yield Farmer"
    if weekend_bias and stats["weekend_spend"] > 200:
        return "Weekend Impulsive Spender"
    return "Balanced"

def compute_risk_alerts():
    alerts = []
    for t in TXNS:
        if t["type"] == "defi" and t["merchant"] in HIGH_RISK_PROTOCOLS and t["amount"] < 0:
            alerts.append({
                "ts": t["ts"],
                "severity": "high",
                "title": f"Risky protocol: {t['merchant']}",
                "detail": HIGH_RISK_PROTOCOLS[t["merchant"]]["reason"],
                "suggestion": f"Consider moving funds to {SAFE_ALT_POOLS[0]['name']} (~{SAFE_ALT_POOLS[0]['apy']}% APY, audited)."
            })
    return alerts

def coaching_nudges():
    s = spend_stats()
    nudges = []
    if s["weekend_spend"] > s["weekday_spend"] * 0.6:
        delta = round(s["weekend_spend"] - s["weekday_spend"] * 0.6, 2)
        nudges.append({
            "type": "spend",
            "message": f"You spend significantly more on weekends. Try pre-allocating $50–$100 to a 'Weekend Pot' (overshoot by ${delta}).",
            "cta": {"label": "Create Weekend Pot ($100)", "action": "create_pot", "amount": 100}
        })
    if any(t["type"] == "defi" and t["merchant"] in HIGH_RISK_PROTOCOLS for t in TXNS):
        nudges.append({
            "type": "defi",
            "message": f"Detected stakes in unaudited pools. Shift 25% to safer audited alternatives like {SAFE_ALT_POOLS[0]['name']} (~{SAFE_ALT_POOLS[0]['apy']}% APY).",
            "cta": {"label": f"Rebalance 25% to {SAFE_ALT_POOLS[0]['name']}", "action": "rebalance", "target": SAFE_ALT_POOLS[0]["name"], "portion": 0.25}
        })
    return nudges

@app.get("/api/profile")
def profile():
    USER["persona"] = persona_infer()
    return jsonify(USER)

@app.get("/api/transactions")
def transactions():
    return jsonify({"transactions": TXNS})

@app.get("/api/insights")
def insights():
    stats = spend_stats()
    alerts = compute_risk_alerts()
    persona = persona_infer()
    return jsonify({
        "persona": persona,
        "spend": stats,
        "risk_alerts": alerts,
        "nudges": coaching_nudges()
    })

@app.post("/api/nudge/accept")
def accept_nudge():
    data = request.get_json(force=True)
    ntype = data.get("type")
    event = {"status": "ok", "applied": ntype}
    return jsonify(event)

@app.get("/api/yield/alternatives")
def yield_alts():
    return jsonify({"alternatives": SAFE_ALT_POOLS})

# -------- LangChain LLM (Ollama Qwen2.5) --------
import os
print("Loading Ollama local model for LLM nudges...")
try:
    from langchain_community.llms import Ollama
    from langchain.prompts import ChatPromptTemplate
    llm = Ollama(model="qwen2.5-coder:7b-instruct-q8_0", temperature=0.0)
    print("Using LLM for coaching nudges, llm.model: ", llm.model)

    # Define the prompt template for the LLM nudge
    nudge_prompt = ChatPromptTemplate.from_template(
        "You are an encouraging, concise AI wallet coach.\n"
        "Persona: {persona}\n"
        "Recent transactions (ISO ts, amount, category): {txns}\n"
        "Constraints: 1-2 sentences, friendly, specific, never give financial advice, say 'guidance' not 'advice'.\n"
        "End with a short actionable suggestion."
    )
    def llm_nudge(persona, txns):
        result = (nudge_prompt | llm).invoke({
            "persona": persona,
            "txns": txns[-6:]
        })
        if isinstance(result, str):
            return result.strip()
        elif hasattr(result, "content"):
            return result.content.strip()
        else:
            return str(result)
except Exception as e:
    def llm_nudge(persona, txns):
        return "Coach temporarily unavailable; using heuristic nudges. Try setting aside $50 for the weekend and review DeFi allocations."


@app.get("/api/nudge/llm")
def nudge_llm():
    print("Generating LLM nudge...")
    persona = persona_infer()
    # Summarize recent transactions for the prompt
    recent = [{
        "ts": t["ts"], "amount": t["amount"], "category": t["category"]
    } for t in TXNS[-10:]]
    message = llm_nudge(persona, recent)
    # Include a suggested CTA derived from persona
    if "Yield" in persona or "Farmer" in persona:
        cta = {"label": "Rebalance 25% to audited pool", "action": "rebalance", "portion": 0.25}
    else:
        cta = {"label": "Create Weekend Pot ($50)", "action": "create_pot", "amount": 50}
    return jsonify({"persona": persona, "message": message, "cta": cta})

# New API endpoint using Ollama model
@app.get("/api/noetllm")
def noet_llm():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        result = llm(prompt)
        return jsonify({"result": result.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5057, debug=True)
