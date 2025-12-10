from embedder import Embedder

embedder = Embedder()

text = "This is a test sentence."

embedding = embedder.embed_text(text)

print("Embedding shape:", embedding.shape)
print("First 5 values:", embedding[:5])
