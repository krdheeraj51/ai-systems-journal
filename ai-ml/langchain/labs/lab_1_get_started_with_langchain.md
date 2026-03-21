# ✅ Lab 1: Getting Started with LangChain v0.2 + Azure OpenAI (LCEL Basics)

````markdown
# 🧪 Lab 1: Introduction to LangChain v0.2 + Azure OpenAI using LCEL

## 🎯 Objective
- Set up LangChain v0.2 with Azure OpenAI
- Understand LCEL (LangChain Expression Language)
- Build your first LLM chain using modern LangChain patterns

---

## 📚 Concepts Covered
- LangChain v0.2 architecture
- LCEL (LangChain Expression Language)
- Chat models in LangChain
- Runnable pipeline (`|` operator)
- Azure OpenAI integration (LangChain way)

---

## ⚙️ Prerequisites
- Python 3.9+
- Azure OpenAI resource (already created)
- Basic Python knowledge

---

## 📦 Installation

```bash
pip install langchain langchain-openai python-dotenv
````

---

## 🔐 Environment Variables

Create a `.env` file:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

---

## 🧠 Step 1: Understand LCEL

LangChain v0.2 replaces older chains with **LCEL (Runnable pipelines)**.

Example idea:

```
Input → Prompt → Model → Output
```

In LCEL:

```python
chain = prompt | model
```

---

## 🧪 Step 2: Create Your First Chain

```python
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Azure OpenAI Chat Model
model = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

# Create Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "Explain {topic} in simple terms.")
])

# Create LCEL Chain
chain = prompt | model

# Run the chain
response = chain.invoke({"topic": "LangChain"})

print(response.content)
```

---

## 🔍 Step 3: What Just Happened?

* `ChatPromptTemplate` → formats input
* `AzureChatOpenAI` → calls Azure model
* `|` operator → connects components (LCEL)
* `.invoke()` → executes the pipeline

---

## 📤 Expected Output

```
LangChain is a framework that helps developers build applications using language models...
```

---

## 🧩 Step 4: Add Output Parsing (Optional Intro)

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()

response = chain.invoke({"topic": "LCEL"})
print(response)
```

---

## 🧠 Key Takeaways

* LCEL is the **core of modern LangChain**
* Everything is a **Runnable**
* Pipelines are built using `|`
* `.invoke()` is the standard execution method

---

## 🧪 Exercises

1. Modify prompt to explain topics in **bullet points**
2. Change system message to act like a **teacher**
3. Pass multiple topics and test responses

---

## 📚 References

* LangChain Docs (LCEL): [https://python.langchain.com/docs/expression_language/](https://python.langchain.com/docs/expression_language/)
* Azure OpenAI Docs: [https://learn.microsoft.com/en-us/azure/ai-services/openai/](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

```

---

## ⚠️ Important Note (About v0.2 in Production)

LangChain v0.2+:
- ✅ LCEL is **production-ready**
- ✅ Legacy chains (`LLMChain`, etc.) are **deprecated**
- ✅ Recommended for **new applications**
- ⚠️ Some APIs still evolving → best practice is:
  - Use **langchain-core + langchain-openai**
  - Avoid older abstractions

---
