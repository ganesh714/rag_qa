# AI-Powered Document Question-Answering System

**Project:** AI-Powered Document Question-Answering System 
**Repository Name:** rag_qa  

## 📋 Overview
This project is a RESTful API service that allows users to upload documents (PDF, TXT, MD) and ask natural language questions about their content. It implements a **Retrieval-Augmented Generation (RAG)** pipeline using **FastAPI**, **ChromaDB**, **Sentence-Transformers**, and **Google Gemini**.

The system processes uploaded files, chunks the text, creates vector embeddings, and retrieves relevant context to generate accurate answers using an LLM.

## 🚀 Features
* **Document Ingestion:** specialized parsing for `.pdf`, `.txt`, and `.md` files.
* **Vector Search:** Efficient similarity search using ChromaDB.
* **Context-Aware Answers:** Uses Google Gemini to answer questions based strictly on the uploaded document's context.
* **Evaluation Metrics:** A reporting endpoint provides system performance metrics.
* **Swagger UI:** Built-in interactive API documentation.

## 🛠️ Technical Stack
* **Language:** Python 3.9+
* **Framework:** FastAPI
* **Vector Database:** ChromaDB (Local/In-memory)
* **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **LLM:** Google Gemini (`gemini-2.5-flash`)
* **PDF Parsing:** `pypdf`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/ganesh714/rag_qa](https://github.com/ganesh714/rag_qa)
cd rag_qa

```

###2. Set Up Virtual EnvironmentIt is recommended to use a virtual environment to manage dependencies.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate

```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

###3. Install Dependencies```bash
pip install -r requirements.txt

```

###4. Configure Environment Variables1. Create a `.env` file in the root directory.
2. Add your Google Gemini API key (Get a free key from [Google AI Studio](https://aistudio.google.com/)).

```env
GEMINI_API_KEY=your_actual_api_key_here

```

---

##🏃‍♂️ Running the ApplicationStart the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload

```

The API will be accessible at:

* **Base URL:** `http://127.0.0.1:8000`
* **Interactive Docs (Swagger UI):** `http://127.0.0.1:8000/docs`

---

##📖 API Documentation###1. Upload Document**Endpoint:** `POST /upload`

**Description:** Uploads a file, processes it into chunks, and indexes it in the vector database.

* **Supported Formats:** `.pdf`, `.txt`, `.md`
* **Body (form-data):**
* `file`: (Select file from system)



**Example Response:**

```json
{
  "message": "Successfully processed sample_doc.pdf",
  "chunks_count": 15
}

```

###2. Query Document**Endpoint:** `POST /query`

**Description:** Ask a question about the uploaded document. Returns the answer and the source text blocks used.

* **Header:** `Content-Type: application/json`
* **Body (raw JSON):**
```json
{
  "question": "What are the main objectives listed in the document?"
}

```



**Example Response:**

```json
{
  "answer": "The main objectives are to create custom widgets...",
  "sources": [
    "chunk text 1...",
    "chunk text 2..."
  ]
}

```

###3. Performance Report**Endpoint:** `GET /report`

**Description:** Returns evaluation metrics for the RAG pipeline.

**Response:**

```json
{
  "context_precision": 0.9,
  "faithfulness": 0.85
}

```

---

##🧪 Testing with PostmanYou can use Postman to test the workflow without writing code.

1. **Upload File:**
* Select `POST` request to `http://127.0.0.1:8000/upload`.
* Go to **Body** -> **form-data**.
* Key: `file` (Change type from 'Text' to 'File' via the dropdown).
* Value: Select your `.pdf` file.
* Click **Send**.


2. **Ask Question:**
* Select `POST` request to `http://127.0.0.1:8000/query`.
* Go to **Body** -> **raw** -> Select **JSON**.
* Paste: `{"question": "Summarize the file."}`
* Click **Send**.



---

##📂 Project Structure
```
rag_qa/
├── data/                   # Storage for uploaded files & vector DB
├── .env                    # API Keys (GitIgnored)
├── .gitignore              # Files to exclude from Git
├── config.py               # Configuration settings
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── utils.py                # Document parsing & chunking logic
├── vector_store.py         # ChromaDB & Embedding logic
└── README.md               # Project documentation

```

## 🎥 Demo Video

[![Watch the video](https://1drv.ms/v/c/2b08b9b6f86447ff/IQA6J9s9QDvSSLpTpOElRYBeAV-c_Kb2jZ4qXXn4EqUwGUs)]
