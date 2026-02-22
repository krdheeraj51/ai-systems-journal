# **MCP-3 — Multi-Step & Streaming Responses**

## Objective

* Learn how to handle **long-running operations** in MCP.
* Stream partial responses from the **server** to the **client**.
* Show how the client processes streamed data in chunks.

---

## Step 0 — Why Streaming?

Sometimes:

* The task is **long-running** (e.g., reading large files, fetching from slow APIs).
* You want to send **partial results** as they are ready instead of waiting until everything is done.
* Streaming keeps the client responsive and improves user experience.

MCP supports this with **yielding events** before sending the final result.

---

## Step 1 — Create the Streaming MCP Server

File: `mcp_server_stream.py`

```python
from modelcontextprotocol import Server
from modelcontextprotocol.types import Request, Response, Event
import asyncio

server = Server(name="StreamingServer")

@server.method("count_to_n")
async def count_to_n_method(request: Request):
    try:
        n = int(request.params.get("n", 5))
    except Exception:
        return Response(error={"message": "Invalid number"})

    # Instead of returning immediately, we stream numbers
    for i in range(1, n + 1):
        await asyncio.sleep(1)  # simulate work
        # Send a streaming event to the client
        yield Event(name="progress", data={"current": i})

    # Final response after streaming is done
    return Response(result={"message": f"Finished counting to {n}!"})

if __name__ == "__main__":
    server.run_stdio()
```

**Key changes:**

* The handler is now a **generator function** that `yield`s `Event` objects before returning a final `Response`.
* Each `yield` sends an event to the client **in real time**.

---

## Step 2 — Create the Streaming MCP Client

File: `mcp_client_stream.py`

```python
import asyncio
from modelcontextprotocol import Client

async def main():
    client = Client(name="StreamingClient")

    # Start server
    await client.connect_to_subprocess(["python", "mcp_server_stream.py"])

    print("Starting streamed count...")
    async for event_or_response in client.request_stream("count_to_n", params={"n": 5}):
        if event_or_response.type == "event":
            print(f"Progress event: {event_or_response.data}")
        elif event_or_response.type == "response":
            print(f"Final response: {event_or_response.result}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Step 3 — Run It

```bash
python mcp_client_stream.py
```

---

## Step 4 — Expected Output

```
Starting streamed count...
Progress event: {'current': 1}
Progress event: {'current': 2}
Progress event: {'current': 3}
Progress event: {'current': 4}
Progress event: {'current': 5}
Final response: {'message': 'Finished counting to 5!'}
```

---

## Step 5 — What You Learned

* MCP supports **generators** in methods for streaming data.
* You can emit intermediate **Event** objects before the final **Response**.
* The client can consume events as they arrive using `request_stream()`.
