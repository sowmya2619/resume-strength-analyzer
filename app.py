from flask import Flask, jsonify, render_template, request

from services.gemini_client import analyze_resume_with_gemini
from services.resume_parser import extract_resume_text


ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

app = Flask(__name__)

# Maximum upload size: 4 MB
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():

    print()
    print("========== ANALYSIS STARTED ==========")

    # --------------------------------
    # Get uploaded resume
    # --------------------------------

    resume_file = request.files.get("resume")

    job_description = request.form.get(
        "jobDescription",
        ""
    ).strip()

    if not resume_file or resume_file.filename == "":
        return jsonify({
            "message": "Please upload a resume file."
        }), 400

    if not job_description:
        return jsonify({
            "message": "Please enter a job description."
        }), 400

    # --------------------------------
    # Validate file type
    # --------------------------------

    extension = (
        resume_file.filename
        .rsplit(".", 1)[-1]
        .lower()
    )

    print(
        f"Resume file: "
        f"{resume_file.filename}"
    )

    print(
        f"Job description length: "
        f"{len(job_description)}"
    )

    print(
        f"File extension: "
        f"{extension}"
    )

    if extension not in ALLOWED_EXTENSIONS:

        return jsonify({
            "message": (
                "Only PDF, DOCX and TXT "
                "files are supported."
            )
        }), 400

    # --------------------------------
    # Extract resume text
    # --------------------------------

    try:

        print("Reading resume directly...")

        resume_text = extract_resume_text(
            resume_file
        )

        print("Resume text extracted.")

        print(
            f"Resume text length: "
            f"{len(resume_text)}"
        )

    except Exception as error:

        print()
        print("========== RESUME ERROR ==========")

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error: {error}"
        )

        print(
            "=================================="
        )

        return jsonify({
            "message": "Failed to read the resume.",
            "error": str(error)
        }), 400

    if not resume_text.strip():

        return jsonify({
            "message": (
                "Could not extract text from "
                "the uploaded resume. "
                "If this is a scanned PDF, "
                "OCR may be required."
            )
        }), 400

    # --------------------------------
    # Gemini analysis
    # --------------------------------

    try:

        print()
        print("Sending resume to Gemini...")

        analysis = analyze_resume_with_gemini(
            resume_text=resume_text,
            job_description=job_description
        )

        print(
            "Gemini analysis completed."
        )

    except Exception as error:

        print()
        print("========== GEMINI ERROR ==========")

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error: {error}"
        )

        print(
            "=================================="
        )

        return jsonify({
            "message": (
                "Gemini is temporarily unavailable. "
                "Please try again in a few seconds."
            ),
            "error": str(error)
        }), 503

    # --------------------------------
    # Return analysis
    # --------------------------------

    analysis["resume_file"] = (
        resume_file.filename
    )

    print(
        "========== ANALYSIS FINISHED =========="
    )

    return jsonify(analysis)


@app.errorhandler(413)
def file_too_large(_error):

    return jsonify({
        "message": (
            "File is too large. "
            "Upload a file under 4 MB."
        )
    }), 413


if __name__ == "__main__":
    app.run(debug=True)