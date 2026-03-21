### 🔷 1. What is LangChain?

LangChain is a Python (and JS) framework that helps you **build applications with language models** by connecting:

* LLMs (like OpenAI or Azure OpenAI)
* Prompt templates
* External tools (like calculators, web search, file access)
* Memory (for conversation context)
* And chaining multiple steps together (reasoning, planning)

LangChain is especially helpful for building **Agentic AI** — systems where the LLM can **choose actions**, use **tools**, and work toward a **goal**.

---

### 🔷 2. Key Concepts (building blocks)

Let's go over the **main components**:

| Component  | What It Does                                                 | Analogy                       |
| ---------- | ------------------------------------------------------------ | ----------------------------- |
| `LLM`      | The actual language model (e.g., Azure OpenAI, GPT-4, etc.)  | The brain                     |
| `Prompt`   | A template for asking the LLM something                      | The question sheet            |
| `LLMChain` | Combines a prompt + LLM to create a response                 | A single task                 |
| `Tool`     | A function the agent can call (e.g., calculator, web search) | A skill the agent can use     |
| `Agent`    | Chooses what steps to take and which tools to use            | A smart assistant             |
| `Memory`   | Stores past interactions or facts                            | The agent's short-term memory |
| `Chain`    | A sequence of steps or tasks                                 | A workflow or pipeline        |

---
### What is difference between promptTemplate and ChatPromptTemplate? 

`PromptTemplate` is used for single-turn prompts, while `ChatPromptTemplate` is designed for multi-turn conversations, allowing you to define system, user, and assistant messages separately.

### What is difference between ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate?

`ChatPromptTemplate` is a container for multiple message templates, while `SystemMessagePromptTemplate` and `HumanMessagePromptTemplate` are specific types of message templates used within a `ChatPromptTemplate` to define system and user messages, respectively.

### What is difference between LLMChain and ChatLLMChain?   

`LLMChain` is a general chain that can work with any prompt, while `ChatLLMChain` is specifically designed for use with `ChatPromptTemplate`, allowing for multi-turn conversations.

### What is difference between Agent and Tool?

An `Agent` is a higher-level construct that can choose which `Tool` to use based on the context, while a `Tool` is a specific function or capability that the agent can call to perform a task (e.g., calculator, web search).

### What is difference between Agent and Chain?

An `Agent` is a decision-maker that can choose which `Chain` or `Tool` to use based on the context, while a `Chain` is a predefined sequence of steps or tasks that can be executed by the agent.

---

## 📚 Labs Overview

| Lab # | Lab Title | View |
|-------|-----------|------|
| 1 | LangChain Basics: Installation & Setup | [Lab 1](./labs/lab-01-basics) |
| 2 | Building Your First LLM Chain | [Lab 2](./labs/lab-02-first-chain) |
| 3 | Prompt Templates & Customization | [Lab 3](./labs/lab-03-prompt-templates) |
| 4 | Chat Models & Conversations | [Lab 4](./labs/lab-04-chat-models) |
| 5 | Memory Management | [Lab 5](./labs/lab-05-memory) |
| 6 | Tools & Function Calling | [Lab 6](./labs/lab-06-tools) |
| 7 | Building Agents | [Lab 7](./labs/lab-07-agents) |
| 8 | Agent Tools & Executors | [Lab 8](./labs/lab-08-agent-tools) |
| 9 | Chains & Sequential Workflows | [Lab 9](./labs/lab-09-chains) |
| 10 | Retrieval Augmented Generation (RAG) | [Lab 10](./labs/lab-10-rag) |
| 11 | Document Loading & Processing | [Lab 11](./labs/lab-11-document-loading) |
| 12 | Vector Stores & Embeddings | [Lab 12](./labs/lab-12-vector-stores) |
| 13 | Advanced Agent Patterns | [Lab 13](./labs/lab-13-advanced-agents) |
| 14 | Error Handling & Debugging | [Lab 14](./labs/lab-14-error-handling) |
| 15 | Building Production Applications | [Lab 15](./labs/lab-15-production) |