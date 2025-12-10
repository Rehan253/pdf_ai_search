import os
import json
from embedder import Embedder
from vector_store import VectorStore

def generate_snippet(text, max_length=200):
    """
    Returns a short snippet from the page text.
    Cuts long text to a maximum length.
    """
    if not text:
        return "[No text available]"

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


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
        if not query.strip():
            print("[WARN] Query cannot be empty.")
            return []

        try:
            query_embedding = self.embedder.embed_text(query)
        except Exception as e:
            print(f"[ERROR] Failed to embed query: {e}")
            return []

        results = self.vector_store.search(query_embedding, k)

        # Load snippets for each result
        enhanced_results = []
        for res in results:
            filename = res["metadata"]["filename"]
            page_num = res["metadata"]["page"]

            json_path = os.path.join("data/extracted", filename.replace(".pdf", ".json"))

            snippet = "[Snippet unavailable]"

            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Find correct page content
                for page in data["pages"]:
                    if page["page"] == page_num:
                        snippet = generate_snippet(page["text"])
                        break

            except Exception as e:
                print(f"[WARN] Could not load snippet from {json_path}: {e}")

            enhanced_results.append({
                "distance": res["distance"],
                "metadata": res["metadata"],
                "snippet": snippet
            })

        return enhanced_results





