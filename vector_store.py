import chromadb
from sentence_transformers import SentenceTransformer
from config import Config
import uuid

# Initialize Model and Client once
embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL_NAME)
chroma_client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
collection = chroma_client.get_or_create_collection(name="docs_collection")

def add_documents_to_db(chunks: list, filename: str):
    """Generates embeddings and stores them in ChromaDB."""
    if not chunks:
        return
        
    # Generate embeddings
    embeddings = embedding_model.encode(chunks).tolist()
    
    # Create unique IDs and metadata
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    metadatas = [{"source": filename} for _ in range(len(chunks))]
    
    # Add to Chroma
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_vector_db(query_text: str, n_results=3):
    """Queries the database for the most relevant chunks."""
    query_embedding = embedding_model.encode([query_text]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    # Flatten results (Chroma returns list of lists)
    documents = results['documents'][0] if results['documents'] else []
    return documents