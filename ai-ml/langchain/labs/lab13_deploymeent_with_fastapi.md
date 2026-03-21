# 🧪 Lab 13: Deployment with FastAPI (LangChain + Azure OpenAI)

## 🎯 Objective
- Convert LangChain pipeline into an API
- Serve RAG/Agent system via FastAPI
- Handle requests and responses
- Prepare for cloud deployment (Azure-ready)

---

## 📚 Concepts Covered
- FastAPI basics
- API endpoints for LLM apps
- Request/response modeling
- Integrating LangChain with web frameworks
- Async API handling
- Production architecture basics

---

## ⚙️ Prerequisites
- Lab 1–12 completed
- Working RAG or Agent pipeline
- Python environment ready

---

## 📦 Step 1: Install Dependencies

```bash
pip install fastapi uvicorn
````

---

## 🧠 Step 2: Basic FastAPI App

```python id="lab13_code1"
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "LangChain API is running"}
```

Run server:

```bash
uvicorn main:app --reload
```

---

## 🧪 Step 3: Define Request Model

```python id="lab13_code2"
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
```

---

## 🧪 Step 4: Integrate LangChain RAG

```python id="lab13_code3"
@app.post("/rag")
def rag_endpoint(request: QueryRequest):
    response = rag_chain.invoke(request.query)
    return {"response": response}
```

---

## 🧪 Step 5: Async Endpoint (Recommended)

```python id="lab13_code4"
@app.post("/rag-async")
async def rag_async(request: QueryRequest):
    response = await rag_chain.ainvoke(request.query)
    return {"response": response}
```

---

## 🧪 Step 6: Agent Endpoint

```python id="lab13_code5"
@app.post("/agent")
async def agent_endpoint(request: QueryRequest):
    response = await agent_executor.ainvoke({
        "input": request.query
    })
    return {"response": response}
```

---

## 🧠 Step 7: Streaming API (Advanced)

```python id="lab13_code6"
from fastapi.responses import StreamingResponse

@app.post("/stream")
async def stream_endpoint(request: QueryRequest):

    async def generator():
        async for chunk in rag_chain.astream(request.query):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")
```

---

## 🧠 Step 8: Project Structure (Production)

```text id="lab13_structure"
project/
│
├── app.py
├── chains/
│   ├── rag.py
│   ├── agent.py
│
├── models/
│   ├── request.py
│
├── utils/
│   ├── config.py
│
├── .env
```

---

## 🧠 Step 9: Environment Handling

```python id="lab13_code7"
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
```

---

## 🧠 Step 10: Production Best Practices

### ✅ Use:

* async endpoints
* environment variables
* modular structure

### ❌ Avoid:

* hardcoding keys
* large synchronous calls
* mixing logic in one file

---

## 🧪 Step 11: Test API

Using curl:

```bash
curl -X POST http://127.0.0.1:8000/rag \
-H "Content-Type: application/json" \
-d '{"query": "What is LangChain?"}'
```

---

## 📤 Expected Output

```json id="lab13_out"
{
  "response": "LangChain is a framework..."
}
```

---

## 🧠 Step 12: Azure Deployment Readiness

This API can be deployed to:

* Azure App Service
* Azure Container Apps
* Docker containers

---

## 🧠 Key Takeaways

* FastAPI turns your LangChain into a service
* Async = scalable APIs
* Streaming = real-time UX
* Modular design = production-ready

---

## 🧪 Exercises

1. Add endpoint:

   * /chat (with memory)
2. Add validation:

   * reject empty queries
3. Add logging:

   * print request + response
4. Deploy locally and test with Postman

---

## 📚 References

* FastAPI Docs: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* LangChain Deployment: [https://python.langchain.com/docs/guides/production/](https://python.langchain.com/docs/guides/production/)

```

---

## 🔥 Where You Are Now

You can now:
- Build **real APIs for AI systems**
- Integrate with:
  - frontend apps
  - mobile apps
  - enterprise systems

This is **true production capability** 🚀