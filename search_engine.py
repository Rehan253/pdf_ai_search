import os
import json
from embedder import Embedder
from vector_store import VectorStore
import re

import re

def generate_snippet(text, query, max_length=250):
    """
    Extract the most relevant sentence(s) based on the query.
    Highlights query words.
    """

    if not text or not text.strip():
        return "[No text available]"

    # 1. Split text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    query_words = [w.lower() for w in query.split()]

    # 2. Score each sentence based on occurrence of query words
    best_sentence = None
    best_score = 0

    for sentence in sentences:
        sent_lower = sentence.lower()
        score = sum(1 for w in query_words if w in sent_lower)

        if score > best_score:
            best_score = score
            best_sentence = sentence

    # 3. If no sentence matched query, fallback to first part of text
    if not best_sentence:
        best_sentence = text[:max_length]

    # 4. If sentence is too long, trim it
    if len(best_sentence) > max_length:
        best_sentence = best_sentence[:max_length] + "..."

    # 5. Highlight query words
    snippet = best_sentence
    for w in query_words:
        snippet = re.sub(
            rf"\b({re.escape(w)})\b",
            r"**\1**",
            snippet,
            flags=re.IGNORECASE
        )

    return snippet



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
                        snippet = generate_snippet(page["text"], query)

                        break

            except Exception as e:
                print(f"[WARN] Could not load snippet from {json_path}: {e}")

            enhanced_results.append({
                "distance": res["distance"],
                "metadata": res["metadata"],
                "snippet": snippet
            })

        return enhanced_results





