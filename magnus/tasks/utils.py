"""
Loader utils.
"""

# Python built-in
from datetime import datetime
from io import BytesIO
import pytz

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


def local_now() -> datetime:
    return datetime.now(pytz.timezone("UTC"))
