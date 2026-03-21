# 🧪 Lab 6: Advanced RAG (Improving Retrieval Quality & Accuracy)

## 🎯 Objective
- Improve RAG accuracy and relevance
- Optimize chunking strategies
- Tune retrieval parameters (top-k, filtering)
- Enhance prompts for better grounded answers
- Build a more production-ready RAG pipeline

---

## 📚 Concepts Covered
- Chunking strategies (critical for RAG)
- Retrieval tuning (top-k, similarity)
- Metadata filtering
- Context formatting techniques
- Prompt optimization for RAG
- Reducing hallucinations

---

## ⚙️ Prerequisites
- Lab 5 completed (basic RAG pipeline)
- Working FAISS vector store
- Understanding of embeddings and retriever

---

## 🧠 Step 1: Why Basic RAG Fails

Common issues:
- ❌ Wrong chunks retrieved
- ❌ Too much irrelevant context
- ❌ Hallucinated answers
- ❌ Missing key information

👉 Solution = Optimize every stage

---

## ✂️ Step 2: Advanced Chunking Strategy

Instead of naive chunking:

```python id="lab6_code1"
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,     # smaller chunks = better precision
    chunk_overlap=80    # overlap preserves context
)

docs = splitter.split_documents(documents)
````

👉 Rule of thumb:

* Smaller chunks → better retrieval
* Overlap → avoids context loss

---

## 🧪 Step 3: Add Metadata (VERY IMPORTANT)

```python id="lab6_code2"
for i, doc in enumerate(docs):
    doc.metadata["source"] = "sample.txt"
    doc.metadata["chunk_id"] = i
```

👉 Metadata helps:

* Filtering
* Debugging
* Traceability

---

## 🗄️ Step 4: Improved Retriever (Top-K Tuning)

```python id="lab6_code3"
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}  # try 3–5
)
```

👉 Too low:

* Misses information

👉 Too high:

* Adds noise

---

## 🔍 Step 5: Metadata Filtering

```python id="lab6_code4"
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3,
        "filter": {"source": "sample.txt"}
    }
)
```

---

## 🧠 Step 6: Better Context Formatting

```python id="lab6_code5"
def format_docs(docs):
    return "\n\n".join(
        f"[Source: {doc.metadata.get('chunk_id')}]\n{doc.page_content}"
        for doc in docs
    )
```

👉 Helps model:

* Understand structure
* Reference sources

---

## 🧪 Step 7: Prompt Optimization (CRITICAL)

```python id="lab6_code6"
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
""")
```

👉 This reduces hallucination significantly.

---

## 🧪 Step 8: Full Advanced RAG Pipeline

```python id="lab6_code7"
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": lambda x: x
    }
    | prompt
    | model
    | StrOutputParser()
)

response = rag_chain.invoke("Explain LangChain components")
print(response)
```

---

## 🔥 Step 9: Add Debugging Layer (Optional but Powerful)

```python id="lab6_code8"
docs = retriever.invoke("Explain LangChain")

for d in docs:
    print(d.metadata, d.page_content[:100])
```

👉 Always inspect retrieved docs!

---

## 🧠 Step 10: Key Optimization Strategies

### ✅ Chunking

* 300–500 size
* 50–100 overlap

### ✅ Retrieval

* k = 3–5
* Use filters when needed

### ✅ Prompt

* Force grounding
* Avoid hallucination

---

## 📤 Expected Output

```id="lab6_out"
LangChain consists of components such as prompts, models, chains, and retrievers...
```

---

## 🧠 Key Takeaways

* RAG quality depends more on **retrieval than model**
* Chunking is the **#1 factor**
* Prompt design reduces hallucination
* Metadata is essential for production systems

---

## 🧪 Exercises

1. Change:

   * chunk_size = 1000 → observe degradation
2. Increase k = 10 → observe noise
3. Add multiple documents and filter by source
4. Modify prompt to include citations

---

## 📚 References

* Advanced RAG Guide: [https://python.langchain.com/docs/use_cases/question_answering/](https://python.langchain.com/docs/use_cases/question_answering/)
* Text Splitters: [https://python.langchain.com/docs/modules/data_connection/document_transformers/](https://python.langchain.com/docs/modules/data_connection/document_transformers/)

```

---

## 🔥 Where You Are Now

You now have:
- A **production-ready RAG foundation**
- Understanding of **what makes RAG actually work**

