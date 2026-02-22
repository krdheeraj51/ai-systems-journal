# **MCP-2 — Multi-Tool MCP Server & Method Discovery**

## Objective

* Extend the MCP server to host **multiple tools** (methods).
* Learn how the client can **list all available methods** dynamically.
* Call different methods and handle parameters.

---

## Step 0 — Prerequisites

We’ll build on **MCP-1**, so make sure you’ve run that first.
Still need:

```bash
pip install modelcontextprotocol
```

---

## Step 1 — Update the MCP Server

File: `mcp_server_multi.py`

```python
from modelcontextprotocol import Server
from modelcontextprotocol.types import Request, Response
import datetime
import math

server = Server(name="MultiToolServer")

# --- Method 1: Hello ---
@server.method("hello")
async def hello_method(request: Request) -> Response:
    name = request.params.get("name", "World") if request.params else "World"
    return Response(result={"message": f"Hello, {name}!"})

# --- Method 2: Get current time ---
@server.method("get_time")
async def get_time_method(request: Request) -> Response:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return Response(result={"utc_time": now})

# --- Method 3: Calculate square root ---
@server.method("sqrt")
async def sqrt_method(request: Request) -> Response:
    try:
        number = float(request.params.get("number"))
        return Response(result={"sqrt": math.sqrt(number)})
    except Exception as e:
        return Response(error={"message": str(e)})

if __name__ == "__main__":
    server.run_stdio()
```

---

## Step 2 — Update the Client to Discover Methods

File: `mcp_client_multi.py`

```python
import asyncio
from modelcontextprotocol import Client

async def main():
    client = Client(name="MultiToolClient")

    # Start server process
    await client.connect_to_subprocess(["python", "mcp_server_multi.py"])

    # --- List all available methods ---
    methods = await client.list_methods()
    print("Available server methods:")
    for m in methods:
        print(f"- {m['name']}: {m.get('description', 'No description')}")

    # --- Call hello ---
    resp1 = await client.request("hello", params={"name": "Azure AI"})
    print("\nHello response:", resp1.result)

    # --- Call get_time ---
    resp2 = await client.request("get_time")
    print("Time response:", resp2.result)

    # --- Call sqrt ---
    resp3 = await client.request("sqrt", params={"number": 16})
    print("Sqrt response:", resp3.result)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Step 3 — Run It

Just run:

```bash
python mcp_client_multi.py
```

The client will automatically start the server and interact with it.

---

## Step 4 — Expected Output

```
Available server methods:
- hello: No description
- get_time: No description
- sqrt: No description

Hello response: {'message': 'Hello, Azure AI!'}
Time response: {'utc_time': '2025-08-14T12:34:56.789Z'}
Sqrt response: {'sqrt': 4.0}
```

---

## Step 5 — What You Learned

* An MCP server can expose **multiple independent tools**.
* Clients can **discover available methods dynamically** without hardcoding them.
* You can pass structured parameters and handle errors in methods.


