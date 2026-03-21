# 🧪 Lab 5: RAG Fundamentals (Document Loading → Embeddings → Retrieval)

## 🎯 Objective
- Understand the RAG architecture
- Load and process documents
- Generate embeddings using Azure OpenAI
- Perform semantic retrieval
- Build your first RAG pipeline using LCEL

---

## 📚 Concepts Covered
- What is RAG?
- Document Loaders
- Text Splitters
- Embeddings
- Vector Stores (FAISS)
- Retriever abstraction
- LCEL-based RAG pipeline

---

## ⚙️ Prerequisites
- Lab 1–4 completed
- Azure OpenAI setup ready
- Basic understanding of embeddings

---

## 🧠 Step 1: What is RAG?

RAG = Combine:
- LLM knowledge ❌ (limited)
- External data ✅ (documents)

Pipeline:

User Query → Retrieve Docs → LLM → Answer

---

## 📦 Step 2: Install Required Packages

```bash
pip install langchain faiss-cpu tiktoken
````

---

## 📄 Step 3: Load Documents

```python id="lab5_code1"
from langchain_community.document_loaders import TextLoader

loader = TextLoader("sample.txt")  # create a sample file
documents = loader.load()

print(documents[0].page_content)
```

---

## ✂️ Step 4: Split Documents

```python id="lab5_code2"
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

print(len(docs))
```

---

## 🧠 Step 5: Create Embeddings (Azure OpenAI)

```python id="lab5_code3"
from langchain_openai import AzureOpenAIEmbeddings
import os

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="your-embedding-deployment",
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
```

---

## 🗄️ Step 6: Store in Vector DB (FAISS)

```python id="lab5_code4"
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(docs, embeddings)

retriever = vectorstore.as_retriever()
```

---

## 🔍 Step 7: Test Retrieval

```python id="lab5_code5"
query = "What is LangChain?"

results = retriever.invoke(query)

for r in results:
    print(r.page_content)
```

---

## 🧪 Step 8: Build Basic RAG Chain (LCEL)

```python id="lab5_code6"
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser

model = AzureChatOpenAI(
    azure_deployment="your-chat-deployment",
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the context below:

Context:
{context}

Question:
{question}
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": lambda x: x
    }
    | prompt
    | model
    | StrOutputParser()
)

response = rag_chain.invoke("What is LangChain?")
print(response)
```

---

## 🔥 Step 9: What’s Happening?

* Retriever → fetches relevant chunks
* format_docs → prepares context
* Prompt → injects context
* Model → generates answer

---

## 📤 Expected Output

```id="lab5_out"
LangChain is a framework used to build applications with language models...
```

---

## 🧠 Key Takeaways

* RAG = Retrieval + Generation
* Embeddings power semantic search
* Chunking is critical
* LCEL makes RAG pipelines clean

---

## 🧪 Exercises

1. Change chunk_size and observe results
2. Ask unrelated questions → observe hallucination
3. Add more documents and test retrieval quality

---

## 📚 References

* RAG Concept: [https://python.langchain.com/docs/use_cases/question_answering/](https://python.langchain.com/docs/use_cases/question_answering/)
* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Embeddings: [https://platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings)

```

---

## 🔥 Where You Are Now

You’ve built:
- Your **first real-world AI system**
- A working **RAG pipeline**