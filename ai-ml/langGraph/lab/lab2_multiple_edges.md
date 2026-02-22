# Lab 2: Multiple Nodes & Branching Edges in LangGraph

In this lab, you’ll extend your knowledge from Lab 1 by:

* Creating **multiple nodes**.
* Adding **branching logic** using conditional edges.
* Passing state between nodes.

---

## Objectives

1. Extend the graph with more than one node.
2. Add a **router node** to decide the flow.
3. Implement branching edges based on conditions.
4. Run the graph with different inputs.

---

## Steps

### 1. Setup

Continue inside the same project from Lab 1. No new packages are required.

### 2. Create File: `lab02_branching.py`

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from rich import print

# Step 1: Define State
class State(TypedDict):
    message: str
    route: str

# Step 2: Node Functions
# Router node: decides path

def router(state: State) -> Literal["greet", "farewell"]:
    text = state["message"].lower()
    if "bye" in text or "goodbye" in text:
        return "farewell"
    return "greet"

# Greeting node
def greet_node(state: State):
    return {"message": f"👋 Hi there! You said: {state['message']}"}

# Farewell node
def farewell_node(state: State):
    return {"message": f"👋 Goodbye! You said: {state['message']}"}

# Step 3: Build Graph
builder = StateGraph(State)

# Add nodes
builder.add_node("router", router)
builder.add_node("greet", greet_node)
builder.add_node("farewell", farewell_node)

# Set entry point
builder.set_entry_point("router")

# Add conditional edges from router
builder.add_conditional_edges(
    "router",  # source node
    router,    # function to decide
    {"greet": "greet", "farewell": "farewell"}  # map condition -> target node
)

# Add terminal edges
builder.add_edge("greet", END)
builder.add_edge("farewell", END)

# Step 4: Compile
app = builder.compile()

# Step 5: Run with different inputs
print("[bold cyan]\nTest 1: Greeting input[/bold cyan]")
result1 = app.invoke({"message": "Hello, LangGraph!"})
print("Result:", result1)

print("[bold cyan]\nTest 2: Farewell input[/bold cyan]")
result2 = app.invoke({"message": "Goodbye LangGraph!"})
print("Result:", result2)
```

### 3. Run the Lab

```bash
python lab02_branching.py
```

---

## Expected Output

```text
Test 1: Greeting input
Result: {'message': '👋 Hi there! You said: Hello, LangGraph!'}

Test 2: Farewell input
Result: {'message': '👋 Goodbye! You said: Goodbye LangGraph!'}
```

---

## Check Your Work ✅

* Did the router correctly direct greetings to the greet node?
* Did farewells go to the farewell node?

If yes, you’ve successfully built your **first branching graph** in LangGraph 🎉

---

## Next Steps

In Lab 3, you’ll learn how to:

* Introduce **looping edges**.
* Keep the conversation going across multiple steps.
