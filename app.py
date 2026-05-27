from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from services.analyzer import analyze_resume
from services.gemini_client import generate_ai_feedback
from services.resume_parser import extract_resume_text


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    resume_file = request.files.get("resume")
    job_description = request.form.get("jobDescription", "").strip()

    if not resume_file or resume_file.filename == "":
        return jsonify({"message": "Please upload a resume file."}), 400

    extension = resume_file.filename.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({"message": "Only PDF and TXT files are supported."}), 400

    UPLOAD_DIR.mkdir(exist_ok=True)
    filename = secure_filename(resume_file.filename)
    file_path = UPLOAD_DIR / filename
    resume_file.save(file_path)

    resume_text = extract_resume_text(file_path)
    if not resume_text.strip():
        return jsonify({"message": "Could not read text from the resume."}), 400

    analysis = analyze_resume(resume_text, job_description)
    analysis["aiFeedback"] = generate_ai_feedback(resume_text, job_description, analysis)

    return jsonify(analysis)


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"message": "File is too large. Upload a file under 4 MB."}), 413


if __name__ == "__main__":
    app.run(debug=True)
