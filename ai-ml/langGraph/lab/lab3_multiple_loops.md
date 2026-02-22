# Lab 3: Looping Edges & Multi-Turn Conversation in LangGraph

In this lab, you’ll expand on branching graphs by:

* Adding **looping edges**.
* Maintaining state across multiple turns.
* Creating a simple conversational flow that continues until the user says "stop".

---

## Objectives

1. Extend your graph with looping edges.
2. Store a **conversation history** in the state.
3. Continue the loop until a stop condition is reached.

---

## Steps

### 1. Setup

Continue in the same project folder as Lab 1 and Lab 2. No extra dependencies required.

### 2. Create File: `lab03_looping.py`

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from rich import print

# Step 1: Define State with conversation history
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step 2: Define Nodes

def user_node(state: State):
    """Simulate user input. If last message was 'stop', end conversation."""
    last_message = state["messages"][-1]["content"] if state["messages"] else ""
    if last_message.strip().lower() == "stop":
        print("[red]User ended the conversation.[/red]")
        return {}
    else:
        return {"messages": [{"role": "user", "content": input("You: ")}]}

def bot_node(state: State):
    """Bot replies to user input."""
    user_message = state["messages"][-1]["content"]
    reply = f"🤖 Bot: I heard you say '{user_message}'"
    print(reply)
    return {"messages": [{"role": "assistant", "content": reply}]}

# Step 3: Build Graph
builder = StateGraph(State)

builder.add_node("user", user_node)
builder.add_node("bot", bot_node)

builder.set_entry_point("user")

# Loop: user -> bot -> user
builder.add_edge("user", "bot")
builder.add_edge("bot", "user")

# Add edge to END when stop is detected
builder.add_edge("user", END)

# Step 4: Compile Graph
app = builder.compile()

# Step 5: Run Conversation
print("[bold green]Type messages to chat with the bot. Type 'stop' to end.[/bold green]")
state = {"messages": []}

app.invoke(state)
```

### 3. Run the Lab

```bash
python lab03_looping.py
```

---

## Example Run

```text
Type messages to chat with the bot. Type 'stop' to end.
You: Hello bot
🤖 Bot: I heard you say 'Hello bot'
You: How are you?
🤖 Bot: I heard you say 'How are you?'
You: stop
User ended the conversation.
```

---

## Check Your Work ✅

* Did the bot keep responding until you typed `stop`?
* Did the conversation history grow with each turn?

If yes, you’ve built your first **looping conversation graph** 🎉

---

## Next Steps

In Lab 4, you’ll:

* Add **external tools** (like a calculator).
* Learn how to let the bot decide whether to call a tool or just chat.
