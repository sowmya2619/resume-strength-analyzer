import re
from collections import Counter


CORE_SECTIONS = {
    "objective": ["objective", "summary", "profile"],
    "education": ["education", "b.tech", "diploma", "cgpa", "percentage"],
    "skills": ["technical skills", "skills", "programming languages"],
    "projects": ["projects", "project"],
    "experience": ["experience", "internship", "training"],
    "certifications": ["certifications", "certification", "courses"],
}

TECH_SKILLS = [
    "java",
    "python",
    "spring boot",
    "flask",
    "rest api",
    "rest apis",
    "mysql",
    "dbms",
    "html",
    "css",
    "javascript",
    "git",
    "machine learning",
    "deep learning",
    "networking",
    "cybersecurity",
    "cisco packet tracer",
    "data structures",
    "algorithms",
    "hashmaps",
    "stacks",
    "queues",
    "trees",
]

ACTION_VERBS = [
    "developed",
    "implemented",
    "designed",
    "built",
    "configured",
    "integrated",
    "deployed",
    "managed",
    "analyzed",
    "optimized",
]

STOP_WORDS = {
    "and",
    "the",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "using",
    "will",
    "are",
    "was",
    "you",
    "your",
    "our",
    "their",
    "have",
    "has",
    "job",
    "role",
    "candidate",
    "experience",
}


def analyze_resume(resume_text: str, job_description: str = "") -> dict:
    normalized_resume = normalize(resume_text)
    normalized_job = normalize(job_description)

    section_results = detect_sections(normalized_resume)
    skills = detect_skills(normalized_resume)
    action_score = score_action_verbs(normalized_resume)
    readability_score = score_readability(resume_text)
    keyword_result = compare_keywords(normalized_resume, normalized_job)

    section_score = round(sum(section_results.values()) / len(section_results) * 100)
    skills_score = min(100, len(skills) * 7)
    keyword_score = keyword_result["matchScore"] if job_description else 72

    ats_score = round(
        section_score * 0.28
        + skills_score * 0.24
        + keyword_score * 0.28
        + action_score * 0.12
        + readability_score * 0.08
    )

    return {
        "atsScore": ats_score,
        "grade": grade_for(ats_score),
        "sectionScore": section_score,
        "skillsScore": skills_score,
        "keywordScore": keyword_score,
        "actionVerbScore": action_score,
        "readabilityScore": readability_score,
        "detectedSections": section_results,
        "detectedSkills": skills,
        "matchedKeywords": keyword_result["matchedKeywords"],
        "missingKeywords": keyword_result["missingKeywords"],
        "suggestions": build_suggestions(section_results, skills, keyword_result, action_score, readability_score),
    }


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def detect_sections(text: str) -> dict:
    results = {}
    for section, markers in CORE_SECTIONS.items():
        results[section] = any(marker in text for marker in markers)
    return results


def detect_skills(text: str) -> list[str]:
    return sorted({skill for skill in TECH_SKILLS if skill in text})


def score_action_verbs(text: str) -> int:
    count = sum(1 for verb in ACTION_VERBS if verb in text)
    return min(100, count * 12)


def score_readability(text: str) -> int:
    words = re.findall(r"[A-Za-z]+", text)
    if len(words) < 120:
        return 55
    if len(words) > 900:
        return 72
    bullet_count = text.count("•") + text.count("- ")
    return min(100, 70 + min(25, bullet_count * 2))


def compare_keywords(resume_text: str, job_description: str) -> dict:
    if not job_description:
        return {"matchScore": 72, "matchedKeywords": [], "missingKeywords": []}

    job_keywords = extract_keywords(job_description)
    resume_tokens = set(extract_keywords(resume_text))

    matched = sorted(keyword for keyword in job_keywords if keyword in resume_tokens)
    missing = sorted(keyword for keyword in job_keywords if keyword not in resume_tokens)
    score = round((len(matched) / max(len(job_keywords), 1)) * 100)

    return {
        "matchScore": score,
        "matchedKeywords": matched[:18],
        "missingKeywords": missing[:18],
    }


def extract_keywords(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", text.lower())
    filtered = [word for word in words if word not in STOP_WORDS]
    common = Counter(filtered).most_common(45)
    return [word for word, _count in common]


def build_suggestions(section_results, skills, keyword_result, action_score, readability_score) -> list[str]:
    suggestions = []
    missing_sections = [section.title() for section, present in section_results.items() if not present]

    if missing_sections:
        suggestions.append("Add or clearly label these sections: " + ", ".join(missing_sections) + ".")

    if len(skills) < 8:
        suggestions.append("Add more role-relevant technical skills, grouped by language, backend, database, tools, and concepts.")

    if keyword_result["missingKeywords"]:
        suggestions.append("Include important job-description keywords naturally: " + ", ".join(keyword_result["missingKeywords"][:8]) + ".")

    if action_score < 70:
        suggestions.append("Start project bullets with strong action verbs such as Developed, Implemented, Designed, Integrated, or Deployed.")

    if readability_score < 75:
        suggestions.append("Use short bullet points with measurable outcomes, technologies used, and project impact.")

    if not suggestions:
        suggestions.append("Resume structure is strong. Add measurable outcomes and deployment links to make it more recruiter-friendly.")

    return suggestions


def grade_for(score: int) -> str:
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 55:
        return "Needs Improvement"
    return "Weak"
