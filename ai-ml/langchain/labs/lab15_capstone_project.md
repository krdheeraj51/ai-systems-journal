# 🧪 Lab 15: Capstone Project — Production-Ready AI Assistant System

## 🎯 Objective
Build a complete AI system that:
- Answers questions using RAG
- Uses tools via Agents
- Maintains conversation memory
- Streams responses
- Applies guardrails
- Exposes API via FastAPI

---

## 📚 Concepts Covered
- End-to-end system design
- RAG + Agent hybrid system
- Conversational memory
- Streaming responses
- Guardrails & validation
- API deployment architecture

---

## ⚙️ Prerequisites
- Lab 1–14 completed
- Azure OpenAI setup ready
- FAISS vector store ready

---

## 🧠 Step 1: Final Architecture

User → API → Guardrails → Agent  
→ (RAG OR Tools) → Memory → Streaming Response

---

## 📁 Step 2: Project Structure

```text id="lab15_structure"
project/
│
├── app.py
├── chains/
│   ├── rag.py
│   ├── agent.py
│
├── tools/
│   ├── tools.py
│
├── memory/
│   ├── memory.py
│
├── utils/
│   ├── guardrails.py
│   ├── config.py
│
├── models/
│   ├── request.py
│
├── vectorstore/
│   ├── faiss_index/
│
├── .env
````

---

## 🧪 Step 3: Setup Model

```python id="lab15_code1"
model = AzureChatOpenAI(
    azure_deployment="your-chat-deployment",
    api_version="your-api-version",
    streaming=True
)
```

---

## 🧪 Step 4: Load Vector Store

```python id="lab15_code2"
vectorstore = FAISS.load_local("faiss_index", embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

---

## 🧪 Step 5: RAG Tool

```python id="lab15_code3"
@tool
def retrieve_info(query: str) -> str:
    docs = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in docs)
```

---

## 🧪 Step 6: Define Tools

```python id="lab15_code4"
@tool
def add(a: int, b: int) -> int:
    return a + b

tools = [retrieve_info, add]
```

---

## 🧠 Step 7: Memory Setup

```python id="lab15_code5"
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

---

## 🧪 Step 8: Prompt (Final Version)

```python id="lab15_code6"
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a safe and intelligent assistant.

Rules:
- Use tools when needed
- Use retrieve_info for knowledge
- If unsure, say "I don't know"
"""),
    ("placeholder", "{chat_history}"),
    ("user", "{input}")
])
```

---

## 🧪 Step 9: Agent Setup

```python id="lab15_code7"
model_with_tools = model.bind_tools(tools)

agent_chain = prompt | model_with_tools

agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=tools,
    verbose=True
)
```

---

## 🧪 Step 10: Add Memory Wrapper

```python id="lab15_code8"
from langchain_core.runnables.history import RunnableWithMessageHistory

conversational_agent = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)
```

---

## 🧪 Step 11: Guardrails

```python id="lab15_code9"
def sanitize_input(text: str) -> str:
    return text.strip()

def filter_output(text: str) -> str:
    if "illegal" in text.lower():
        return "Response blocked"
    return text
```

---

## 🧪 Step 12: FastAPI Integration

```python id="lab15_code10"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RequestModel(BaseModel):
    query: str
    session_id: str
```

---

## 🧪 Step 13: Streaming Endpoint

```python id="lab15_code11"
from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat(request: RequestModel):

    async def generator():
        clean_query = sanitize_input(request.query)

        async for chunk in conversational_agent.astream(
            {"input": clean_query},
            config={"configurable": {"session_id": request.session_id}}
        ):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")
```

---

## 🧪 Step 14: Run Application

```bash id="lab15_run"
uvicorn app:app --reload
```

---

## 🧪 Step 15: Test System

```bash id="lab15_test"
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"query": "What is LangChain?", "session_id": "user1"}'
```

---

## 📤 Expected Behavior

```text id="lab15_out"
- Maintains conversation
- Retrieves knowledge
- Uses tools when needed
- Streams response
- Applies guardrails
```

---

## 🧠 Final Key Takeaways

* You built a **complete AI system**
* Combined:

  * RAG
  * Agents
  * Memory
  * Streaming
  * Guardrails
  * API

---

## 🧪 Final Exercises (Real-World Challenges)

1. Add:

   * authentication layer
2. Replace FAISS with:

   * Azure AI Search
3. Add logging + monitoring
4. Deploy to Azure

---

## 📚 References

* LangChain Docs: [https://python.langchain.com/docs/](https://python.langchain.com/docs/)
* FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

```

---

# 🎉 Congratulations

You’ve now built:

## 🚀 A Production-Ready AI System

You can now:
- Build **enterprise copilots**
- Create **AI SaaS products**
- Design **scalable LLM systems**