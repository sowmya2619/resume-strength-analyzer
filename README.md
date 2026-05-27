# AI-Based Resume Strength Analyzer

A Flask web application that analyzes resumes for ATS readiness, skills coverage, keyword match, and improvement suggestions. This project is designed to match the resume entry for **Balla Sowmya Sushma** and demonstrates Python, Flask, Google Gemini AI integration, resume parsing, and deployment-friendly project structure.

## Built By

**Balla Sowmya Sushma**  
Computer Science Engineering student  
GitHub: [sowmya2619](https://github.com/sowmya2619)

## Tech Stack

- Python
- Flask
- HTML, CSS, JavaScript
- Google Gemini AI API
- PyPDF for PDF parsing
- PythonAnywhere-ready structure

## Features

- Upload resume as PDF or TXT
- Paste a target job description
- Generate ATS compatibility score
- Detect matched and missing keywords
- Identify technical skills from resume text
- Provide section-wise resume feedback
- Optional Google Gemini AI suggestions
- Rule-based fallback analysis when no API key is configured

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://localhost:5000
```

## Optional Gemini Setup

Create a `.env` file:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

Then run the app again.

## Project Structure

```text
resume-strength-analyzer/
  app.py
  requirements.txt
  services/
    analyzer.py
    gemini_client.py
    resume_parser.py
  templates/
    index.html
  static/
    styles.css
    app.js
```

## Resume Alignment

This project demonstrates:

- Flask backend development
- AI API integration using Google Gemini
- Resume parsing and text analysis
- ATS scoring logic
- User-friendly web interface
- Deployment-ready Python web app structure
