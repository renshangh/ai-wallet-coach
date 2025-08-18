# Steps to Build a Minimal MCP Server with FastAPI
1. Create a project folder
mkdir mcp-credit-mock
cd mcp-credit-mock

2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Create the server file

Name it server.py (this is a common convention with FastAPI; you can pick another name, but server.py keeps it clean).

📄 server.py

5. Run the server
```bash
uvicorn server:app --reload --port 8000
```

* server = the file name (server.py)
* app = the FastAPI app object inside that file
* --reload = hot reload when you edit
* --port 8000 = runs on http://localhost:8000

6. Test it in your browser or curl

Current expense:

http://localhost:8000/mcp/credit/expenses/current


Recent transactions:

http://localhost:8000/mcp/credit/transactions/recent


✅ You should see JSON responses with mock credit card data.

7. Hook into LangChain

Later, in LangChain you’d wrap these endpoints in a tool, like:
```python
import requests
from langchain.tools import tool

@tool
def get_current_expense_tool() -> dict:
    """Fetch current month's credit card expense from MCP server."""
    r = requests.get("http://localhost:8000/mcp/credit/expenses/current")
    return r.json()
```

Now your LangChain agent can call this just like it would call a real MCP connector.

📌 Summary

Use server.py as your FastAPI file.

Run with uvicorn server:app.

Mock endpoints under /mcp/... mimic your future credit card provider.

Integrate with LangChain as if it’s a real data source.