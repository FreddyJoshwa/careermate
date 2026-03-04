from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def generate_roadmap(goal, skills, missing_skills):

    prompt = f"""
You are a career mentor.

Goal: {goal}

Current Skills:
{skills}

Missing Skills:
{missing_skills}

Create:
1) Quick Start Plan (3-5 days)
2) Detailed Roadmap (maximum 8 weeks)

Each week must include:
- skills
- tasks
- mini_project

Return JSON format:
{{
  "quick_start": {{}},
  "detailed_roadmap": {{}}
}}

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT include markdown, headings, code fences, or explanations.
- Output must start with {{ and end with }}.
- If you include "days", it must be a STRING like "3-5", not 3-5.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}]
    )

    raw = response.choices[0].message.content.strip()

    # Safe JSON extraction (in case model adds extra text)
    start = raw.find("{")
    end = raw.rfind("}")
    raw_json = raw[start:end+1]

    roadmap_dict = json.loads(raw_json)
    return roadmap_dict