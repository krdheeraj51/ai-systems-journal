# Lab 5 — Multi-Agent Workflow with a Researcher, Writer & Critic

## Objective

* Build a tiny multi-agent pipeline where:

  1. **Researcher** produces factual bullet points about a topic.
  2. **Writer** turns bullets into a concise summary.
  3. **Critic** evaluates the summary and either **approves** or **requests a revision**.
* Implement a **controlled retry loop** so revisions happen automatically (up to a limit).
* Keep everything grounded, observable, and easy to extend.

---

## Step 0 — Prereqs (same env as earlier labs)

Make sure you already completed Labs 1–4 and have:

* Python venv activated
* Packages installed:

```bash
pip install -U langchain langchain-openai langchain-core langgraph
```

* Azure OpenAI env vars set:

```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-06-01"
export AZURE_OPENAI_CHAT_DEPLOYMENT="your-chat-deployment-name"
```

---

## Step 1 — Design notes (mental model)

* Each *agent* is a small function that accepts a `state` dict and returns an updated `state`.
* The **orchestrator** coordinates the flow:

  * Researcher → Writer → Critic
  * If Critic returns `revise`, orchestrator runs Researcher+Writer again (optionally carrying Critic feedback)
  * Stop after a max number of iterations to avoid infinite loops
* We use a single Azure LLM (same deployment) for all agents, but we give each agent a different *system prompt* to shape its role.

---

## Step 2 — Create `lab5_multiagent.py`

Create this file and paste the code below. It is self-contained and runnable.

```python
# lab5_multiagent.py
import os
from typing import Dict, List
from dataclasses import dataclass, field
import time

from langchain_openai import AzureChatOpenAI

# ---------- Configuration ----------
MAX_REVISIONS = 2  # how many times Critic may request a revision before giving up
SLEEP_BETWEEN_ITER = 0.25  # tiny pause between LLM calls to avoid short-rate limits

# Azure LLM client (shared)
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0.2,
)

# ---------- State dataclass for clarity ----------
@dataclass
class PipelineState:
    topic: str
    bullets: List[str] = field(default_factory=list)
    summary: str = ""
    critic_reason: str = ""  # why critic requested revision (if any)
    revision_round: int = 0


# ---------- Agent implementations ----------
def researcher(state: PipelineState) -> PipelineState:
    """
    Produces 4-6 factual bullet points about state.topic.
    Uses a system role to ask the LLM to return bullets prefixed with '- '.
    """
    prompt = (
        "You are a careful researcher. Produce 4 to 6 factual, distinct bullet points "
        f"about the following topic, each starting with '- '. Topic: {state.topic}\n"
        "Be concise (1-2 short sentences per bullet) and avoid speculation. If unsure, say you cannot find facts."
    )
    resp = llm.invoke(prompt)
    time.sleep(SLEEP_BETWEEN_ITER)
    text = resp.content.strip()
    # Extract lines starting with '-'
    bullets = [line.strip("- ").strip() for line in text.splitlines() if line.strip().startswith("-")]
    # Fallback: if the model returned plain lines (no dashes), split by newline and take first 5 non-empty
    if not bullets:
        bullets = [ln.strip() for ln in text.splitlines() if ln.strip()][:6]
    state.bullets = bullets[:6]
    return state


def writer(state: PipelineState) -> PipelineState:
    """
    Turns bullets into a single clear 100-150 word summary.
    If Critic provided feedback (state.critic_reason), incorporate it.
    """
    feedback_note = ""
    if state.critic_reason:
        feedback_note = (
            f"CRITIC FEEDBACK: {state.critic_reason}\n"
            "When writing the summary, address this feedback explicitly."
        )

    bullets_text = "\n".join(f"- {b}" for b in state.bullets)
    prompt = (
        "You are a concise technical writer. Convert the following bullets into a single 100-150 word summary.\n"
        f"{feedback_note}\n\nBullets:\n{bullets_text}\n\n"
        "Be factual, avoid hedging language like 'maybe' or 'probably', and do not invent sources."
    )
    resp = llm.invoke(prompt)
    time.sleep(SLEEP_BETWEEN_ITER)
    state.summary = resp.content.strip()
    return state


def critic(state: PipelineState) -> PipelineState:
    """
    Evaluates the summary along three axes:
      1) Factual consistency with bullets (did writer introduce claims not in bullets?)
      2) Clarity (is it concise and well structured?)
      3) Safety / unsupported claims (anything that sounds like hallucination?)
    Returns state.critic_reason non-empty if revise is requested.
    """
    # We ask the model to reply with a very small, machine-parseable verdict:
    # Either "VERDICT: APPROVE" or "VERDICT: REVISE" followed by a brief reason.
    prompt = (
        "You are a strict critic. Compare the SUMMARY to the provided BULLETS.\n\n"
        f"BULLETS:\n{chr(10).join(f'- {b}' for b in state.bullets)}\n\n"
        f"SUMMARY:\n{state.summary}\n\n"
        "Answer in this exact format (no extra text before or after):\n"
        "VERDICT: <APPROVE or REVISE>\n"
        "REASON: <one-sentence reason explaining why you asked for revision (or 'OK')>\n\n"
        "Revise if the summary contains claims not supported by bullets, is unclear, or uses hedging/unsupported language."
    )
    resp = llm.invoke(prompt)
    time.sleep(SLEEP_BETWEEN_ITER)
    out = resp.content.strip().splitlines()
    verdict = "REVISE"
    reason = "Critic could not parse verdict; requesting revision."
    # Parse reply
    for ln in out:
        ln = ln.strip()
        if ln.upper().startswith("VERDICT:"):
            verdict = ln.split(":", 1)[1].strip().upper()
        elif ln.upper().startswith("REASON:"):
            reason = ln.split(":", 1)[1].strip()
    if verdict == "APPROVE":
        state.critic_reason = ""
    else:
        # Ask the critic to provide targeted feedback to improve bullets (so Researcher can use it)
        prompt2 = (
            "Given the BULLETS and SUMMARY above, provide 1-2 short actionable suggestions "
            "that the Researcher can follow to improve the bullets (short, 1-2 lines each)."
        )
        resp2 = llm.invoke(prompt2)
        time.sleep(SLEEP_BETWEEN_ITER)
        state.critic_reason = resp2.content.strip()
    return state


# ---------- Orchestrator ----------
def run_pipeline(topic: str, max_rounds: int = MAX_REVISIONS) -> PipelineState:
    state = PipelineState(topic=topic)
    round_num = 0

    while True:
        round_num += 1
        state.revision_round = round_num
        print(f"\n=== ROUND {round_num}: Researcher → Writer → Critic ===")

        # Researcher
        state = researcher(state)
        print("\n[Researcher produced bullets]")
        for i, b in enumerate(state.bullets, start=1):
            print(f"{i}. {b}")

        # Writer
        state = writer(state)
        print("\n[Writer produced summary]\n")
        print(state.summary)

        # Critic
        state = critic(state)
        if not state.critic_reason:
            print("\n[Critic verdict] APPROVED ✅")
            return state
        else:
            print("\n[Critic verdict] REVISE ❗")
            print("Critic feedback to Researcher:")
            print(state.critic_reason)

        if round_num >= (max_rounds + 1):  # +1 because first run is round 1
            print("\nMaximum revision rounds reached. Stopping with last summary.")
            return state

        # Use critic feedback to refine bullets for the next round:
        # Simple strategy: prepend Critic's suggestion as an instruction for the Researcher to follow.
        # This keeps the pipeline simple and deterministic.
        prepend_instruction = f"(Incorporate this feedback into the facts: {state.critic_reason})\n"
        # Rebuild bullets by re-running researcher but giving it the feedback as an extra instruction:
        # Here we add the feedback into the topic string so the researcher sees it.
        state.topic = f"{state.topic}\n\n{prepend_instruction}"

        # loop continues for next revision


# ---------- Simple CLI ----------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Multi-agent Researcher→Writer→Critic demo")
    parser.add_argument("--topic", type=str, default="Agentic AI patterns in production", help="Topic to summarize")
    parser.add_argument("--max-revisions", type=int, default=MAX_REVISIONS, help="Max critic-requested revisions")
    args = parser.parse_args()

    final_state = run_pipeline(args.topic, max_rounds=args.max_revisions)
    print("\n\n=== FINAL OUTPUT ===")
    print("Topic:", final_state.topic)
    print("Revision rounds:", final_state.revision_round)
    print("\nBullets:")
    for b in final_state.bullets:
        print("-", b)
    print("\nSummary:\n", final_state.summary)
    if final_state.critic_reason:
        print("\nLast critic feedback (unresolved):\n", final_state.critic_reason)
```

---

## Step 3 — How to run

From a terminal with your env vars set:

```bash
python lab5_multiagent.py --topic "Best practices for deploying agents in production" --max-revisions 2
```

You’ll see a printed trace for each round:

* Researcher bullets
* Writer summary
* Critic verdict & feedback (if any)
* If Critic requests revise, the pipeline repeats (with Critic feedback injected for the Researcher)

---

## Step 4 — What to look for (expected behavior)

* First run: Researcher produces 4–6 bullets; Writer turns them into a clear \~100–150 word summary.
* Critic evaluates and usually either approves or asks for a revision with a short reason.
* If Critic requests revision, the pipeline runs again, and bullets (and therefore summary) should improve.
* The pipeline stops when the Critic approves or max revisions are reached.

---

## Step 5 — Why this pattern matters

* **Separation of concerns**: each agent focuses on one job → easier debugging and specialty prompts.
* **Iterative refinement**: Critic acts like a test suite or QA step; pipelines that loop until passing are common.
* **Observability**: printing intermediate outputs helps diagnose hallucinations or logic errors.
* **Extensible**: you can add a *Publisher* node that posts approved summaries to a database or a Slack channel.

---

## Step 6 — Troubleshooting

* `Unauthorized / 401` → verify `AZURE_OPENAI_API_KEY` and that the key belongs to the same resource as `AZURE_OPENAI_ENDPOINT`.
* **Output parsing is messy** → the Critic parsing is simple; if the LLM returns unexpected formatting, relax parsing or use a stricter parse like PydanticOutputParser.
* **Too many revisions / never converges** → lower temperature on `llm` (we set 0.2), reduce `MAX_REVISIONS`, or make the Critic stricter/clearer about pass criteria.
* **Rate limits** → increase `SLEEP_BETWEEN_ITER` or add exponential backoff and retries for LLM calls.
* **Researcher invents facts** → make Researcher prompt stricter: ask it to reply with only verifiable facts or to say `I don't know` when unsure.

---

## Step 7 — Extensions & experiments

* **Add a Fact-Checker**: Use RAG (from Lab 3) inside the Critic — check summary claims against an indexed document store.
* **Specialized agents**: Make Researcher use a different LLM (e.g., cheaper one for retrieval/processing) and Writer use a higher-quality LLM for copywriting.
* **Automated unit tests**: Have Critic include concrete assertions (e.g., must mention X) and fail if missing; turn test results into structured JSON.
* **Human-in-the-loop**: Pause on Critic `REVISE` and ask a human reviewer to edit bullets before repeating.
* **Observability dashboard**: Log each round and display in a small UI (e.g., streamlit) to monitor drift across runs.

---

## Step 8 — Quick checklist

* [ ] I ran `lab5_multiagent.py` and got bullets → summary → critic verdict.
* [ ] I saw at least one complete cycle of Researcher→Writer→Critic.
* [ ] When Critic requested revision, the pipeline repeated and updated the output.
* [ ] I understand where to inject RAG, add more agents, or involve humans.

