# Lab 1 — Set Up & Say Hello (LangChain + Azure OpenAI)

## Objective

Get your environment ready and make your **first successful LangChain call** to **Azure OpenAI**. Along the way you’ll learn:

* How Azure OpenAI + LangChain fit together (client, model, prompt, response).
* How to configure **endpoint, API key, API version, deployment name**.
* How to invoke the model with both **plain text** and **chat messages**.
* How to **stream** tokens and control behavior with **temperature**.

---

## Step 0 — What you need (once per machine)

1. **An Azure subscription** with access to **Azure OpenAI**.
2. **An Azure OpenAI resource** (in the Azure Portal). Note its:

   * **Endpoint** (looks like `https://<your-resource>.openai.azure.com`)
   * **API version** (e.g., `2024-06-01`)
3. **A chat model deployment** inside that resource.

   * Example deployment name: `gpt-4o-mini` (you can use any deployed chat model; just keep the **deployment name** handy).

> If you don’t have a deployment yet, create one in the Azure OpenAI Studio and copy the **deployment name**.

---

## Step 1 — Create a project folder

```bash
mkdir langchain-azure-lab1
cd langchain-azure-lab1
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

---

## Step 2 — Install packages

```bash
pip install -U langchain langchain-openai langchain-core
```

> These give you LangChain’s core primitives and the Azure OpenAI integration.

---

## Step 3 — Set environment variables

Set these in your shell **before** running code (or put them in a `.env` and load them—keeping secrets out of source control).

**macOS/Linux (bash/zsh):**

```bash
export AZURE_OPENAI_API_KEY="<your-azure-openai-key>"
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-06-01"
export AZURE_OPENAI_CHAT_DEPLOYMENT="<your-chat-deployment-name>"  # e.g. gpt-4o-mini
```

**Windows (PowerShell):**

```powershell
$env:AZURE_OPENAI_API_KEY="<your-azure-openai-key>"
$env:AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
$env:AZURE_OPENAI_API_VERSION="2024-06-01"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT="<your-chat-deployment-name>"  # e.g. gpt-4o-mini
```

---

## Step 4 — Your first script: simple prompt → response

Create `lab1_hello.py`:

```python
import os
from langchain_openai import AzureChatOpenAI

# 1) Create the LLM client pointed at Azure OpenAI
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0.2,  # small creativity; use 0 for deterministic
)

# 2) Send a plain-text prompt (LangChain will wrap as a chat under the hood)
response = llm.invoke("In one sentence, what is LangChain?")
print("=== Plain Text Prompt ===")
print(response.content)

# 3) Send role-based chat messages (system + human)
from langchain_core.messages import SystemMessage, HumanMessage
messages = [
    SystemMessage(content="You are a concise technical explainer."),
    HumanMessage(content="Explain LangChain in 2 short bullet points.")
]
chat_response = llm.invoke(messages)
print("\n=== Chat Messages Prompt ===")
print(chat_response.content)

# 4) Optional: stream tokens (for live UIs / CLIs)
print("\n=== Streaming Demo ===")
for chunk in llm.stream("Write a 12-word tagline about building agents with LangChain and Azure OpenAI."):
    # Each chunk is a partial message; print tokens as they arrive
    print(chunk.content, end="", flush=True)
print()  # newline
```

---

## Step 5 — Run it

```bash
python lab1_hello.py
```

**Expected output (will vary slightly):**

```
=== Plain Text Prompt ===
LangChain is a Python framework for building LLM-powered apps using composable tools.

=== Chat Messages Prompt ===
- A framework to build LLM apps by composing prompts, tools, memory, and chains.
- It standardizes model access and orchestration so you can ship faster.

=== Streaming Demo ===
Build powerful agentic apps with LangChain on Azure—fast, reliable, production-ready.
```

---

## Step 6 — Understand what just happened (key concepts)

* **Model client:** `AzureChatOpenAI` connects LangChain to your Azure OpenAI **deployment**.
* **Config:** You provided `azure_endpoint`, `api_version`, and a **deployment name** (not the model name).
* **Prompts:** You can pass either a **string** or structured **chat messages** (System/Human).
* **Temperature:** Lower (e.g., `0`) = more deterministic; higher = more creative/varied.
* **Streaming:** `llm.stream(...)` yields partial outputs—great for responsive UIs.

---

## Step 7 — Troubleshooting (quick fixes)

* **`Resource not found` / `404`**
  Check `AZURE_OPENAI_ENDPOINT` and that the **deployment name** matches exactly.

* **`Invalid API version`**
  Ensure `AZURE_OPENAI_API_VERSION` matches one supported by your resource (e.g., `2024-06-01`).

* **`Unauthorized` / `401`**
  Confirm `AZURE_OPENAI_API_KEY` is correct and belongs to the same resource/tenant.

* **`Rate limit` / `429`**
  Add retries/backoff or reduce request rate. For now, just re-run after a pause.

---

## Step 8 — (Optional) Make it a tiny CLI

Create `lab1_cli.py` for quick experiments:

```python
import os, sys
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0.0,
)

prompt = " ".join(sys.argv[1:]) or "Say hello from Azure OpenAI via LangChain."
for chunk in llm.stream(prompt):
    print(chunk.content, end="", flush=True)
print()
```

Run:

```bash
python lab1_cli.py "Give me 3 crisp tips for better prompts."
```

---

## Step 9 — Your mini checklist (confidence booster)

* [ ] I can activate a venv and install packages.
* [ ] I set `AZURE_OPENAI_*` environment variables correctly.
* [ ] `lab1_hello.py` runs and prints three sections (plain, chat, streaming).
* [ ] I understand **deployment name vs. model name**.
* [ ] I know how to adjust **temperature**.

---

<!-- ## Where this leads (preview)

* **Lab 2:** Structured outputs (validated JSON with Pydantic).
* **Lab 3:** RAG over your PDFs with Azure embeddings.
* **Lab 4:** Tool-using agents (calculator, KB lookup).
* **Lab 5:** Multi-agent flows with LangGraph + memory.

If you want, I can spin up **Lab 2** next in the same step-by-step style, still using your **Azure OpenAI** deployments. -->
