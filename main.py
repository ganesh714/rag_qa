from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import shutil

from config import Config
from utils import parse_document, chunk_text
from vector_store import add_documents_to_db, query_vector_db

app = FastAPI(title="Document QA System")

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel(Config.GENERATION_MODEL_NAME)

class QueryRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Accepts .txt, .md, .pdf, parses, chunks, and indexes them."""
    filename = file.filename
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in [".txt", ".md", ".pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .txt, .md, .pdf, .docx allowed.")

    file_path = os.path.join(Config.UPLOAD_DIR, filename)
    
    try:
        # Save file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process Document
        text = parse_document(file_path)
        chunks = chunk_text(text)
        add_documents_to_db(chunks, filename)
        
        return {"message": f"Successfully processed {filename}", "chunks_count": len(chunks)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_document(request: QueryRequest):
    """RAG endpoint: Search context -> Prompt Gemini -> Return Answer."""
    try:
        # 1. Retrieve Context
        context_chunks = query_vector_db(request.question)
        context_text = "\n\n".join(context_chunks)
        
        if not context_text:
            return {"answer": "I don't have enough information in the documents to answer that.", "sources": []}

        # 2. Construct Prompt
        prompt = (
            "You are a helpful assistant. Use the provided context to answer the user's question.\n\n"
            f"Context:\n{context_text}\n\n"
            f"Question: {request.question}"
        )

        # 3. Call Gemini
        response = model.generate_content(prompt)
        
        # Handle potential empty responses (e.g., safety blocks)
        if not response.text:
            raise ValueError("Gemini returned an empty response (possibly due to safety settings).")

        return {
            "answer": response.text,
            "sources": context_chunks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report")
async def get_report():
    """Returns hardcoded evaluation metrics as requested."""
    return {
        "context_precision": 0.9,
        "faithfulness": 0.85
    }