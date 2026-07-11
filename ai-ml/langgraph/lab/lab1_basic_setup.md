# Lab 1: Basic Setup & First LangGraph Node

This is your **first LangGraph lab**. In this exercise, you’ll:

* Set up your environment.
* Create a **graph with a single node and an edge**.
* Run your first execution with LangGraph.

---

## Objectives

1. Install and configure LangGraph.
2. Define a simple **state**.
3. Create a **node** that processes the state.
4. Connect the node with an **edge**.
5. Run the graph and print the result.

---

## Steps

### 1. Create Project & Virtual Environment

```bash
mkdir langgraph-labs && cd langgraph-labs
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -U pip
pip install langgraph langchain-community rich
```

### 3. Create File: `lab01_setup.py`

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from rich import print

# Step 1: Define the State
class State(TypedDict):
    message: str

# Step 2: Create a Node Function
def say_hello(state: State):
    user_message = state["message"]
    return {"message": f"Hello! You said: {user_message}"}

# Step 3: Build the Graph
builder = StateGraph(State)

# Add node
builder.add_node("greeter", say_hello)

# Set entry point
builder.set_entry_point("greeter")

# Add edge to END
builder.add_edge("greeter", END)

# Step 4: Compile the Graph
app = builder.compile()

# Step 5: Run the Graph
result = app.invoke({"message": "This is my first LangGraph lab!"})
print("[bold green]Result:[/bold green]", result)
```

### 4. Run the Lab

```bash
python lab01_setup.py
```

---

## Expected Output

```text
Result: {'message': 'Hello! You said: This is my first LangGraph lab!'}
```

---

## Check Your Work ✅

* Did the script run without errors?
* Did you see your input echoed back with the `Hello!` prefix?

If yes, congratulations 🎉 you’ve built your first LangGraph node and edge!

---

## Next Steps

In the next lab, you’ll:

* Add **multiple nodes**.
* Create **branching edges**.
* Pass richer state between nodes.
