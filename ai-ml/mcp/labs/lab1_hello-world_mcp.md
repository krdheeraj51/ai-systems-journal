# **MCP-1 — Hello World MCP Server & Client**

## Objective

Learn the **minimum viable setup** for an MCP server and client:

* Understand what the MCP protocol is and why it exists.
* Create a **simple MCP server** that exposes a “Hello World” method.
* Write a **client** that connects to the server, calls the method, and prints the result.

---

## Step 0 — What is MCP?

**Model Context Protocol (MCP)** is a standardized way for AI models (and AI-powered apps) to talk to external **tools, databases, APIs, or environments** in a structured, secure way.
Think of it as a *"USB protocol for AI"* — the LLM is the device, and MCP is the universal port.

Key points:

* **Server** → Exposes functions/resources to the AI (like a calculator, DB, API).
* **Client** → Connects to server, sends requests, receives structured responses.
* **Transport** → Can be WebSocket, HTTP, or others.
* **Format** → JSON-RPC-like messages with schema validation.

---

## Step 1 — Install MCP Python SDK

```bash
pip install modelcontextprotocol
```

---

## Step 2 — Create a Basic MCP Server

File: `mcp_server.py`

```python
from modelcontextprotocol import Server
from modelcontextprotocol.types import Request, Response

# Create MCP server instance
server = Server(name="HelloWorldServer")

# Define a simple "hello" method
@server.method("hello")
async def hello_method(request: Request) -> Response:
    # You can read params from request.params if provided
    name = request.params.get("name", "World") if request.params else "World"
    return Response(result={"message": f"Hello, {name}!"})

if __name__ == "__main__":
    # Start server (using stdio transport for simplicity)
    server.run_stdio()
```

What’s happening:

* `server.method("hello")` → Registers a callable method for clients.
* `server.run_stdio()` → Starts listening for JSON messages over **stdin/stdout** (easy for local dev).

---

## Step 3 — Create a Basic MCP Client

File: `mcp_client.py`

```python
import asyncio
from modelcontextprotocol import Client

async def main():
    # Create a client (stdio transport to talk to server process)
    client = Client(name="TestClient")

    # Start the server process automatically
    await client.connect_to_subprocess(["python", "mcp_server.py"])

    # Send a request to call the 'hello' method
    resp = await client.request("hello", params={"name": "Azure AI"})
    print("Server responded:", resp.result)

    # Close connection
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Step 4 — Run the Lab

1. Open **two terminals**.

**Terminal 1** — Run server directly:

```bash
python mcp_server.py
```

**Terminal 2** — Run client:

```bash
python mcp_client.py
```

Or run them together via client’s `connect_to_subprocess` (as written in code above), so you only run the client.

---

## Step 5 — Expected Output

```
Server responded: {'message': 'Hello, Azure AI!'}
```

---

## Step 6 — Understanding the Flow

1. **Client → Server:** Sends JSON-RPC request with method `"hello"` and parameters `{name: "Azure AI"}`.
2. **Server:** Executes `hello_method`, returns `{"message": "Hello, Azure AI!"}`.
3. **Client:** Prints the server's response.

---

## Step 7 — What You Learned

* How to set up an **MCP server** with a single method.
* How to connect an **MCP client** to it via stdio transport.
* How JSON-based requests and responses flow between them.

