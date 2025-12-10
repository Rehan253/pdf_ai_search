from vector_store import VectorStore
import os


def test_vector_store_loading():
    index_path = "data/index/faiss.index"
    metadata_path = "data/index/metadata.json"

    # Index must exist
    assert os.path.exists(index_path)
    assert os.path.exists(metadata_path)

    store = VectorStore()
    store.load(index_path, metadata_path)

    assert len(store.metadata) > 0
