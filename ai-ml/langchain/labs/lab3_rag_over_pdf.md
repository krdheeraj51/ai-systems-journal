# Lab 3 — RAG over a PDF with Azure OpenAI

## Objective

Learn how to:

* Load and split a PDF into searchable text chunks.
* Generate embeddings using Azure OpenAI’s embedding model.
* Store chunks in a FAISS vector database.
* Query the vector DB to retrieve relevant chunks.
* Pass those chunks into a prompt so the model answers **grounded in your document**.

By the end, you’ll be able to ask questions about your own PDF and get relevant, context-based answers.

---

## Step 0 — Prereqs

From Labs 1 & 2 you should already have:

* Python venv + packages installed.
* Azure OpenAI **chat** and **embedding** deployments.

If not, install:

```bash
pip install -U langchain langchain-openai langchain-core langchain-community langchain-text-splitters faiss-cpu pypdf
```

Also, set environment variables (adjust for your resource):

```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-06-01"
export AZURE_OPENAI_CHAT_DEPLOYMENT="your-chat-deployment-name"  # e.g. gpt-4o-mini
export AZURE_OPENAI_EMBED_DEPLOYMENT="your-embedding-deployment-name"  # e.g. text-embedding-3-large
```

---

## Step 1 — Prepare your PDF

1. Create a folder `data/`.
2. Put any PDF in it — for testing, pick something text-heavy (e.g., a whitepaper, a user manual).
3. Name it `mydoc.pdf`.

---

## Step 2 — Create `lab3_rag_pdf.py`

```python
import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1) Embedding model
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# 2) Chat model
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0.1,  # factual answers
)

# 3) Load PDF
print("Loading PDF...")
loader = PyPDFLoader("data/mydoc.pdf")
docs = loader.load()

# 4) Split into chunks for embedding
print("Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(docs)

# 5) Create FAISS vector store
print("Creating FAISS vector DB...")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  # retrieve top 4 chunks

# 6) Prompt template for RAG
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use ONLY the provided context to answer. If unsure, say 'I don't know'."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

# 7) Function to format retrieved docs
def format_docs(docs):
    return "\n\n".join(f"[Page {d.metadata.get('page', '?')}]\n{d.page_content}" for d in docs)

# 8) Assemble RAG chain: retrieve → format → prompt → LLM
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 9) Test with a question
while True:
    q = input("\nAsk a question about the PDF (or 'exit'): ")
    if q.lower().strip() == "exit":
        break
    answer = rag_chain.invoke(q)
    print("\nAnswer:\n", answer.content)
```

---

## Step 3 — Run it

```bash
python lab3_rag_pdf.py
```

Example interaction:

```
Loading PDF...
Splitting into chunks...
Creating FAISS vector DB...

Ask a question about the PDF (or 'exit'): What are the main recommendations in the document?

Answer:
The document recommends implementing a phased rollout, conducting regular stakeholder reviews, and establishing clear success metrics before scaling the initiative.
```

---

## Step 4 — How it works

1. **Loader**: `PyPDFLoader` extracts text from each page.
2. **Splitter**: Splits text into chunks so embeddings capture coherent meaning.
3. **Embedding model**: Converts each chunk into a vector using Azure OpenAI embeddings.
4. **Vector store (FAISS)**: Stores embeddings for similarity search.
5. **Retriever**: Finds the most relevant chunks for a given query.
6. **Prompt**: Injects retrieved context into the LLM prompt.
7. **LLM**: Generates an answer **grounded in the retrieved context**.

---

## Step 5 — Experiment

* Change `chunk_size` from 1000 → 500 and see if answers improve.
* Adjust `search_kwargs={"k": 6}` to retrieve more chunks.
* Try a different PDF — e.g., your company’s onboarding manual.
* Swap FAISS for a cloud vector DB (e.g., Azure AI Search) for scale.

---

## Step 6 — Checklist

* [ ] I can load and split a PDF.
* [ ] I can embed chunks with Azure OpenAI embeddings.
* [ ] I can store/retrieve chunks from FAISS.
* [ ] I can pass retrieved context to the LLM and get grounded answers.

