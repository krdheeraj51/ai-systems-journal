# 🧪 Lab 16: Document Loaders (Core + Multiple Sources)

## 🎯 Objective
- Understand how LangChain loads different data sources
- Work with multiple document loaders
- Prepare documents for RAG pipelines

---

## 📚 Concepts Covered
- Document abstraction in LangChain
- TextLoader
- PyPDFLoader
- CSVLoader
- WebBaseLoader
- Metadata handling

---

## ⚙️ Prerequisites
- Lab 5 completed (basic RAG)
- Python environment ready

---

## 🧠 Step 1: What is a Document in LangChain?

Each document contains:
- `page_content` → actual text
- `metadata` → source info

Example:
```python id="lab16_doc_example"
{
  "page_content": "LangChain is a framework...",
  "metadata": {"source": "file.txt"}
}
````

---

## 📦 Step 2: Install Required Packages

```bash
pip install langchain-community pypdf
```

---

## 🧪 Step 3: Load Text File

```python id="lab16_code1"
from langchain_community.document_loaders import TextLoader

loader = TextLoader("sample.txt")
documents = loader.load()

print(documents[0].page_content)
print(documents[0].metadata)
```

---

## 🧪 Step 4: Load PDF File

```python id="lab16_code2"
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("sample.pdf")
documents = loader.load()

print(len(documents))  # pages
```

---

## 🧪 Step 5: Load CSV Data

```python id="lab16_code3"
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path="data.csv")
documents = loader.load()

print(documents[0].page_content)
```

---

## 🧪 Step 6: Load Web Content

```python id="lab16_code4"
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")
documents = loader.load()

print(documents[0].page_content[:500])
```

---

## 🧠 Step 7: Combine Multiple Sources

```python id="lab16_code5"
all_docs = []

all_docs.extend(TextLoader("sample.txt").load())
all_docs.extend(PyPDFLoader("sample.pdf").load())

print(len(all_docs))
```

---

## 🧠 Step 8: Add Custom Metadata

```python id="lab16_code6"
for doc in all_docs:
    doc.metadata["project"] = "langchain_lab"
```

---

## 🧠 Step 9: Why Metadata Matters

Metadata helps:

* filtering
* debugging
* source attribution
* multi-document systems

---

## 📤 Expected Output

```text id="lab16_out"
- Documents loaded from multiple sources
- Each document has content + metadata
```

---

## 🧠 Key Takeaways

* Loaders convert raw data → LangChain documents
* Metadata is critical for production
* Multiple sources can be combined easily

---

## 🧪 Exercises

1. Load:

   * 2 PDFs + 1 text file
2. Add metadata:

   * source type (pdf/text)
3. Print:

   * first 100 characters of each doc
4. Try:

   * loading a website article

---

## 📚 References

* Document Loaders: [https://python.langchain.com/docs/modules/data_connection/document_loaders/](https://python.langchain.com/docs/modules/data_connection/document_loaders/)

```

---

## 🔥 What’s Next (Lab 17 Preview)

Next lab will go deeper into:

👉 **Text Splitters (RecursiveCharacterTextSplitter — Most Important One)**

This is where:
- RAG quality = decided 🔥
