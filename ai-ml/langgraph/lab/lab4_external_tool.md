# Lab 4: Adding Tools to LangGraph

In this lab, you’ll expand your conversational graph by:

* Introducing **external tools** (like a calculator).
* Allowing the bot to decide when to call a tool.
* Returning results to the user.

---

## Objectives

1. Wrap Python functions as **tools**.
2. Extend the graph to handle tool calls.
3. Route between **chat** and **tool execution**.

---

## Steps

### 1. Setup

Continue in the same project folder as before. Install extra dependencies if not already installed:

```bash
pip install langchain-core
```

### 2. Create File: `lab04_tools.py`

```python
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from rich import print
import math

# Step 1: Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]
    route: str

# Step 2: Define a Tool
@tool
def calc(expr: str) -> str:
    """Evaluate a basic math expression like '2 * (3 + 4)'."""
    try:
        return str(eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt}))
    except Exception as e:
        return f"Error: {e}"

# Step 3: Define Nodes

def router(state: State) -> Literal["math", "chat"]:
    """Route to math if message looks like a calculation, else chat."""
    last = state["messages"][-1]["content"].lower()
    if any(k in last for k in ["calc", "calculate", "sqrt", "+", "-", "*", "/"]):
        return "math"
    return "chat"

def do_math(state: State):
    user_message = state["messages"][-1]["content"]
    result = calc.invoke({"expr": user_message})
    reply = f"🧮 The result is {result}"
    print(reply)
    return {"messages": [AIMessage(content=reply)]}

def chat(state: State):
    user_message = state["messages"][-1]["content"]
    reply = f"💬 I heard you say: '{user_message}'"
    print(reply)
    return {"messages": [AIMessage(content=reply)]}

# Step 4: Build Graph
builder = StateGraph(State)

builder.add_node("router", router)
builder.add_node("math", do_math)
builder.add_node("chat", chat)

builder.set_entry_point("router")

builder.add_conditional_edges("router", router, {"math": "math", "chat": "chat"})

builder.add_edge("math", END)
builder.add_edge("chat", END)

# Step 5: Compile Graph
app = builder.compile()

# Step 6: Run Tests
print("[bold green]\nTest 1: Math input[/bold green]")
result1 = app.invoke({"messages": [{"role":"user","content":"sqrt(144) + 2"}]})
print("Final Result:", result1)

print("[bold green]\nTest 2: Chat input[/bold green]")
result2 = app.invoke({"messages": [{"role":"user","content":"Hello, LangGraph bot!"}]})
print("Final Result:", result2)
```

---

## Expected Output

```text
Test 1: Math input
🧮 The result is 14.0
Final Result: {'messages': [... AI reply ...]}

Test 2: Chat input
💬 I heard you say: 'Hello, LangGraph bot!'
Final Result: {'messages': [... AI reply ...]}
```

---

## Check Your Work ✅

* Did math queries get routed to the calculator?
* Did normal text go to the chat node?

If yes, you’ve successfully built your **first tool-using LangGraph bot** 🎉

---

## Next Steps

In Lab 5, you’ll learn how to:

* Integrate **retrievers** (for RAG).
* Make the bot answer from documents instead of just memory.
