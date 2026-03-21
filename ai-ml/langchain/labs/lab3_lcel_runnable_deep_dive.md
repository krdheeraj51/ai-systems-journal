# 🧪 Lab 3: LCEL Runnables Deep Dive (Branching, Parallel, Composition)

## 🎯 Objective
- Master advanced LCEL concepts
- Learn branching, parallel execution, and data transformation
- Build dynamic pipelines like production systems

---

## 📚 Concepts Covered
- RunnableLambda
- RunnableSequence
- RunnableParallel
- RunnableBranch (conditional logic)
- Data transformation inside chains
- Pipeline thinking (VERY IMPORTANT)

---

## ⚙️ Prerequisites
- Lab 1 & Lab 2 completed
- Understanding of:
  - prompt | model | parser
  - JSON/Pydantic parsing

---

## 🧠 Step 1: What are Runnables?

In LangChain v0.2:
👉 Everything is a **Runnable**

Examples:
- Prompt → Runnable
- Model → Runnable
- Parser → Runnable
- Custom function → Runnable

---

## 🧪 Step 2: RunnableLambda (Custom Logic)

You can inject Python logic inside LCEL.

```python id="lab3_code1"
from langchain_core.runnables import RunnableLambda

def to_upper(data):
    return {"topic": data["topic"].upper()}

transform = RunnableLambda(to_upper)
````

---

## 🔗 Step 3: Combine with Existing Chain

```python id="lab3_code2"
chain = transform | prompt | model

response = chain.invoke({"topic": "langchain"})
print(response.content)
```

---

## 🧪 Step 4: RunnableParallel (Run Tasks Together)

```python id="lab3_code3"
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel({
    "summary": prompt | model | StrOutputParser(),
    "keywords": (
        ChatPromptTemplate.from_template("Give 5 keywords about {topic}")
        | model
        | StrOutputParser()
    )
})

result = parallel_chain.invoke({"topic": "LangChain"})

print(result)
```

---

## 📤 Expected Output

```json id="lab3_out1"
{
  "summary": "...",
  "keywords": "..."
}
```

---

## 🧪 Step 5: RunnableBranch (Conditional Logic)

```python id="lab3_code4"
from langchain_core.runnables import RunnableBranch

def is_advanced(input):
    return "advanced" in input["level"].lower()

branch = RunnableBranch(
    (is_advanced, ChatPromptTemplate.from_template("Explain {topic} in technical detail")),
    ChatPromptTemplate.from_template("Explain {topic} in simple terms")
)

chain = branch | model | StrOutputParser()

print(chain.invoke({"topic": "LangChain", "level": "beginner"}))
print(chain.invoke({"topic": "LangChain", "level": "advanced"}))
```

---

## 🧠 Step 6: Combine Everything (Real Pipeline)

```python id="lab3_code5"
pipeline = (
    RunnableLambda(lambda x: {"topic": x["topic"], "level": x["level"]})
    | RunnableBranch(
        (lambda x: x["level"] == "advanced",
         ChatPromptTemplate.from_template("Explain {topic} deeply")),
        ChatPromptTemplate.from_template("Explain {topic} simply")
    )
    | model
    | StrOutputParser()
)

print(pipeline.invoke({"topic": "RAG", "level": "advanced"}))
```

---

## 🔥 Real-World Use Cases

* Dynamic chatbot responses
* Multi-output APIs
* Intelligent routing systems
* Preprocessing + LLM + postprocessing pipelines

---

## 🧠 Key Takeaways

* LCEL is NOT just chaining → it's **data flow orchestration**
* RunnableParallel = speed
* RunnableBranch = intelligence
* RunnableLambda = flexibility

---

## 🧪 Exercises

1. Add a third branch:

   * "intermediate" level explanation
2. Modify parallel chain to return:

   * summary
   * keywords
   * difficulty (structured JSON)
3. Add preprocessing step:

   * clean input text before sending to model

---

## 📚 References

* Runnables: [https://python.langchain.com/docs/expression_language/interface/](https://python.langchain.com/docs/expression_language/interface/)
* LCEL Composition: [https://python.langchain.com/docs/expression_language/how_to/](https://python.langchain.com/docs/expression_language/how_to/)

```