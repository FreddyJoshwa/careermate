from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def generate_first_question(role):
    prompt = f"""
You are a technical interviewer.

Role: {role}

Generate ONE short interview question suitable for a 2-minute mock interview.
Return only the question text.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def generate_followup_question(role, previous_question, previous_answer):
    prompt = f"""
You are a technical interviewer.

Role: {role}

Previous Question:
{previous_question}

Candidate Answer:
{previous_answer}

Generate ONE short follow-up interview question based on the candidate's answer.
Return only the question text.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def evaluate_answer(question, answer):
    prompt = f"""
You are a technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer and return ONLY valid JSON in this format:
{{
  "score": 7,
  "feedback": "short practical feedback"
}}

Rules:
- score must be a number from 0 to 10
- feedback must be short and practical
- do not include markdown, explanations, or extra text
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    raw_json = raw[start:end+1]

    return json.loads(raw_json)