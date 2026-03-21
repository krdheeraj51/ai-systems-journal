# 🧪 Lab 12: Caching, Cost Optimization & Performance Tuning

## 🎯 Objective
- Reduce API costs using caching
- Improve response speed
- Optimize LangChain pipelines for production
- Understand performance bottlenecks

---

## 📚 Concepts Covered
- LLM caching
- Embedding caching
- Response reuse strategies
- Token optimization
- Batch processing
- Efficient retrieval design

---

## ⚙️ Prerequisites
- Lab 1–11 completed
- Working RAG + Agent pipeline
- Azure OpenAI setup ready

---

## 🧠 Step 1: Why Optimization Matters?

Without optimization:
- ❌ High API cost
- ❌ Slow response time
- ❌ Poor scalability

With optimization:
- ✅ Faster responses
- ✅ Lower cost
- ✅ Better UX

---

## 🧪 Step 2: Enable LLM Caching

```python id="lab12_code1"
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache

set_llm_cache(InMemoryCache())
````

👉 Now repeated queries won't call the API again.

---

## 🧪 Step 3: Test Caching

```python id="lab12_code2"
chain.invoke({"topic": "LangChain"})
chain.invoke({"topic": "LangChain"})  # Cached response
```

👉 Second call = ⚡ instant

---

## 🧠 Step 4: Persistent Caching (Production)

```python id="lab12_code3"
from langchain.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))
```

👉 Benefits:

* Cache survives restarts
* Useful in real applications

---

## 🧪 Step 5: Embedding Optimization

```python id="lab12_code4"
# Avoid recomputing embeddings
vectorstore = FAISS.from_documents(docs, embeddings)

# Save locally
vectorstore.save_local("faiss_index")
```

Load later:

```python id="lab12_code5"
vectorstore = FAISS.load_local("faiss_index", embeddings)
```

---

## 🧠 Step 6: Reduce Token Usage (VERY IMPORTANT)

### Bad Prompt:

```text
Explain everything about LangChain in detail with history...
```

### Optimized Prompt:

```text
Explain LangChain in 3 concise points
```

👉 Fewer tokens = lower cost

---

## 🧪 Step 7: Limit Context Size

```python id="lab12_code6"
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}  # reduce context size
)
```

---

## 🧠 Step 8: Batch Processing (Advanced Optimization)

```python id="lab12_code7"
inputs = [
    {"topic": "AI"},
    {"topic": "ML"},
    {"topic": "LangChain"}
]

results = chain.batch(inputs)

print(results)
```

👉 Faster than sequential calls

---

## 🧪 Step 9: Parallel Execution (Reuse from Lab 3)

```python id="lab12_code8"
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel({
    "summary": chain,
    "keywords": another_chain
})
```

---

## 🧠 Step 10: Optimize RAG Retrieval

```python id="lab12_code9"
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3,
        "fetch_k": 5  # retrieve more, return best
    }
)
```

---

## 🧠 Step 11: Cost-Saving Strategy (VERY IMPORTANT)

### Use smaller models when possible:

* Simple tasks → cheaper model
* Complex tasks → powerful model

👉 Example:

* Classification → small model
* Reasoning → GPT-4-level

---

## 🧠 Step 12: Pipeline Optimization Pattern

```python id="lab12_code10"
optimized_chain = (
    preprocess_step
    | cached_chain
    | postprocess_step
)
```

---

## 📤 Expected Outcome

```id="lab12_out"
- Faster responses
- Reduced API calls
- Lower cost
```

---

## 🧠 Key Takeaways

* Caching = biggest cost saver
* Token reduction = direct cost control
* Retrieval tuning = performance boost
* Batch + parallel = speed improvement

---

## 🧪 Exercises

1. Enable SQLite cache and restart app → verify cache persists
2. Compare:

   * k=2 vs k=5 retrieval cost
3. Create:

   * short vs long prompt → compare tokens
4. Add caching to RAG pipeline

---

## 📚 References

* Caching: [https://python.langchain.com/docs/integrations/llm_caching/](https://python.langchain.com/docs/integrations/llm_caching/)
* Performance: [https://python.langchain.com/docs/guides/production/](https://python.langchain.com/docs/guides/production/)

```

---

## 🔥 Where You Are Now

You now understand:
- ⚡ Performance tuning
- 💰 Cost optimization
- 🧠 Efficient architecture design
