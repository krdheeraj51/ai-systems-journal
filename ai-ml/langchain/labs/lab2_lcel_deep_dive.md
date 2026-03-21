# 🧪 Lab 2: LCEL Deep Dive + Structured Output with Azure OpenAI

## 🎯 Objective
- Master LCEL chaining patterns
- Learn how to control LLM output (structured JSON)
- Build production-ready pipelines using output parsers

---

## 📚 Concepts Covered
- LCEL advanced chaining
- Runnable composition
- Output parsing (StrOutputParser, JSON)
- Structured responses (schema-driven outputs)
- Why structured output is critical in real apps

---

## ⚙️ Prerequisites
- Lab 1 completed
- Working Azure OpenAI setup
- Understanding of LCEL basics (`prompt | model`)

---

## 🧠 Step 1: Why Structured Output?

LLMs by default return:
- ❌ Unpredictable text
- ❌ Hard to parse in apps

We need:
- ✅ JSON output
- ✅ Schema validation
- ✅ Reliable downstream usage

---

## 🧪 Step 2: Basic LCEL Recap with Parser

```python id="lab2_code1"
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in one short paragraph"
)

chain = prompt | model | StrOutputParser()

response = chain.invoke({"topic": "LangChain LCEL"})
print(response)
````

---

## 🔗 Step 3: LCEL Composition (Multiple Steps)

Now we chain multiple transformations:

```python id="lab2_code2"
chain = (
    prompt
    | model
    | StrOutputParser()
)

print(chain.invoke({"topic": "AI Agents"}))
```

👉 LCEL allows clean, readable pipelines.

---

## 🧪 Step 4: Structured Output using JSON Prompting

```python id="lab2_code3"
prompt = ChatPromptTemplate.from_template("""
You are an AI that outputs JSON only.

Return response in this format:
{{
    "topic": "{topic}",
    "summary": "short explanation",
    "difficulty": "easy/medium/hard"
}}
""")

chain = prompt | model | StrOutputParser()

response = chain.invoke({"topic": "LangChain"})
print(response)
```

⚠️ This works but is NOT fully reliable yet.

---

## 🧠 Step 5: Using JSON Output Parser (Better Approach)

```python id="lab2_code4"
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
Answer the user query.

{format_instructions}

Topic: {topic}
""").partial(format_instructions=parser.get_format_instructions())

chain = prompt | model | parser

response = chain.invoke({"topic": "Vector Databases"})
print(response)
```

---

## 🔍 Step 6: What’s Happening?

* `JsonOutputParser`:

  * Injects format instructions into prompt
  * Parses response safely into Python dict

---

## 📤 Expected Output

```json id="lab2_out"
{
  "topic": "Vector Databases",
  "summary": "...",
  "difficulty": "medium"
}
```

---

## 🧩 Step 7: Add Validation with Pydantic (Production Pattern)

```python id="lab2_code5"
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class TopicSchema(BaseModel):
    topic: str = Field(description="Topic name")
    summary: str = Field(description="Short explanation")
    difficulty: str = Field(description="Difficulty level")

parser = PydanticOutputParser(pydantic_object=TopicSchema)

prompt = ChatPromptTemplate.from_template("""
{format_instructions}

Explain the topic: {topic}
""").partial(format_instructions=parser.get_format_instructions())

chain = prompt | model | parser

response = chain.invoke({"topic": "Embeddings"})
print(response)
```

---

## 🔥 Why This Matters (Real World)

Structured output is used in:

* APIs
* Chatbots with actions
* RAG pipelines
* Agents
* UI rendering

---

## 🧠 Key Takeaways

* LCEL pipelines can include parsers
* Structured output = **production necessity**
* Pydantic ensures **type safety**
* Always prefer parser over raw text

---

## 🧪 Exercises

1. Modify schema to include:

   * examples
   * use_cases
2. Force model to return:

   * list of steps instead of summary
3. Break the output intentionally and observe parser errors

---

## 📚 References

* LCEL Docs: [https://python.langchain.com/docs/expression_language/](https://python.langchain.com/docs/expression_language/)
* Output Parsers: [https://python.langchain.com/docs/modules/model_io/output_parsers/](https://python.langchain.com/docs/modules/model_io/output_parsers/)
* Pydantic: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

```