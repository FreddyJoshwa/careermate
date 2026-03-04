from PyPDF2 import PdfReader
import docx2txt
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def parse_resume(file_path: str) -> str:
    """
    Takes a file path (PDF or DOCX) and returns extracted text.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print("Error reading PDF:", e)

    elif ext in [".docx", ".doc"]:
        try:
            text = docx2txt.process(file_path) or ""
        except Exception as e:
            print("Error reading DOCX:", e)

    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX allowed.")

    return text.strip()

def analyze_resume(text: str, goal: str) -> dict:
    """
    Use AI to find:
    - skills present in resume
    - missing skills based on user's goal
    Returns: {"skills": [...], "missing_skills": [...]}
    """
    if not text or len(text.strip()) < 30:
        return {"skills": [], "missing_skills": []}

    system_prompt = (
        "You are a strict resume analyzer. "
        "Return ONLY valid JSON. No markdown, no extra text."
    )

    user_prompt = f"""
Analyze the following resume text and user goal.

Resume:
{text}

User Goal:
{goal}

Task:
1) List the skills clearly mentioned in the resume.
2) List the important skills missing for the user's goal.

Return JSON exactly like:
{{
  "skills": ["skill1", "skill2"],
  "missing_skills": ["skillA", "skillB"]
}}

Rules:
- Keep each list max 25 items
- No duplicates
- Use short skill names (e.g., "React", "Node.js", "SQL")
"""

    try:
        response = client.chat.completions.create(
           model="llama-3.1-8b-instant",      # best quality
            # model="llama3-8b-8192",     # faster alternative
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}  # forces JSON
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        skills = data.get("skills", [])
        missing = data.get("missing_skills", [])

        # Safety + cleanup
        if not isinstance(skills, list): skills = []
        if not isinstance(missing, list): missing = []

        skills = sorted({str(s).strip() for s in skills if str(s).strip()})
        missing = sorted({str(s).strip() for s in missing if str(s).strip()})

        return {"skills": skills, "missing_skills": missing}

    except Exception as e:
        print("Error with AI analyze:", e)
        return {"skills": [], "missing_skills": [], "error": str(e)}