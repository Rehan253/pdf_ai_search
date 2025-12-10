from embedder import Embedder
import numpy as np


def test_embedding_dimension():
    model = Embedder()
    vector = model.embed_text("hello world")

    assert isinstance(vector, np.ndarray)
    assert vector.shape == (384,)  # MiniLM-L6-v2 output size
