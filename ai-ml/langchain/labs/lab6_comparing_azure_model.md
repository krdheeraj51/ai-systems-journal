
# Lab 6 — Comparing Azure OpenAI Models Side-by-Side

## Objective

* Use two (or more) Azure OpenAI chat model deployments.
* Send the same prompt to each.
* Display results side-by-side for human evaluation.
* Measure simple metrics like token count and latency.

---

## Step 0 — Prerequisites

* Azure OpenAI resource with at least **two chat model deployments**, e.g.:

  * `gpt-4o`
  * `gpt-35-turbo`
* Same Python env from previous labs:

```bash
pip install -U langchain langchain-openai tabulate
```

* Environment variables:

```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-06-01"
```

---

## Step 1 — Create `lab6_model_comparison.py`

```python
# lab6_model_comparison.py
import os
import time
from tabulate import tabulate
from langchain_openai import AzureChatOpenAI

# --- Configure your deployments here ---
MODEL_DEPLOYMENTS = {
    "GPT-4o": "gpt-4o-deployment-name",         # replace with your Azure deployment name
    "GPT-35-Turbo": "gpt-35-turbo-deployment",  # replace with your Azure deployment name
}

API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# --- Function to query model ---
def query_model(model_name: str, deployment: str, prompt: str, temperature=0):
    llm = AzureChatOpenAI(
        azure_deployment=deployment,
        api_version=API_VERSION,
        azure_endpoint=AZURE_ENDPOINT,
        temperature=temperature,
    )
    start_time = time.time()
    resp = llm.invoke(prompt)
    latency = time.time() - start_time
    content = resp.content.strip()
    return {
        "model": model_name,
        "response": content,
        "latency_sec": round(latency, 2),
        "chars": len(content),
    }

# --- Main comparison function ---
def compare_models(prompt: str):
    results = []
    for model_name, deployment in MODEL_DEPLOYMENTS.items():
        try:
            res = query_model(model_name, deployment, prompt)
            results.append(res)
        except Exception as e:
            results.append({
                "model": model_name,
                "response": f"ERROR: {e}",
                "latency_sec": None,
                "chars": None,
            })

    # Print table summary
    table = []
    for r in results:
        table.append([r["model"], r["latency_sec"], r["chars"]])
    print("\n=== Comparison Summary ===")
    print(tabulate(table, headers=["Model", "Latency (s)", "Chars"]))

    # Print outputs
    print("\n=== Outputs ===\n")
    for r in results:
        print(f"--- {r['model']} ---")
        print(r["response"])
        print()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compare Azure OpenAI models on same prompt")
    parser.add_argument("--prompt", type=str, default="Explain quantum computing in simple terms.")
    args = parser.parse_args()

    compare_models(args.prompt)
```

---

## Step 2 — Run it

Example:

```bash
python lab6_model_comparison.py --prompt "Summarize the key differences between Agentic AI and traditional AI systems."
```

---

## Step 3 — Expected Output

```
=== Comparison Summary ===
Model           Latency (s)    Chars
--------------  ------------  -------
GPT-4o                 2.11     478
GPT-35-Turbo           1.37     392

=== Outputs ===

--- GPT-4o ---
Agentic AI refers to...

--- GPT-35-Turbo ---
Agentic AI is a form of...
```

---

## Step 4 — How it works

* `MODEL_DEPLOYMENTS` dictionary maps **friendly model name** → **Azure deployment name**.
* The script queries each model sequentially with the **same prompt**.
* We collect:

  * Model name
  * Latency in seconds
  * Character count of output
* We display both a **summary table** and **full responses** for human comparison.

---

## Step 5 — Analysis Tips

When comparing:

1. **Content depth** — Does one model explain with more clarity/examples?
2. **Style** — Is one more concise or verbose?
3. **Factual accuracy** — Does either hallucinate or get details wrong?
4. **Latency** — Useful for time-sensitive apps.
5. **Output length** — Can indicate verbosity or conciseness.

---

## Step 6 — Extensions

* **Add token usage metrics**: wrap with Azure's response metadata to get prompt/output token counts.
* **Automated scoring**: pass both outputs to another LLM acting as a judge (meta-evaluation).
* **Multiple prompts batch**: feed in a list of prompts to get aggregate statistics.
* **Diff view**: use Python `difflib` to highlight text differences.


