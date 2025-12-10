import os
import json
from embedder import Embedder
from vector_store import VectorStore
import numpy as np

# Paths
extracted_folder = "data/extracted"
index_path = "data/index/faiss.index"
metadata_path = "data/index/metadata.json"

# Initialize modules
embedder = Embedder()
vector_store = VectorStore(dim=384)

all_embeddings = []
all_metadata = []

print("[INFO] Building index from extracted JSON files...")

# Loop through all JSON files
for filename in os.listdir(extracted_folder):
    if filename.endswith(".json"):
        json_path = os.path.join(extracted_folder, filename)

        print(f"[PROCESSING] {filename}")
        
        # Load JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        pages = data["pages"]
        filename_only = data["filename"]

        # Create metadata for each page
        metadata_list = [
            {"filename": filename_only, "page": page["page"]}
            for page in pages
        ]

        # Get embeddings
        page_texts = [p["text"] for p in pages]
        page_embeddings = embedder.embed_pages(pages)

        # Add to global lists
        all_embeddings.append(page_embeddings)
        all_metadata.extend(metadata_list)

# Combine embeddings into a single matrix
all_embeddings = np.vstack(all_embeddings)

# Add to FAISS index
vector_store.add_embeddings(all_embeddings, all_metadata)

# Save index + metadata
vector_store.save(index_path, metadata_path)

print("[SUCCESS] Index has been built and saved!")
