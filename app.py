from fastapi import FastAPI
from pydantic import BaseModel
import os, json
from openai import OpenAI

client = OpenAI()  # Automatically uses OPENAI_API_KEY from env

app = FastAPI(title="Global Impact Agent")

class DomainInput(BaseModel):
    domain: str

SYSTEM_PROMPT = """
You are a strategic global innovation agent.

Your job:
Given a user's domain, identify:

1. Five of the world's largest high-impact problems
2. For each problem:
   - Why it is massive
   - A bold, actionable idea for how this domain could help
   - Why this idea could realistically work

Return structured JSON.
"""

@app.post("/generate")
async def generate_ideas(input: DomainInput):
    user_prompt = f"""
Domain: {input.domain}

Generate five high-impact global problems and how this domain could address them.
Return structured JSON in this format:

[
  {{
    "problem": "...",
    "why_massive": "...",
    "solution_idea": "...",
    "why_it_could_work": "..."
  }}
]
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        return {"success": True, "ideas": parsed}
    except Exception as e:
        return {"success": False, "error": str(e)}
