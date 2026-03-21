# 🧪 Lab 11: Streaming & Async with LangChain (Real-Time AI Responses)

## 🎯 Objective
- Enable streaming responses from Azure OpenAI
- Implement async execution in LangChain
- Build real-time user experience
- Optimize latency and responsiveness

---

## 📚 Concepts Covered
- Streaming in LangChain
- Async execution (`ainvoke`)
- Token-level streaming
- Callback handlers
- Real-time pipelines

---

## ⚙️ Prerequisites
- Lab 1–10 completed
- Azure OpenAI model ready
- Understanding of LCEL pipelines

---

## 🧠 Step 1: Why Streaming?

Without streaming:
- ❌ User waits for full response

With streaming:
- ✅ Tokens appear instantly
- ✅ Better UX
- ✅ Lower perceived latency

---

## 🧪 Step 2: Enable Streaming in Model

```python id="lab11_code1"
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_deployment="your-chat-deployment",
    api_version="your-api-version",
    streaming=True
)
````

---

## 🧪 Step 3: Basic Streaming Example

```python id="lab11_code2"
for chunk in model.stream("Explain LangChain in simple terms"):
    print(chunk.content, end="", flush=True)
```

---

## 🧠 Step 4: Streaming with LCEL Chain

```python id="lab11_code3"
chain = prompt | model

for chunk in chain.stream({"topic": "RAG systems"}):
    print(chunk.content, end="", flush=True)
```

---

## 🧪 Step 5: Async Execution (IMPORTANT)

```python id="lab11_code4"
response = await chain.ainvoke({"topic": "LangChain"})
print(response.content)
```

---

## 🧪 Step 6: Async Streaming

```python id="lab11_code5"
async for chunk in chain.astream({"topic": "AI Agents"}):
    print(chunk.content, end="", flush=True)
```

---

## 🧠 Step 7: Combine with RAG

```python id="lab11_code6"
async for chunk in rag_chain.astream("What is LangChain?"):
    print(chunk, end="", flush=True)
```

---

## 🧪 Step 8: Streaming in Agent

```python id="lab11_code7"
async for chunk in agent_executor.astream({
    "input": "Multiply 5 and 6"
}):
    print(chunk, end="", flush=True)
```

---

## 🧠 Step 9: Callback Handlers (Advanced)

```python id="lab11_code8"
from langchain_core.callbacks import BaseCallbackHandler

class MyHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        print(token, end="", flush=True)
```

Attach handler:

```python id="lab11_code9"
model = AzureChatOpenAI(
    azure_deployment="your-chat-deployment",
    streaming=True,
    callbacks=[MyHandler()]
)
```

---

## 🔥 Step 10: Real-World Usage Patterns

Streaming is used in:

* Chat applications
* Dashboards
* Voice assistants
* APIs (FastAPI streaming)

---

## 📤 Expected Output

```id="lab11_out"
LangChain is a framework... (streaming word by word)
```

---

## 🧠 Key Takeaways

* Streaming improves UX dramatically
* Async = better scalability
* LCEL fully supports streaming
* Callback handlers give fine control

---

## 🧪 Exercises

1. Stream RAG responses
2. Add delay simulation and observe streaming benefits
3. Use async for multiple simultaneous queries
4. Combine streaming + agent + RAG

---

## 📚 References

* Streaming: [https://python.langchain.com/docs/expression_language/streaming/](https://python.langchain.com/docs/expression_language/streaming/)
* Async: [https://python.langchain.com/docs/expression_language/async/](https://python.langchain.com/docs/expression_language/async/)

```

---

## 🔥 Where You Are Now

You can now build:
- ⚡ Real-time AI applications
- ⚡ Scalable async pipelines
- ⚡ Production-grade UX