"""
Loader utils.
"""

# Python built-in
from io import BytesIO

# pydocx
from docx import Document

# PyPDF2
from PyPDF2 import PdfReader


def decode_docx(content: bytes) -> str:
    stream = BytesIO(content)
    doc = Document(stream)
    return "".join(
        map(
            lambda paragraph: paragraph.text,
            doc.paragraphs,
        )
    )


def decode_pdf(content: bytes) -> str:
    stream = BytesIO(content)
    pdf = PdfReader(stream)
    return "".join(map(lambda page: page.extract_text(), pdf.pages))
