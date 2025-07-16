# ingest.py

import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
from utils import load_documents, chunk_text
import numpy as np

DATA_DIR = "data/documents"
DB_DIR = "db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def main():
    documents = load_documents(DATA_DIR)
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = []
    metadata = []

    for filename, content in documents.items():
        chunks = chunk_text(content)
        texts.extend(chunks)
        metadata.extend([filename] * len(chunks))

    embeddings = model.encode(texts, show_progress_bar=True)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    # Save index
    os.makedirs(DB_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(DB_DIR, "faiss_index.index"))

    # Save metadata
    with open(os.path.join(DB_DIR, "metadata.json"), "w") as f:
        json.dump({"texts": texts, "metadata": metadata}, f)

    print(f"Ingested {len(texts)} chunks from {len(documents)} files.")

if __name__ == "__main__":
    main()
