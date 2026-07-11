# Lab 5: LangGraph with Retrieval-Augmented Generation (RAG) using ChromaDB

In this lab, you’ll expand your LangGraph bot by:

* Integrating a **retriever tool** for knowledge lookup.
* Using **ChromaDB + embeddings** to index and query documents.
* Routing between normal chat, calculator, and RAG search.

---

## Objectives

1. Build a **document retriever** using ChromaDB.
2. Wrap it as a LangChain **tool**.
3. Extend the graph to handle queries about documents.

---

## Steps

### 1. Setup

Install extra packages if not already installed:

```bash
pip install chromadb sentence-transformers langchain-text-splitters
```

Put a couple of `.txt` or `.md` files into the `data/` folder for retrieval.

### 2. Create File: `lab05_rag.py`

```python
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from rich import print
import glob, math, os

# Step 1: Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]
    route: str

# Step 2: Prepare Retriever
def build_retriever():
    files = glob.glob("data/*.txt") + glob.glob("data/*.md")
    docs = []
    for f in files:
        docs.extend(TextLoader(f).load())

    if not docs:
        from langchain_core.documents import Document
        docs = [Document(page_content="LangGraph is a framework for building stateful AI workflows.")]

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Use Chroma as vector store
    persist_dir = "chroma_db"
    vs = Chroma.from_documents(chunks, emb, persist_directory=persist_dir)
    return vs.as_retriever(search_kwargs={"k": 3})

retriever = build_retriever()

# Step 3: Define Tools
@tool
def calc(expr: str) -> str:
    try:
        return str(eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt}))
    except Exception as e:
        return f"Error: {e}"

@tool
def search_docs(query: str) -> str:
    results = retriever.get_relevant_documents(query)
    return "\n---\n".join([d.page_content[:200] for d in results])

# Step 4: Define Router
def router(state: State) -> Literal["math", "rag", "chat"]:
    last = state["messages"][-1]["content"].lower()
    if any(k in last for k in ["calc", "calculate", "sqrt", "+", "-", "*", "/"]):
        return "math"
    if "doc" in last or "file" in last or "explain" in last:
        return "rag"
    return "chat"

# Step 5: Define Nodes
def do_math(state: State):
    user_message = state["messages"][-1]["content"]
    result = calc.invoke({"expr": user_message})
    reply = f"🧮 The result is {result}"
    print(reply)
    return {"messages": [AIMessage(content=reply)]}

def do_rag(state: State):
    user_message = state["messages"][-1]["content"]
    docs = search_docs.invoke({"query": user_message})
    reply = f"📚 Based on documents, here’s what I found:\n{docs}"
    print(reply)
    return {"messages": [AIMessage(content=reply)]}

def chat(state: State):
    user_message = state["messages"][-1]["content"]
    reply = f"💬 I heard you say: '{user_message}'"
    print(reply)
    return {"messages": [AIMessage(content=reply)]}

# Step 6: Build Graph
builder = StateGraph(State)

builder.add_node("router", router)
builder.add_node("math", do_math)
builder.add_node("rag", do_rag)
builder.add_node("chat", chat)

builder.set_entry_point("router")

builder.add_conditional_edges("router", router, {
    "math": "math",
    "rag": "rag",
    "chat": "chat"
})

builder.add_edge("math", END)
builder.add_edge("rag", END)
builder.add_edge("chat", END)

# Step 7: Compile & Run
app = builder.compile()

print("[bold green]\nTest 1: Math input[/bold green]")
result1 = app.invoke({"messages": [{"role":"user","content":"sqrt(100) + 10"}]})
print("Final Result:", result1)

print("[bold green]\nTest 2: RAG input[/bold green]")
result2 = app.invoke({"messages": [{"role":"user","content":"Explain what the docs say about LangGraph"}]})
print("Final Result:", result2)

print("[bold green]\nTest 3: Chat input[/bold green]")
result3 = app.invoke({"messages": [{"role":"user","content":"Hello bot!"}]})
print("Final Result:", result3)
```

---

## Expected Output

```text
Test 1: Math input
🧮 The result is 20.0
Final Result: {...}

Test 2: RAG input
📚 Based on documents, here’s what I found:
LangGraph is a framework for building stateful AI workflows.
Final Result: {...}

Test 3: Chat input
💬 I heard you say: 'Hello bot!'
Final Result: {...}
```

---

## Check Your Work ✅

* Did math queries hit the calculator?
* Did document-related queries pull from your files (via ChromaDB)?
* Did other inputs go to plain chat?

If yes, you’ve built a **RAG-enabled LangGraph agent using ChromaDB** 🎉

---

## Next Steps

In Lab 6, you’ll:

* Combine **looping edges** with RAG.
* Maintain a multi-turn conversation while still using tools.
