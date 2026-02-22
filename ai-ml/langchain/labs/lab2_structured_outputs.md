# Lab 2 — Structured Outputs with Pydantic + Azure OpenAI

## Objective

Learn how to:

* Define a **schema** for the model’s output using Pydantic.
* Instruct the model to **only** return valid JSON matching the schema.
* Automatically **validate** and parse the model’s output into a Python object you can use in your code.

By the end, you’ll have a mini **feature idea generator** that always returns clean, machine-readable JSON.

---

## Step 0 — Prereqs

If you’ve done Lab 1, you already have:

* Python venv set up
* Required packages installed
* Azure OpenAI environment variables set

Otherwise, run:

```bash
pip install -U langchain langchain-openai langchain-core pydantic
```

And make sure your env vars from Lab 1 are set:

```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-06-01"
export AZURE_OPENAI_CHAT_DEPLOYMENT="your-chat-deployment-name"
```

---

## Step 1 — Understand the concept

Plain text responses are great for humans but messy for code.
Structured outputs:

* **Schema**: Defines allowed fields, types, constraints.
* **Parser**: Gives model exact JSON formatting instructions.
* **Validation**: Ensures the response is correct (or raises errors you can handle).

---

## Step 2 — Create your schema

We’ll make a `FeatureIdea` schema with:

* `title`: short string
* `user_value`: why users care
* `complexity`: int from 1–5
* `acceptance_criteria`: list of testable criteria

---

## Step 3 — Create `lab2_structured.py`

```python
import os
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# 1) Define schema
class FeatureIdea(BaseModel):
    title: str = Field(..., description="Short title for the feature idea")
    user_value: str = Field(..., description="Why users will benefit")
    complexity: int = Field(..., ge=1, le=5, description="Estimated complexity on a scale of 1 to 5")
    acceptance_criteria: list[str] = Field(..., description="List of clear, testable acceptance criteria")

# 2) Create parser from schema
parser = PydanticOutputParser(pydantic_object=FeatureIdea)

# 3) Prompt with formatting instructions
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a product manager. Respond ONLY with valid JSON matching the schema."),
    ("human", """
Generate a feature idea for a note-taking app used by remote teams.
FORMAT INSTRUCTIONS:
{format_instructions}
"""),
]).partial(format_instructions=parser.get_format_instructions())

# 4) Azure OpenAI model client
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0.3,  # small creativity
)

# 5) Chain: prompt → model → parser
chain = prompt | llm | parser

# 6) Invoke
result = chain.invoke({})
print("=== Parsed Python object ===")
print(result)
print("\n=== JSON Output ===")
print(result.model_dump_json(indent=2))
```

---

## Step 4 — Run it

```bash
python lab2_structured.py
```

**Expected output (will vary):**

```
=== Parsed Python object ===
title='Real-Time Collaborative Notes' user_value='Allows remote teams to co-edit notes in real-time...' complexity=4 acceptance_criteria=['Multiple users can edit simultaneously', 'Edits appear in < 1 second', 'No data loss after network issues']

=== JSON Output ===
{
  "title": "Real-Time Collaborative Notes",
  "user_value": "Allows remote teams to co-edit notes in real-time to increase productivity.",
  "complexity": 4,
  "acceptance_criteria": [
    "Multiple users can edit the same note at once",
    "Edits appear in less than 1 second",
    "No data is lost if a user goes offline and reconnects"
  ]
}
```

---

## Step 5 — Understand what happened

1. **Schema**: `FeatureIdea` defined exactly what we want.
2. **Parser**: `PydanticOutputParser` gave the model explicit JSON instructions.
3. **PromptTemplate**: Injected formatting instructions into the prompt.
4. **Validation**: If the model output is invalid, you’ll get a `ValidationError` instead of garbage.

---

## Step 6 — Try breaking it

Change `complexity` in the output manually (e.g., `6`) → rerun → watch validation fail.
This is how you catch bad model outputs before they crash your app later.

---

## Step 7 — Extensions

* Add fields like `risk_level` or `estimated_time_days`.
* Swap `list[str]` with a nested object type.
* Pass **dynamic user input** instead of hardcoding “note-taking app”:

```python
topic = input("What product are we brainstorming for? ")
chain.invoke({"product": topic})
```

(You’d also change the prompt to include `{product}`.)

---

## Step 8 — Checklist

* [ ] I know how to define a schema with Pydantic.
* [ ] I can instruct the model to match that schema.
* [ ] I can parse and validate the response.
* [ ] I know how to handle validation errors.

