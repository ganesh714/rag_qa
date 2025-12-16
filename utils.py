import os
from pypdf import PdfReader
from config import Config

def parse_document(file_path: str) -> str:
    """Extracts text from .txt, .md, or .pdf files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")
        
    return text

def chunk_text(text: str, chunk_size=Config.CHUNK_SIZE, overlap=Config.CHUNK_OVERLAP):
    """Splits text into fixed-size chunks with overlap."""
    if not text:
        return []
        
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # Move forward by chunk_size minus overlap
        start += chunk_size - overlap
        
    return chunks