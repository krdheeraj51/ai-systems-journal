# 🧪 Lab 8: Building Agents with Tools (LangChain v0.2 + Azure OpenAI)

## 🎯 Objective
- Understand what Agents are
- Learn how LLMs use tools
- Build your first agent using LangChain v0.2
- Integrate tools into LCEL workflows

---

## 📚 Concepts Covered
- Agents vs Chains
- Tools in LangChain
- Function calling (tool calling)
- AgentExecutor
- Tool binding with LLM
- Decision-making workflows

---

## ⚙️ Prerequisites
- Lab 1–7 completed
- Strong understanding of LCEL and RAG
- Azure OpenAI setup ready

---

## 🧠 Step 1: What is an Agent?

### Chain:
- Fixed flow ❌

### Agent:
- Dynamic decision-making ✅
- Chooses:
  - which tool to use
  - when to use it

---

## 🧪 Step 2: Define a Simple Tool

```python id="lab8_code1"
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
````

---

## 🧪 Step 3: Initialize Model with Tool Calling

```python id="lab8_code2"
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_deployment="your-chat-deployment",
    api_version="your-api-version",
)

model_with_tools = model.bind_tools([multiply])
```

---

## 🧪 Step 4: Create Agent Prompt

```python id="lab8_code3"
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])
```

---

## 🧪 Step 5: Create Agent Chain

```python id="lab8_code4"
agent_chain = prompt | model_with_tools
```

---

## 🧪 Step 6: Invoke Agent

```python id="lab8_code5"
response = agent_chain.invoke({"input": "What is 5 multiplied by 3?"})
print(response)
```

👉 The model decides:

* "This is math"
* Calls the tool

---

## 🧠 Step 7: Add Tool Execution Loop (AgentExecutor)

```python id="lab8_code6"
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=[multiply],
    verbose=True
)

response = agent_executor.invoke({"input": "Multiply 10 and 20"})
print(response)
```

---

## 🔥 Step 8: What’s Happening Internally?

1. User asks question
2. LLM decides:

   * Use tool OR respond directly
3. Tool executes
4. LLM formats final answer

---

## 🧪 Step 9: Add Multiple Tools

```python id="lab8_code7"
@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

model_with_tools = model.bind_tools([multiply, add])
```

---

## 🧠 Step 10: Improve Prompt (Production Pattern)

```python id="lab8_code8"
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intelligent assistant.

Use tools when necessary.
Explain your reasoning briefly.
"""),
    ("user", "{input}")
])
```

---

## 📤 Expected Output

```id="lab8_out"
User: Multiply 10 and 20

Agent:
- Decides to use multiply tool
- Calls tool
- Returns: 200
```

---

## 🧠 Key Takeaways

* Agents = decision-making systems
* Tools extend LLM capability
* Tool calling = structured + reliable
* Agents are foundation of:

  * copilots
  * automation systems
  * AI workflows

---

## 🧪 Exercises

1. Create a tool:

   * weather lookup (mock)
2. Create tool:

   * string formatter
3. Ask:

   * "Add 5 and 10, then multiply by 2"
     → Observe behavior

---

## 📚 References

* Agents: [https://python.langchain.com/docs/modules/agents/](https://python.langchain.com/docs/modules/agents/)
* Tools: [https://python.langchain.com/docs/modules/tools/](https://python.langchain.com/docs/modules/tools/)

```

---

## 🔥 Where You Are Now

You can now build:
- AI systems that **take actions**
- Not just answer questions


