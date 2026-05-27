import os

from dotenv import load_dotenv

load_dotenv()


def generate_ai_feedback(resume_text: str, job_description: str, analysis: dict) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return fallback_feedback(analysis)

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = build_prompt(resume_text, job_description, analysis)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as error:
        return fallback_feedback(analysis) + f"\n\nAI service note: {error}"


def build_prompt(resume_text: str, job_description: str, analysis: dict) -> str:
    return f"""
You are an ATS resume coach. Give concise, practical feedback.

ATS score: {analysis["atsScore"]}
Detected skills: {", ".join(analysis["detectedSkills"])}
Missing keywords: {", ".join(analysis["missingKeywords"])}

Resume:
{resume_text[:5000]}

Job description:
{job_description[:2500] if job_description else "No job description provided."}

Return:
1. Top 3 strengths
2. Top 5 improvements
3. Suggested improved resume bullets
"""


def fallback_feedback(analysis: dict) -> str:
    suggestions = "\n".join(f"- {item}" for item in analysis["suggestions"])
    return (
        "Rule-based feedback:\n"
        f"- ATS grade: {analysis['grade']} ({analysis['atsScore']}/100)\n"
        f"- Skills detected: {len(analysis['detectedSkills'])}\n"
        f"- Keyword score: {analysis['keywordScore']}/100\n\n"
        "Recommended improvements:\n"
        f"{suggestions}"
    )
