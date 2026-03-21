# 🧪 Lab 7: Conversational RAG (Memory + Chat History)

## 🎯 Objective
- Build a conversational RAG system
- Maintain chat history across queries
- Improve retrieval using conversation context
- Use LangChain v0.2 memory patterns (modern approach)

---

## 📚 Concepts Covered
- Conversational RAG
- Chat history handling
- RunnableWithMessageHistory
- Context-aware retrieval
- Session-based memory

---

## ⚙️ Prerequisites
- Lab 5 & 6 completed (RAG + Advanced RAG)
- Working retriever + vectorstore
- Azure OpenAI model setup

---

## 🧠 Step 1: Why Conversational RAG?

Basic RAG:
- ❌ Each query is independent

Conversational RAG:
- ✅ Understands follow-up questions
- ✅ Maintains context
- ✅ More natural interaction

---

## 🧪 Step 2: Chat History Storage

```python id="lab7_code1"
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
````

---

## 🧠 Step 3: Modify Prompt to Include History

```python id="lab7_code2"
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use context to answer."),
    ("placeholder", "{chat_history}"),
    ("user", "{question}")
])
```

---

## 🧪 Step 4: Context-Aware Retrieval

We enhance retrieval using conversation.

```python id="lab7_code3"
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": lambda x: x["question"]
    }
    | prompt
    | model
    | StrOutputParser()
)
```

---

## 🧪 Step 5: Add Message History Wrapper

```python id="lab7_code4"
from langchain_core.runnables.history import RunnableWithMessageHistory

conversational_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)
```

---

## 🧪 Step 6: Invoke with Session

```python id="lab7_code5"
config = {"configurable": {"session_id": "user_1"}}

response1 = conversational_chain.invoke(
    {"question": "What is LangChain?"},
    config=config
)

print(response1)

response2 = conversational_chain.invoke(
    {"question": "What are its components?"},
    config=config
)

print(response2)
```

---

## 🔥 Step 7: What Just Happened?

* Chat history stored per session
* Follow-up questions use previous context
* System behaves like real assistant

---

## 📤 Expected Behavior

```id="lab7_out"
Q1 → "What is LangChain?"
→ Answer

Q2 → "What are its components?"
→ Uses previous answer context automatically
```

---

## 🧠 Step 8: Improve Prompt (Production Pattern)

```python id="lab7_code6"
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an AI assistant.

Use the provided context and chat history.
If unsure, say "I don't know".
"""),
    ("placeholder", "{chat_history}"),
    ("user", "Context:\n{context}\n\nQuestion:\n{question}")
])
```

---

## 🧠 Step 9: Key Design Insight

👉 Two contexts now:

1. Retrieved documents
2. Chat history

Both influence answer quality.

---

## 🧠 Key Takeaways

* Conversational RAG = RAG + Memory
* Session-based memory is essential
* RunnableWithMessageHistory = modern approach
* Enables real chatbot behavior

---

## 🧪 Exercises

1. Create multiple sessions:

   * user_1
   * user_2
2. Clear history manually and observe behavior
3. Add limit to chat history (last 3 messages only)

---

## 📚 References

* Conversational RAG: [https://python.langchain.com/docs/use_cases/question_answering/chat_history/](https://python.langchain.com/docs/use_cases/question_answering/chat_history/)
* Memory: [https://python.langchain.com/docs/expression_language/how_to/message_history/](https://python.langchain.com/docs/expression_language/how_to/message_history/)

```

---

## 🔥 Where You Are Now

You’ve built:
- A **chat-based RAG assistant**
- With **memory + context awareness**
