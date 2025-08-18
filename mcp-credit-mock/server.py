from fastapi import FastAPI

app = FastAPI(title="Mock MCP Credit Card Server")

# Fake current expense endpoint
@app.get("/mcp/credit/expenses/current")
def get_current_expense():
    return {
        "month": "2025-08",
        "currency": "USD",
        "total_spent": 2345.67,
        "categories": {
            "groceries": 520.45,
            "travel": 830.00,
            "subscriptions": 95.22,
            "misc": 900.00
        }
    }

# Fake recent transactions endpoint
@app.get("/mcp/credit/transactions/recent")
def get_recent_transactions():
    return [
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
        {"ts": "2025-08-03T00:35:00Z", "type": "card", "merchant": "Bars & Pubs", "amount": -63.40, "category": "Nightlife"},        
    ]