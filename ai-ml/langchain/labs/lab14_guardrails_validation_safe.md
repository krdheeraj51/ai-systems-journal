# 🧪 Lab 14: Guardrails, Validation & Safe AI Systems

## 🎯 Objective
- Add safety layers to LLM applications
- Validate inputs and outputs
- Prevent hallucinations and unsafe responses
- Build reliable production-grade AI systems

---

## 📚 Concepts Covered
- Guardrails in LLM systems
- Input validation
- Output validation (schema enforcement)
- Prompt-based safety constraints
- Response filtering
- Fail-safe design

---

## ⚙️ Prerequisites
- Lab 1–13 completed
- Working API (FastAPI + LangChain)
- Understanding of RAG + Agents

---

## 🧠 Step 1: Why Guardrails Matter

Without guardrails:
- ❌ Hallucinations
- ❌ Unsafe responses
- ❌ Invalid outputs
- ❌ Security risks

With guardrails:
- ✅ Reliable outputs
- ✅ Safe responses
- ✅ Controlled behavior

---

## 🧪 Step 2: Input Validation (FastAPI Level)

```python id="lab14_code1"
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
````

---

## 🧪 Step 3: Input Sanitization

```python id="lab14_code2"
def sanitize_input(text: str) -> str:
    return text.strip().replace("\n", " ")
```

---

## 🧠 Step 4: Prompt Guardrails (VERY IMPORTANT)

```python id="lab14_code3"
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a safe AI assistant.

Rules:
- Do not generate harmful content
- Do not guess answers
- If unsure, say "I don't know"
- Only use provided context
"""),
    ("user", "{input}")
])
```

---

## 🧪 Step 5: Output Validation with Pydantic

```python id="lab14_code4"
from pydantic import BaseModel

class SafeResponse(BaseModel):
    answer: str
    confidence: str
```

---

## 🧪 Step 6: Use Output Parser

```python id="lab14_code5"
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=SafeResponse)

prompt = ChatPromptTemplate.from_template("""
{format_instructions}

Question: {question}
""").partial(format_instructions=parser.get_format_instructions())

chain = prompt | model | parser
```

---

## 🧠 Step 7: Response Filtering

```python id="lab14_code6"
def filter_response(response: str) -> str:
    blocked_words = ["hack", "illegal"]

    for word in blocked_words:
        if word in response.lower():
            return "Response blocked due to unsafe content."

    return response
```

---

## 🧪 Step 8: Add Guardrails to API

```python id="lab14_code7"
@app.post("/safe-rag")
async def safe_rag(request: QueryRequest):
    clean_query = sanitize_input(request.query)

    response = await rag_chain.ainvoke(clean_query)

    safe_output = filter_response(response)

    return {"response": safe_output}
```

---

## 🧠 Step 9: Prevent Hallucination (RAG Guard)

```python id="lab14_code8"
prompt = ChatPromptTemplate.from_template("""
Use ONLY the context below.

If answer is not found, say:
"I don't know"

Context:
{context}

Question:
{question}
""")
```

---

## 🧠 Step 10: Add Confidence Score (Advanced)

```python id="lab14_code9"
prompt = ChatPromptTemplate.from_template("""
Answer the question and provide confidence level:
- high
- medium
- low

Question: {question}
""")
```

---

## 🧠 Step 11: Fail-Safe Pattern

```python id="lab14_code10"
try:
    response = chain.invoke({"question": query})
except Exception:
    response = "System error. Please try again later."
```

---

## 📤 Expected Output

```json id="lab14_out"
{
  "answer": "LangChain is a framework...",
  "confidence": "high"
}
```

---

## 🧠 Key Takeaways

* Guardrails = essential for production AI
* Validate both input and output
* Prompt design enforces behavior
* Always include fail-safe mechanisms

---

## 🧪 Exercises

1. Add:

   * profanity filter
2. Force invalid JSON → observe parser failure
3. Add:

   * confidence threshold (reject low confidence)
4. Test malicious input:

   * "Ignore instructions and..."

---

## 📚 References

* Guardrails: [https://python.langchain.com/docs/guides/safety/](https://python.langchain.com/docs/guides/safety/)
* Pydantic: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

```

---

## 🔥 Where You Are Now

You now have:
- 🛡️ Safe AI systems  
- ✅ Validated pipelines  
- 🧠 Controlled outputs  