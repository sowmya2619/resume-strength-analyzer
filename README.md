# AI-Based Resume Strength Analyzer

A Flask web application that analyzes resumes for ATS readiness, skills coverage, keyword matching, and improvement suggestions. This project demonstrates Python, Flask, Google Gemini AI integration, resume parsing, and a deployment-ready project structure.

## 🌐 Live Website

**Try the application here:** [AI-Based Resume Strength Analyzer](https://sowmyasushma2619.pythonanywhere.com/)

Upload your resume, paste a target job description, and explore resume analysis and improvement suggestions.

## 👩‍💻 Built By

**Balla Sowmya Sushma**  
Computer Science Engineering  
GitHub: [sowmya2619](https://github.com/sowmya2619)

## 🛠️ Tech Stack

- Python
- Flask
- HTML, CSS, JavaScript
- Google Gemini AI API
- PyPDF for PDF parsing
- PythonAnywhere for deployment

## ✨ Features

- Upload resumes in PDF or TXT format
- Paste a target job description
- Generate an ATS compatibility score
- Identify matched and missing keywords
- Identify technical skills from resume text
- Provide section-wise resume feedback
- Generate AI-powered suggestions using Google Gemini
- Support rule-based fallback analysis when no API key is configured

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sowmya2619/resume_stregth_analyzer.git
cd resume_stregth_analyzer
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open the following URL in your browser:

```text
http://localhost:5000
```

## 🔑 Optional Google Gemini Setup

Create a `.env` file in the project root directory and add your API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

Restart the application after configuring the key.

**Security note:** Never commit your actual API key or `.env` file to GitHub.

## 📂 Project Structure

```text
resume-strength-analyzer/
├── app.py
├── requirements.txt
├── services/
│   ├── analyzer.py
│   ├── gemini_client.py
│   └── resume_parser.py
├── templates/
│   └── index.html
└── static/
    ├── styles.css
    └── app.js
```

## 🎯 Resume Alignment

This project demonstrates:

- Flask backend development
- AI API integration using Google Gemini
- Resume parsing and text analysis
- ATS scoring logic
- User-friendly web interface development
- Job description and keyword matching
- Deployment of a Python web application

## 🔗 Project Links

- **Live Demo:** [sowmyasushma2619.pythonanywhere.com](https://sowmyasushma2619.pythonanywhere.com/)
- **GitHub Profile:** [github.com/sowmya2619](https://github.com/sowmya2619)
- **Repository:** [AI Resume Strength Analyzer](https://github.com/sowmya2619/resume_stregth_analyzer)

---

*Built by Balla Sowmya Sushma to help job seekers analyze and improve their resumes using AI-assisted feedback.*
