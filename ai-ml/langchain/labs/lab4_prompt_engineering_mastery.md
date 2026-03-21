# 🧪 Lab 4: Prompt Engineering Mastery (Dynamic, Few-Shot, Production Prompts)

## 🎯 Objective
- Learn advanced prompt engineering techniques
- Build dynamic and reusable prompts using LCEL
- Use Few-shot prompting for better control
- Design production-grade prompts

---

## 📚 Concepts Covered
- ChatPromptTemplate deep dive
- System vs User vs Assistant roles
- Dynamic prompts
- Few-shot prompting
- Prompt partials (reusable variables)
- Prompt composition

---

## ⚙️ Prerequisites
- Lab 1–3 completed
- Familiarity with LCEL pipelines
- Basic understanding of LLM behavior

---

## 🧠 Step 1: Prompt Roles (Very Important)

LangChain chat prompts use roles:

- **system** → behavior control
- **user** → input
- **assistant** → examples / responses

---

## 🧪 Step 2: Structured Prompt with Roles

```python id="lab4_code1"
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI tutor."),
    ("user", "Explain {topic} in simple terms.")
])
````

---

## 🧪 Step 3: Dynamic Prompting

```python id="lab4_code2"
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} for a {audience} audience"
)

chain = prompt | model

print(chain.invoke({
    "topic": "LangChain",
    "audience": "beginner"
}).content)
```

---

## 🧪 Step 4: Prompt Partials (Reusable Components)

```python id="lab4_code3"
base_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in {style} style"
)

prompt = base_prompt.partial(style="simple")

chain = prompt | model

print(chain.invoke({"topic": "AI Agents"}).content)
```

---

## 🧪 Step 5: Few-Shot Prompting (VERY IMPORTANT)

Few-shot improves reliability significantly.

```python id="lab4_code4"
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "What is AI?", "output": "AI is machines simulating human intelligence."},
    {"input": "What is ML?", "output": "ML is a subset of AI that learns from data."}
]

example_prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}"),
    ("assistant", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    few_shot_prompt,
    ("user", "{input}")
])

chain = final_prompt | model

print(chain.invoke({"input": "What is LangChain?"}).content)
```

---

## 🧪 Step 6: Dynamic Few-Shot (Advanced Concept)

Instead of static examples, you can:

* Select examples dynamically
* Use similarity (later in RAG)

👉 For now, simulate dynamic selection:

```python id="lab4_code5"
def select_examples(topic):
    if "AI" in topic:
        return [{"input": "What is AI?", "output": "AI simulates intelligence"}]
    return [{"input": "What is Python?", "output": "Python is a programming language"}]
```

---

## 🧪 Step 7: Combine with LCEL Pipeline

```python id="lab4_code6"
chain = final_prompt | model | StrOutputParser()

response = chain.invoke({"input": "Explain embeddings"})
print(response)
```

---

## 🔥 Step 8: Production Prompt Pattern

Best practice template:

```python id="lab4_code7"
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a domain expert. Always respond in JSON."),
    ("user", "Task: {task}\nInput: {input}")
])
```

---

## 🧠 Key Takeaways

* Prompt = **core intelligence layer**
* Few-shot = **accuracy boost**
* Partials = **reusability**
* Dynamic prompts = **scalability**

---

## 🧪 Exercises

1. Create a prompt that:

   * Responds in bullet points
   * Includes examples
2. Add 3–5 few-shot examples for:

   * Coding explanations
3. Modify system prompt to act like:

   * interviewer
   * strict evaluator

---

## 📚 References

* Prompt Templates: [https://python.langchain.com/docs/modules/model_io/prompts/](https://python.langchain.com/docs/modules/model_io/prompts/)
* Few-shot prompting: [https://python.langchain.com/docs/modules/model_io/prompts/few_shot/](https://python.langchain.com/docs/modules/model_io/prompts/few_shot/)

```

---

## 🔥 Where You Are Now

You can now:
- Design **high-quality prompts**
- Control LLM behavior
- Improve output reliability significantly

