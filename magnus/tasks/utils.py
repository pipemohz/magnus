"""
Loader utils.
"""

# Python built-in
from datetime import datetime
from io import BytesIO

import pytz
import zipfile, re
import fitz


def decode_docx(content: bytes) -> str:
    stream = BytesIO(content)
    docx = zipfile.ZipFile(stream)
    text = docx.read('word/document.xml').decode('utf-8')
    cleaned = re.sub('<(.|\n)*?>','',text)
    return cleaned

def decode_pdf(content: bytes) -> str:
    stream = BytesIO(content)
    doc = fitz.open(stream=stream, filetype="pdf")
    text= "".join(map(lambda page: page.get_textpage().extractText(),doc.pages(step=1)))
    # for page in doc.pages(step=1):
    #     text += page.get_textpage().extractText()
    cleaned = text.strip() #re.sub('\n\n','',text)
    return cleaned


def local_now() -> datetime:
    return datetime.now(pytz.timezone("UTC"))
