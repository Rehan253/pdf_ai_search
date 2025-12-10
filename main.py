from search_engine import SearchEngine

def main():
    print("\n===============================")
    print("   AI PDF Semantic Search")
    print("===============================\n")

    engine = SearchEngine()

    while True:
        query = input("\nEnter your question (or type 'exit' to quit):\n>> ")

        if query.lower() == "exit":
            print("Goodbye!")
            break

        results = engine.search(query, k=5)

        print("\n=== TOP RESULTS ===\n")

        for res in results:
            print(f"Score: {res['distance']}")
            print(f"File: {res['metadata']['filename']}")
            print(f"Page: {res['metadata']['page']}")
            print("-----------------------------")

if __name__ == "__main__":
    main()
