import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


# =========================================================
# GEMINI MODELS
# =========================================================

PRIMARY_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"


# =========================================================
# JSON RESPONSE SCHEMA
# =========================================================

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_score": {
            "type": "integer"
        },

        "ats_score": {
            "type": "integer"
        },

        "job_match_score": {
            "type": "integer"
        },

        "matched_skills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "missing_skills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "recommended_skills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "strengths": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "weaknesses": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "experience_relevance": {
            "type": "string"
        },

        "project_relevance": {
            "type": "string"
        },

        "education_relevance": {
            "type": "string"
        },

        "ats_issues": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "improvement_suggestions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "improved_bullets": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "final_feedback": {
            "type": "string"
        }
    },

    "required": [
        "overall_score",
        "ats_score",
        "job_match_score",
        "matched_skills",
        "missing_skills",
        "recommended_skills",
        "strengths",
        "weaknesses",
        "experience_relevance",
        "project_relevance",
        "education_relevance",
        "ats_issues",
        "improvement_suggestions",
        "improved_bullets",
        "final_feedback"
    ]
}

# =========================================================
# BUILD GEMINI PROMPT
# =========================================================

def build_prompt(resume_text: str, job_description: str) -> str:

    return f"""
You are an expert AI resume analyzer and ATS consultant.

Analyze the candidate's resume against the provided job description.

Your goal is to evaluate the resume and provide useful,
practical and AI-powered recommendations to improve it.

========================
RESUME
========================

{resume_text[:12000]}

========================
JOB DESCRIPTION
========================

{job_description[:8000]}

========================
ANALYSIS REQUIREMENTS
========================

Calculate scores from 0 to 100:

1. overall_score
   Overall strength of the resume for the target job.

2. ats_score
   How suitable the resume is for ATS screening,
   including structure, readability, formatting,
   relevant skills and job-specific terminology.

3. job_match_score
   How closely the existing resume matches the target job.

Analyze the following:

- matched skills
- missing skills
- recommended skills
- resume strengths
- resume weaknesses
- experience relevance
- project relevance
- education relevance
- ATS issues
- improvement suggestions
- improved resume bullets
- final AI feedback

========================
MATCHED SKILLS
========================

List technical skills, tools, frameworks, programming
languages, platforms and relevant concepts that are
clearly present in the resume and relevant to the job.

========================
MISSING SKILLS
========================

List important skills from the job description that are
relevant to the role but are not clearly present in the
candidate's resume.

Do not claim that the candidate knows these skills.

========================
RECOMMENDED SKILLS
========================

Recommend skills that the candidate should learn or
strengthen to improve their resume and job match.

Recommendations should be based on:

- missing skills
- important technologies in the job description
- candidate's existing skills
- realistic next-step skills

Do not recommend random or unrelated skills.

Recommend approximately 5 to 10 practical skills.

========================
RESUME STRENGTHS
========================

Identify the strongest parts of the resume for this
specific job.

========================
RESUME WEAKNESSES
========================

Identify areas that reduce the resume's effectiveness
for this specific job.

========================
AI IMPROVEMENT SUGGESTIONS
========================

Provide practical suggestions to improve the resume.

Suggestions may include:

- skill improvements
- project improvements
- experience descriptions
- resume structure
- ATS improvements
- technical skill presentation
- achievement descriptions

========================
IMPROVED BULLETS
========================

Rewrite existing resume bullet points to make them
clearer, stronger and more professional.

IMPORTANT:
Do not invent achievements, technologies,
responsibilities, numbers or experience.

Only improve the wording of information already
present in the resume.

========================
FINAL AI FEEDBACK
========================

Provide a concise overall assessment explaining:

- what is already strong
- what needs improvement
- which skills should be learned
- how the candidate can improve the resume
- how the resume can better match the target job

========================
IMPORTANT RULES
========================

1. Analyze only information actually present in the resume.

2. Do NOT invent:
   - skills
   - work experience
   - projects
   - certifications
   - achievements
   - technologies
   - responsibilities

3. Do not claim the candidate knows a missing or
   recommended skill.

4. You may recognize reasonable synonyms.

5. Clearly distinguish between:
   - matched skills
   - missing skills
   - recommended skills

6. Recommended skills must be realistic and
   relevant to the target job.

7. Improved bullets must only rewrite existing
   resume information.

8. Return only the requested JSON structure.
"""

# =========================================================
# SINGLE GEMINI REQUEST
# =========================================================

def call_gemini(
    client,
    model,
    prompt
):

    print()
    print("----------------------------------------")
    print(f"Trying Gemini model: {model}")
    print("----------------------------------------")


    response = client.models.generate_content(

        model=model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=RESPONSE_SCHEMA,

            temperature=0.2
        )
    )


    if not response.text:

        raise RuntimeError(
            f"Gemini returned an empty response using {model}."
        )


    return json.loads(
        response.text
    )


# =========================================================
# MAIN GEMINI ANALYZER
# =========================================================

def analyze_resume_with_gemini(
    resume_text: str,
    job_description: str
) -> dict:

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )


    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )


    client = genai.Client(
        api_key=api_key
    )


    prompt = build_prompt(
        resume_text,
        job_description
    )


    # =====================================================
    # PRIMARY MODEL
    # =====================================================

    last_error = None


    for attempt in range(1, 4):

        try:

            print(
                f"Gemini primary attempt "
                f"{attempt}/3"
            )


            result = call_gemini(

                client,

                PRIMARY_MODEL,

                prompt
            )


            print(
                f"Gemini primary model succeeded: "
                f"{PRIMARY_MODEL}"
            )


            return result


        except Exception as error:

            last_error = error


            print()
            print(
                f"Primary model error: {error}"
            )


            error_text = str(error)


            # -------------------------------------------------
            # TEMPORARY ERRORS
            # -------------------------------------------------

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                if attempt < 3:

                    wait_time = 2 ** attempt


                    print(
                        "Temporary Gemini service issue."
                    )


                    print(
                        f"Waiting {wait_time} seconds "
                        f"before retry..."
                    )


                    time.sleep(
                        wait_time
                    )


                    continue


            # Non-temporary error

            break


    # =====================================================
    # FALLBACK MODEL
    # =====================================================

    print()

    print(
        "Primary Gemini model unavailable."
    )


    print(
        f"Trying fallback model: "
        f"{FALLBACK_MODEL}"
    )


    try:

        result = call_gemini(

            client,

            FALLBACK_MODEL,

            prompt
        )


        print(
            f"Fallback model succeeded: "
            f"{FALLBACK_MODEL}"
        )


        return result


    except Exception as fallback_error:

        print()

        print(
            "Fallback Gemini model also failed."
        )


        print(
            f"Fallback error: "
            f"{fallback_error}"
        )


        raise RuntimeError(
            "Gemini is temporarily unavailable. "
            "The primary model and fallback model "
            "could not process the request. "
            "Please try the analysis again after "
            "a short wait."
        ) from fallback_error