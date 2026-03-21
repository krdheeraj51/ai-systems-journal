# 🧪 Lab 9: Advanced Agents (Multi-Step Reasoning + Tool Orchestration)

## 🎯 Objective
- Build advanced agents capable of multi-step reasoning
- Enable tool chaining (tool → tool → final answer)
- Improve agent reliability and control
- Handle complex user queries

---

## 📚 Concepts Covered
- Multi-step reasoning
- Tool orchestration
- Agent planning behavior
- Intermediate steps handling
- Controlling agent execution
- ReAct-style reasoning (LangChain approach)

---

## ⚙️ Prerequisites
- Lab 8 completed (basic agents)
- Understanding of tools and AgentExecutor
- Azure OpenAI setup ready

---

## 🧠 Step 1: Problem with Basic Agents

Basic agent:
- ❌ Handles simple queries only

Advanced agent:
- ✅ Breaks problem into steps
- ✅ Uses multiple tools
- ✅ Combines outputs

---

## 🧪 Step 2: Define Multiple Tools

```python id="lab9_code1"
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def square(x: int) -> int:
    """Square a number"""
    return x * x
````

---

## 🧪 Step 3: Bind Tools to Model

```python id="lab9_code2"
model_with_tools = model.bind_tools([add, multiply, square])
```

---

## 🧠 Step 4: Advanced Prompt (Guiding Reasoning)

```python id="lab9_code3"
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intelligent assistant.

You can:
- Break problems into steps
- Use tools multiple times
- Think step-by-step before answering
"""),
    ("user", "{input}")
])
```

---

## 🧪 Step 5: Create Agent Executor

```python id="lab9_code4"
from langchain.agents import AgentExecutor

agent_chain = prompt | model_with_tools

agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=[add, multiply, square],
    verbose=True,
    max_iterations=5
)
```

---

## 🧪 Step 6: Multi-Step Query

```python id="lab9_code5"
response = agent_executor.invoke({
    "input": "Add 5 and 3, then multiply the result by 10, then square it"
})

print(response)
```

---

## 🔥 Step 7: What Happens Internally?

Agent reasoning:

1. Add 5 + 3 = 8
2. Multiply 8 × 10 = 80
3. Square 80 = 6400
4. Return final answer

---

## 🧪 Step 8: Control Agent Behavior

```python id="lab9_code6"
agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=[add, multiply, square],
    verbose=True,
    max_iterations=3,        # limit reasoning steps
    handle_parsing_errors=True
)
```

---

## 🧠 Step 9: Add Safety Constraints

```python id="lab9_code7"
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a safe and reliable assistant.

- Do not guess
- Use tools when needed
- If unsure, say "I don't know"
"""),
    ("user", "{input}")
])
```

---

## 🧪 Step 10: Debug Intermediate Steps

```python id="lab9_code8"
result = agent_executor.invoke(
    {"input": "Multiply 4 and 5, then add 10"},
    return_intermediate_steps=True
)

print(result)
```

---

## 📤 Expected Output

```id="lab9_out"
Final Answer: 30

Intermediate Steps:
- multiply(4,5) → 20
- add(20,10) → 30
```

---

## 🧠 Key Takeaways

* Agents can perform **multi-step reasoning**
* Tools can be chained dynamically
* Prompt design controls reasoning quality
* Iteration limits prevent infinite loops

---

## 🧪 Exercises

1. Add a new tool:

   * divide(a, b)
2. Ask:

   * "((5+5)*2)^2"
3. Force error:

   * divide by zero → handle gracefully
4. Limit agent to 2 steps → observe failure

---

## 📚 References

* Agents Advanced: [https://python.langchain.com/docs/modules/agents/](https://python.langchain.com/docs/modules/agents/)
* Tool Calling: [https://python.langchain.com/docs/modules/tools/](https://python.langchain.com/docs/modules/tools/)

```

---

## 🔥 Where You Are Now

You can now build:
- **Multi-step reasoning systems**
- **Tool-driven AI workflows**
- Systems close to:
  - copilots
  - automation engines
