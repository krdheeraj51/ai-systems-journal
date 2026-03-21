# 🧪 Lab 10: Hybrid System (RAG + Agents Integration)

## 🎯 Objective
- Combine RAG and Agents into one system
- Enable agent to decide:
  - retrieve knowledge OR
  - use tools
- Build an intelligent assistant capable of reasoning + knowledge retrieval

---

## 📚 Concepts Covered
- Hybrid architecture (RAG + Agents)
- Tool-based retrieval
- Agent decision routing
- Knowledge + action integration
- Real-world system design

---

## ⚙️ Prerequisites
- Lab 5–9 completed
- Working RAG pipeline
- Working Agent with tools
- Azure OpenAI setup ready

---

## 🧠 Step 1: Problem Statement

RAG alone:
- ❌ Cannot perform actions

Agent alone:
- ❌ No external knowledge

👉 Combine both:
- ✅ Retrieve information
- ✅ Perform actions

---

## 🧪 Step 2: Convert RAG into a Tool

```python id="lab10_code1"
from langchain_core.tools import tool

@tool
def retrieve_info(query: str) -> str:
    """Retrieve information from documents"""
    docs = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in docs)
````

---

## 🧪 Step 3: Add Existing Tools

```python id="lab10_code2"
tools = [retrieve_info, add, multiply]
```

---

## 🧠 Step 4: Bind Tools to Model

```python id="lab10_code3"
model_with_tools = model.bind_tools(tools)
```

---

## 🧪 Step 5: Smart Agent Prompt

```python id="lab10_code4"
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intelligent assistant.

Rules:
- Use retrieve_info tool for knowledge questions
- Use math tools for calculations
- Combine tools if needed
- Think step-by-step
"""),
    ("user", "{input}")
])
```

---

## 🧪 Step 6: Create Agent Executor

```python id="lab10_code5"
from langchain.agents import AgentExecutor

agent_chain = prompt | model_with_tools

agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=tools,
    verbose=True,
    max_iterations=5
)
```

---

## 🧪 Step 7: Test Hybrid Queries

### Case 1: Knowledge Query

```python id="lab10_code6"
agent_executor.invoke({
    "input": "What is LangChain?"
})
```

👉 Uses: retrieve_info

---

### Case 2: Action Query

```python id="lab10_code7"
agent_executor.invoke({
    "input": "Multiply 5 and 6"
})
```

👉 Uses: multiply tool

---

### Case 3: Hybrid Query

```python id="lab10_code8"
agent_executor.invoke({
    "input": "What is LangChain and multiply 5 by 3"
})
```

👉 Uses:

* retrieve_info
* multiply

---

## 🔥 Step 8: What’s Happening?

Agent decides dynamically:

* Which tool to use
* In what order
* How to combine results

---

## 🧠 Step 9: Improve Retrieval Tool (Production Upgrade)

```python id="lab10_code9"
@tool
def retrieve_info(query: str) -> str:
    """Retrieve relevant information from knowledge base"""
    docs = retriever.invoke(query)
    
    if not docs:
        return "No relevant information found."
    
    return "\n\n".join(
        f"[Source]\n{doc.page_content}" for doc in docs
    )
```

---

## 🧠 Step 10: Add Safety & Control

```python id="lab10_code10"
agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)
```

---

## 📤 Expected Output

```id="lab10_out"
User: What is LangChain and multiply 5 by 3

Agent:
- Retrieves info about LangChain
- Calls multiply tool → 15
- Combines both answers
```

---

## 🧠 Key Takeaways

* Hybrid systems = **real-world AI architecture**
* RAG provides knowledge
* Agents provide reasoning/actions
* Tool-based design is scalable

---

## 🧪 Exercises

1. Add tool:

   * summarize(text)
2. Ask:

   * "Summarize LangChain and multiply 10 by 2"
3. Add condition:

   * limit retrieval length
4. Add second document source

---

## 📚 References

* RAG: [https://python.langchain.com/docs/use_cases/question_answering/](https://python.langchain.com/docs/use_cases/question_answering/)
* Agents: [https://python.langchain.com/docs/modules/agents/](https://python.langchain.com/docs/modules/agents/)

