from services.gemini_client import analyze_resume_with_gemini


resume = """
Balla Sowmya Sushma

Education:
B.Tech Computer Science Engineering

Skills:
Java, Spring Boot, React, MySQL, Python, REST APIs, Git

Projects:
Blood Bank Management System
AI Resume Strength Analyzer

Experience:
Java Full Stack Intern

Certifications:
Python for Data Science
"""


job_description = """
We are looking for a Software Developer.

Required skills:
Java, Spring Boot, REST APIs, React, JavaScript, MySQL and Git.

Responsibilities:
Develop backend applications using Java and Spring Boot.
Create REST APIs.
Work with MySQL databases.
Develop frontend components using React.
Debug and test applications.
Use Git for version control.
"""


print()
print("======================================")
print("TESTING GEMINI RESUME ANALYZER")
print("======================================")


result = analyze_resume_with_gemini(
    resume_text=resume,
    job_description=job_description
)


print()
print("======================================")
print("GEMINI ANALYSIS RESULT")
print("======================================")


print(
    result
)