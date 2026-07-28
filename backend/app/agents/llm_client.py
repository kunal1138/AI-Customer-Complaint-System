"""
Thin wrapper around the Groq API. Keeping this separate from the LangGraph
nodes means you can swap models, add retries, or mock this out in tests
without touching the graph logic.
"""
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads the .env file and loads GROQ_API_KEY into the environment

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

EXTRACTION_MODEL = "openai/gpt-oss-20b"    # fast, cheap — used for structured extraction / classification
REASONING_MODEL = "openai/gpt-oss-120b"    # used where more nuanced reasoning helps (root cause, CAPA)
# Note: the assignment originally specified gemma2-9b-it and llama-3.3-70b-versatile,
# but Groq has since decommissioned both models. These are Groq's official recommended
# replacements as of July 2026 — mention this substitution in your README/demo video.


def call_llm(prompt: str, system: str = "", model: str = EXTRACTION_MODEL,
             json_mode: bool = False, temperature: float = 0.2) -> str:
    """Call Groq's chat completion endpoint and return the raw text response."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        **kwargs,
    )
    return response.choices[0].message.content


def call_llm_json(prompt: str, system: str = "", model: str = EXTRACTION_MODEL,
                   temperature: float = 0.1) -> dict:
    """Call the LLM and parse the response as JSON, with a safety fallback."""
    raw = call_llm(prompt, system=system, model=model, json_mode=True, temperature=temperature)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: strip markdown code fences if the model added them anyway
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
