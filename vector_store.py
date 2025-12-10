import faiss
import numpy as np
import os
import json


class VectorStore:
    def __init__(self, dim=384):
        """
        dim = dimension of embeddings (384 for MiniLM-L6-v2)
        """
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)  # FAISS index (L2 distance)
        self.metadata = []  # Stores PDF info for each vector

    def add_embeddings(self, embeddings, metadata_list):
        """
        embeddings: numpy array of shape (N, 384)
        metadata_list: list of dictionaries with {filename, page}
        """
        embeddings = embeddings.astype("float32")  # FAISS needs float32
        self.index.add(embeddings)
        self.metadata.extend(metadata_list)
        print(f"[INFO] Added {len(embeddings)} embeddings to index.")

    def search(self, query_embedding, k=5):
        """
        Find the top k similar embeddings to the query.
        Returns distances and metadata.
        """
        query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "distance": float(dist),
                "metadata": self.metadata[idx]
            })

        return results

    def save(self, index_path, metadata_path):
        """Save FAISS index + metadata to disk."""
        faiss.write_index(self.index, index_path)
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4)
        print(f"[INFO] Index saved to {index_path}")
        print(f"[INFO] Metadata saved to {metadata_path}")

    def load(self, index_path, metadata_path):
        """Load FAISS index + metadata from disk."""
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        print("[INFO] Index and metadata loaded successfully!")
