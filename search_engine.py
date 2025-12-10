from embedder import Embedder
from vector_store import VectorStore
import numpy as np

class SearchEngine:
    def __init__(self, index_path="data/index/faiss.index", metadata_path="data/index/metadata.json"):
        """
        Loads the FAISS index and metadata.
        Initializes the embedder for query embedding.
        """
        print("[INFO] Initializing Search Engine...")

        self.embedder = Embedder()              # For converting questions → embeddings
        self.vector_store = VectorStore()       # For searching embeddings
        
        # Load FAISS index + metadata
        self.vector_store.load(index_path, metadata_path)

        print("[INFO] Search Engine ready!")

    def search(self, query, k=5):
        """
        Perform semantic search on the index.
        """
        print(f"[INFO] Searching for: {query}")

        # Convert query text to embedding
        query_embedding = self.embedder.embed_text(query)

        # Perform FAISS search
        results = self.vector_store.search(query_embedding, k)

        return results
