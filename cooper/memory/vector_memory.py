import chromadb
from sentence_transformers import SentenceTransformer

class VectorMemory:

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./cooper_memory")

        self.collection = self.client.get_or_create_collection(
            name="cooper_memories"
        )

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def remember(self, text: str):
        embedding = self.model.encode(text).tolist()

        memory_id = str(self.collection.count() + 1)

        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[text]
        )

    def recall(self, query: str, limit: int = 5):
        embedding = self.model.encode(query).tolist()

        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit
        )

        if not result["documents"]:
            return []

        return result["documents"][0]