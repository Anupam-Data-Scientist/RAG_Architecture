import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment and Gemini API key
load_dotenv()
# You can use this if using .env: GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = "AIzaSyDLI30xmKSryF3ceSrpppEcGkpA2-_ZWtU"

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model (❌ DO NOT use "gemini-pro")
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

# Embedding model & database path
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DB_DIR = "db"

# ✅ Load FAISS index and metadata
def load_faiss():
    index = faiss.read_index(os.path.join(DB_DIR, "faiss_index.index"))
    with open(os.path.join(DB_DIR, "metadata.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    return index, data["texts"], data["metadata"]

# ✅ Search top_k similar chunks & call Gemini
def search_and_respond(query, top_k=3):
    # Encode query using sentence transformer
    embed_model = SentenceTransformer(EMBEDDING_MODEL)
    query_vector = embed_model.encode([query]).astype("float32")

    # Search similar chunks from FAISS
    index, texts, metadata = load_faiss()
    D, I = index.search(query_vector, top_k)
    retrieved = [(texts[i], metadata[i]) for i in I[0]]

    # Prepare context
    context = "\n\n".join([f"[{i+1}] From {fname}:\n{chunk}" for i, (chunk, fname) in enumerate(retrieved)])

    # Prompt for Gemini
    prompt = f"""You are an educational AI assistant. Use only the context below to answer the user's question clearly.
Avoid citations like [1], just explain in natural tone.

Context:
{context}

Question: {query}
Answer:"""

    # Call Gemini
    try:
        response = gemini_model.generate_content([{"text": prompt}])
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"
