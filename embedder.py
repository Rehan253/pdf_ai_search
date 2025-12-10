from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print("[INFO] Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        print("[INFO] Model loaded successfully!")

    def embed_text(self, text):
        """
        Convert a single text string into an embedding vector.
        """
        embedding = self.model.encode(text)
        return np.array(embedding)

    def embed_pages(self, pages):
        """
        Convert a list of page dictionaries into embeddings.
        Each page dict: {"page": x, "text": "..."}
        """
        texts = [page["text"] for page in pages]
        embeddings = self.model.encode(texts)
        return np.array(embeddings)
