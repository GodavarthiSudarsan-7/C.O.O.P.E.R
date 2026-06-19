import chromadb
from sentence_transformers import SentenceTransformer

print("ChromaDB OK")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding Model Loaded")