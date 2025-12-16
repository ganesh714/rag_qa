import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    VECTOR_DB_PATH = "./data/chroma_db"
    UPLOAD_DIR = "./data/uploads"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" 
    GENERATION_MODEL_NAME = "gemini-2.5-flash"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

# Ensure directories exist
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)