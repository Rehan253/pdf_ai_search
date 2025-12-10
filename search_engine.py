import os
from embedder import Embedder
from vector_store import VectorStore


class SearchEngine:
    def __init__(self, index_path="data/index/faiss.index", metadata_path="data/index/metadata.json"):
        print("[INFO] Initializing Search Engine...")

        # Check index existence
        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"[ERROR] FAISS index not found at '{index_path}'. "
                "Please run build_index.py first."
            )

        # Check metadata existence
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(
                f"[ERROR] Metadata file not found at '{metadata_path}'. "
                "Please run build_index.py first."
            )

        try:
            self.embedder = Embedder()
        except Exception as e:
            raise RuntimeError(
                f"[ERROR] Could not load embedding model: {e}\n"
                "Make sure your environment is set correctly."
            )

        self.vector_store = VectorStore()

        try:
            self.vector_store.load(index_path, metadata_path)
        except Exception as e:
            raise RuntimeError(
                f"[ERROR] Failed to load FAISS index or metadata: {e}"
            )

        print("[INFO] Search Engine ready!")

    def search(self, query, k=5):
        """
        Perform semantic search on the index.
        """
        if not query.strip():
            print("[WARN] Query cannot be empty.")
            return []

        try:
            query_embedding = self.embedder.embed_text(query)
        except Exception as e:
            print(f"[ERROR] Failed to embed query: {e}")
            return []

        results = self.vector_store.search(query_embedding, k)

        if not results:
            print("[INFO] No results found for your query.")
        return results
