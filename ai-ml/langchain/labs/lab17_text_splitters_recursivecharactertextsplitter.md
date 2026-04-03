# 🧪 Lab 17: Text Splitters (RecursiveCharacterTextSplitter Deep Dive)

## 🎯 Objective
- Understand why text splitting is critical
- Learn how RecursiveCharacterTextSplitter works
- Optimize chunk size and overlap
- Prepare high-quality chunks for RAG

---

## 📚 Concepts Covered
- Why chunking is needed
- RecursiveCharacterTextSplitter
- Chunk size vs overlap tradeoff
- Semantic vs naive splitting
- Chunk quality impact on retrieval

---

## ⚙️ Prerequisites
- Lab 16 completed (Document Loaders)
- Basic understanding of RAG

---

## 🧠 Step 1: Why Text Splitting?

LLMs cannot process large documents directly:
- ❌ Token limits
- ❌ Poor retrieval if chunks are too large

👉 Solution:
- Split documents into **smaller meaningful chunks**

---

## 🧪 Step 2: Basic Text Splitter

```python id="lab17_code1"
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
````

---

## 🧪 Step 3: Split Documents

```python id="lab17_code2"
docs = splitter.split_documents(documents)

print(len(docs))
print(docs[0].page_content)
```

---

## 🧠 Step 4: How Recursive Splitting Works

It splits using priority:

1. Paragraphs (`\n\n`)
2. Lines (`\n`)
3. Spaces (` `)
4. Characters

👉 Goal: preserve meaning as much as possible

---

## 🧪 Step 5: Experiment with Chunk Size

```python id="lab17_code3"
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)
```

Try:

* 200 → more precise
* 1000 → more context but noisy

---

## 🧠 Step 6: Overlap Importance

```python id="lab17_code4"
chunk_overlap=100
```

👉 Why overlap?

* Prevents context loss between chunks
* Helps answer boundary questions

---

## 🧪 Step 7: Visualize Chunking

```python id="lab17_code5"
for i, doc in enumerate(docs[:3]):
    print(f"Chunk {i}:")
    print(doc.page_content[:200])
    print("------")
```

---

## 🧠 Step 8: Add Metadata to Chunks

```python id="lab17_code6"
for i, doc in enumerate(docs):
    doc.metadata["chunk_id"] = i
```

---

## 🧪 Step 9: Split Raw Text (Alternative)

```python id="lab17_code7"
text = "LangChain is a framework..." * 100

chunks = splitter.split_text(text)

print(len(chunks))
```

---

## 🧠 Step 10: Best Practices

### ✅ Recommended:

* chunk_size = 300–500
* overlap = 50–100

### ❌ Avoid:

* very large chunks (>1000)
* zero overlap

---

## 📤 Expected Output

```text id="lab17_out"
- Documents split into meaningful chunks
- Each chunk manageable for embeddings
```

---

## 🧠 Key Takeaways

* Chunking is **more important than model choice**
* Recursive splitter preserves semantic structure
* Overlap improves context continuity
* Smaller chunks = better retrieval precision

---

## 🧪 Exercises

1. Try:

   * chunk_size = 100, 300, 800 → compare results
2. Remove overlap → observe loss in context
3. Print chunk boundaries → analyze splitting
4. Add metadata:

   * chunk position

---

## 📚 References

* Text Splitters: [https://python.langchain.com/docs/modules/data_connection/document_transformers/](https://python.langchain.com/docs/modules/data_connection/document_transformers/)

```

---

## 🔥 What’s Next (Lab 18 Preview)

Now we go beyond basic splitting:

👉 **Advanced Text Splitters**
- CharacterTextSplitter vs Recursive
- Token-based splitting (VERY important)
- When to use which
