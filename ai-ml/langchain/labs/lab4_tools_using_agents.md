# Lab 4 — Tool-Using Agent (Function Calling) with Azure OpenAI

## Objective

Learn how to:

* Define **tools** (Python functions) with clear docstrings so the model can call them.
* Create a **tool-calling agent** that decides which tool to use and when.
* Execute multi-step reasoning where the agent can call multiple tools before answering.

By the end, your agent can solve math with a calculator tool and fetch blurbs from a tiny KB — and you can easily add more tools.

---

## Step 0 — Prereqs

From earlier labs you should already have:

* venv + packages
* Azure OpenAI **chat deployment** (e.g., `gpt-4o-mini`)
* Environment variables:

```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-06-01"
export AZURE_OPENAI_CHAT_DEPLOYMENT="your-chat-deployment-name"
```

Install (if you haven’t already):

```bash
pip install -U langchain langchain-openai langchain-core langchain-community
```

---

## Step 1 — Create `lab4_agent_tools.py`

```python
import os, math
from typing import Optional

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ---------------------------
# 1) Define Tools
# ---------------------------

@tool
def calc(expression: str) -> str:
    """Evaluate a math expression safely, e.g. '2*(3+4)' or 'sqrt(144)+11'.
    Allowed: + - * / ** ( ) and sqrt from math."""
    try:
        # Very small whitelist environment for safety:
        safe_env = {"__builtins__": {}}
        safe_funcs = {"sqrt": math.sqrt}
        result = eval(expression, safe_env, safe_funcs)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

KB = {
    "langchain": "LangChain is a framework for building LLM apps with chains, tools, memory, and agents.",
    "agent": "Agents use an LLM to choose actions (tool calls) to achieve a goal.",
    "rag": "RAG augments an LLM with retrieved context from external knowledge.",
}

@tool
def kb_lookup(topic: str) -> str:
    """Return a short blurb for a topic from a tiny local KB. Try topics like 'langchain', 'agent', or 'rag'."""
    return KB.get(topic.strip().lower(), "Not found")

tools = [calc, kb_lookup]

# ---------------------------
# 2) LLM (Azure OpenAI)
# ---------------------------
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0,  # deterministic for repeatable tool choices
)

# ---------------------------
# 3) Agent Prompt
# ---------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant that can use tools. "
     "If using a tool would help, call it. "
     "Show the final answer clearly. If a tool fails, try to recover or explain."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")  # where intermediate tool-calls/observations go
])

# ---------------------------
# 4) Assemble Agent + Executor
# ---------------------------
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # verbose=True prints the reasoning/tool calls

# ---------------------------
# 5) Demo Runs
# ---------------------------
if __name__ == "__main__":
    # Example 1: force tool use
    out1 = executor.invoke({"input": "What is sqrt(144) + 11? Use the calculator."})
    print("\nFINAL:", out1["output"])

    # Example 2: autonomous choice
    out2 = executor.invoke({"input": "Explain what an 'agent' is in LangChain. Check the KB."})
    print("\nFINAL:", out2["output"])

    # Example 3: multiple steps (calc first, then explanation)
    out3 = executor.invoke({"input": "Compute (23*5 - 7) / 4 with the calculator, then explain your steps briefly."})
    print("\nFINAL:", out3["output"])

    # Interactive loop (optional)
    # while True:
    #     q = input("\nAsk the agent (or 'exit'): ").strip()
    #     if q.lower() == "exit":
    #         break
    #     res = executor.invoke({"input": q})
    #     print("\nFINAL:", res["output"])
```

---

## Step 2 — Run it

```bash
python lab4_agent_tools.py
```

**What you’ll see (abridged, will vary):**

* The agent prints intermediate steps due to `verbose=True`, like:

  * It “decides” to call the `calc` tool with `sqrt(144)+11`
  * It receives the tool’s output (`23.0`)
  * It produces the final, user-facing answer
* For the KB question, it calls `kb_lookup(topic="agent")` and uses the result in the final answer.

---

## Step 3 — How it works (mental model)

* **Tools**: Simple Python functions wrapped with `@tool`. Clear docstrings help the model decide when/how to use them.
* **Prompt**: Includes `agent_scratchpad`, where LangChain tracks intermediate tool calls & observations.
* **Agent**: `create_tool_calling_agent` configures the LLM to use OpenAI-style function calling under the hood.
* **Executor**: Orchestrates the loop: model thinks → chooses tool → tool runs → model sees result → repeats → final answer.

---

## Step 4 — Add your own tools (quick patterns)

1. **HTTP fetch (read-only)**
   Create a function that fetches a URL and returns summarized text (be mindful of network and parsing).
2. **File reader**
   A tool that loads a local `.txt` or `.md` snippet (useful for quick RAG-lite).
3. **SQL query**
   Use `langchain-community` SQL tools to query a small SQLite DB.

> Tip: Keep tool **signatures simple** (strings, numbers) and docstrings **crisp** so the model picks the right tool.

---

## Step 5 — Troubleshooting

* **Agent never calls a tool**

  * Lower temperature (already 0 here) and improve the tool’s docstring (be explicit: “Use this to do math.”).
  * Add a user hint like *“Use the calculator.”* in the prompt to nudge it.
* **Tool errors (“Error: …”)**

  * Your expression may be unsupported. The `calc` tool only allows `sqrt` and arithmetic. Extend the whitelist if needed.
* **Auth errors / 401 / 404**

  * Re-check your Azure env vars and that your **deployment name** matches exactly.

---

## Step 6 — Extensions (next-level)

* **Guardrails**: Validate tool inputs (e.g., with Pydantic) before executing.
* **Multi-turn tool use**: Ask the agent a question requiring multiple tool calls, e.g., “Look up term X in KB, then compute Y with calc, then summarize both.”
* **Observability**: Log tool inputs/outputs for debugging (without logging secrets).
* **Policies**: Add a system message that forbids certain tool invocations or constrains behavior.

---

## Step 7 — Checklist

* [ ] I can define tools with `@tool` and clear docstrings.
* [ ] I can build a tool-calling agent with `create_tool_calling_agent`.
* [ ] I can run multi-step tasks where the agent chooses and executes tools.
* [ ] I understand how `verbose=True` reveals the tool-use trace.

---

Want me to craft **Lab 5 — Multi-Agent Workflow with LangGraph** next (Researcher → Writer → Critic), still on Azure OpenAI? It’s a great step toward real Agentic AI pipelines.
