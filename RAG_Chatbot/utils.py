# utils.py

import os
import fitz  # PyMuPDF
import docx

def load_documents(folder_path):
    docs = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        ext = filename.split(".")[-1].lower()

        text = ""
        if ext == "pdf":
            with fitz.open(file_path) as doc:
                text = "\n".join([page.get_text() for page in doc])
        elif ext == "docx":
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        if text.strip():
            docs[filename] = text

    return docs

def chunk_text(text, max_length=500):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
