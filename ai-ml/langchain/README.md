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

Let’s go over the **main components**:

| Component  | What It Does                                                 | Analogy                       |
| ---------- | ------------------------------------------------------------ | ----------------------------- |
| `LLM`      | The actual language model (e.g., Azure OpenAI, GPT-4, etc.)  | The brain                     |
| `Prompt`   | A template for asking the LLM something                      | The question sheet            |
| `LLMChain` | Combines a prompt + LLM to create a response                 | A single task                 |
| `Tool`     | A function the agent can call (e.g., calculator, web search) | A skill the agent can use     |
| `Agent`    | Chooses what steps to take and which tools to use            | A smart assistant             |
| `Memory`   | Stores past interactions or facts                            | The agent’s short-term memory |
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





