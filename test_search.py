from search_engine import SearchEngine

engine = SearchEngine()

query = "What information does the document show about weather conditions?"

results = engine.search(query, k=5)

print("\n=== SEARCH RESULTS ===\n")
for res in results:
    print(f"Score: {res['distance']}")
    print(f"File: {res['metadata']['filename']}")
    print(f"Page: {res['metadata']['page']}")
    print("-------------------------")
