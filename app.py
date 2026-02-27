import os
import json
from openai import OpenAI

# ----------------------------
# Setup
# ----------------------------

# Make sure you set your API key:
# export OPENAI_API_KEY="your_key_here"
client = OpenAI()

# ----------------------------
# Agent Prompt
# ----------------------------

SYSTEM_PROMPT = """
You are a strategic global innovation agent.

Your job:
Given a user's domain, identify:

1. Five of the world's largest high-impact problems
2. For each problem:
   - Why it is massive
   - A bold, actionable idea for how this domain could help
   - Why this idea could realistically work

Be specific. Avoid generic startup ideas.
Think at scale (millions to billions impacted).
Focus on leverage and asymmetry.
Return structured JSON.
"""

# ----------------------------
# Agent Function
# ----------------------------

def generate_ideas(domain: str):
    user_prompt = f"""
Domain: {domain}

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8,
    )

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
        return parsed
    except:
        return content


# ----------------------------
# CLI Interface
# ----------------------------

if __name__ == "__main__":
    print("\n🌍 Global Impact Agent")
    print("----------------------")
    domain = input("Enter your domain (e.g., AI, healthcare, climate tech, fintech): ")

    ideas = generate_ideas(domain)

    print("\n🚀 Results:\n")

    if isinstance(ideas, list):
        for i, idea in enumerate(ideas, 1):
            print(f"\n=== Idea {i} ===")
            print("Problem:", idea["problem"])
            print("Why Massive:", idea["why_massive"])
            print("Solution Idea:", idea["solution_idea"])
            print("Why It Could Work:", idea["why_it_could_work"])
    else:
        print(ideas)
