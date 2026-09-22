from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_resume_text(uploaded_file):
    """
    Extract text directly from an uploaded Flask file
    without permanently saving it to disk.
    """

    filename = uploaded_file.filename or ""
    extension = filename.rsplit(".", 1)[-1].lower()

    # Read uploaded file into memory
    file_data = uploaded_file.read()

    if extension == "txt":

        return file_data.decode(
            "utf-8",
            errors="ignore"
        )

    if extension == "pdf":

        pdf_file = BytesIO(file_data)

        reader = PdfReader(pdf_file)

        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]

        return "\n".join(pages)

    if extension == "docx":

        docx_file = BytesIO(file_data)

        document = Document(docx_file)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    return ""